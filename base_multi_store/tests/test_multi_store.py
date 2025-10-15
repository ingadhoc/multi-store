# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger
from psycopg2 import IntegrityError


class TestMultiStore(TransactionCase):
    """
    Test suite for the base_multi_store module.
    It covers constraints and business logic for res.store and res.users.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Get the multi-store group
        cls.group_multi_store = cls.env.ref("base_multi_store.group_multi_store")

        # Create companies
        cls.company_a = cls.env["res.company"].create({"name": "Company A"})
        cls.company_b = cls.env["res.company"].create({"name": "Company B"})

        # Create stores
        cls.store_a = cls.env["res.store"].create({"name": "Store A", "company_id": cls.company_a.id})
        cls.store_b = cls.env["res.store"].create(
            {"name": "Store B", "company_id": cls.company_a.id, "parent_id": cls.store_a.id}
        )
        cls.store_c = cls.env["res.store"].create({"name": "Store C", "company_id": cls.company_a.id})

        # Create a test user with access to two stores
        cls.test_user = cls.env["res.users"].create(
            {
                "name": "Test User",
                "login": "testuser",
                "company_id": cls.company_a.id,
                "company_ids": [(4, cls.company_a.id)],
                # The user has access to stores A and B
                "store_ids": [(6, 0, [cls.store_a.id, cls.store_b.id])],
                # The active store is A
                "store_id": cls.store_a.id,
            }
        )

    @mute_logger("odoo.sql_db")
    def test_01_store_unique_name_constraint(self):
        """Test that store name is unique per company."""
        # 1. Should fail: Try to create a store with the same name in the same company
        with self.assertRaises(IntegrityError):
            self.env["res.store"].create({"name": "Store A", "company_id": self.company_a.id})

        # 2. Should pass: Create a store with the same name but in a different company
        store_a_comp_b = self.env["res.store"].create({"name": "Store A", "company_id": self.company_b.id})
        self.assertTrue(store_a_comp_b)

    def test_02_store_recursion_constraint(self):
        """Test that creating recursive stores is not allowed."""
        with self.assertRaises(ValidationError):
            # Try to set store_a's parent to store_b, creating a cycle (A->B->A)
            self.store_a.parent_id = self.store_b.id

    def test_03_user_store_id_constraint(self):
        """Test that user's store_id must be in their store_ids."""
        # 1. Should fail: The user does not have access to store C
        with self.assertRaises(ValidationError):
            self.test_user.store_id = self.store_c.id

        # 2. Should pass: The user has access to store B
        self.test_user.store_id = self.store_b.id
        self.assertEqual(self.test_user.store_id, self.store_b)

    def test_04_name_search_user_preference(self):
        """Test name_search with user_preference context."""
        # Run the search as the test user
        Store = self.env["res.store"].with_user(self.test_user)
        # Use the context that triggers the special logic
        results = Store.with_context(user_preference=True).name_search(name="")
        result_ids = [res[0] for res in results]

        # The user should only see the stores they have access to (A and B)
        self.assertIn(self.store_a.id, result_ids)
        self.assertIn(self.store_b.id, result_ids)
        # The user should not see Store C
        self.assertNotIn(self.store_c.id, result_ids)

    def test_05_multi_store_group_assignment_on_write(self):
        """Test group is assigned/removed when user's stores are updated."""
        # Initial state: User has 2 stores, so they should be in the group
        self.assertIn(self.group_multi_store, self.test_user.group_ids)

        # Action: Remove one store, leaving the user with only one
        self.test_user.write({"store_ids": [(6, 0, [self.store_a.id])]})
        # Verification: The group should be removed
        self.assertNotIn(self.group_multi_store, self.test_user.group_ids)

        # Action: Go back to zero stores
        self.test_user.write({"store_ids": [(5, 0, 0)]})
        # Verification: The group should still be removed
        self.assertNotIn(self.group_multi_store, self.test_user.group_ids)

        # Action: Add two stores back
        self.test_user.write({"store_ids": [(6, 0, [self.store_a.id, self.store_b.id])]})
        # Verification: The group should be added back
        self.assertIn(self.group_multi_store, self.test_user.group_ids)

    def test_06_multi_store_group_assignment_on_create(self):
        """Test group is assigned correctly when a new user is created."""
        # 1. Create a user with more than one store
        user_multi = self.env["res.users"].create(
            {
                "name": "Multi Store User",
                "login": "multi",
                "store_ids": [(6, 0, [self.store_a.id, self.store_b.id])],
            }
        )
        # Verification: The user should be in the multi-store group
        self.assertIn(self.group_multi_store, user_multi.group_ids)

        # 2. Create a user with exactly one store
        user_single = self.env["res.users"].create(
            {
                "name": "Single Store User",
                "login": "single",
                "store_ids": [(6, 0, [self.store_a.id])],
            }
        )
        # Verification: The user should NOT be in the multi-store group
        self.assertNotIn(self.group_multi_store, user_single.group_ids)

        # 3. Create a user with no stores
        user_none = self.env["res.users"].create(
            {
                "name": "No Store User",
                "login": "none",
            }
        )
        # Verification: The user should NOT be in the multi-store group
        self.assertNotIn(self.group_multi_store, user_none.group_ids)
