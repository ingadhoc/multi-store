from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSaleOrderStore(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.store_own = cls.env["res.store"].create({"name": "Own store"})
        cls.store_other = cls.env["res.store"].create({"name": "Other store"})
        cls.warehouse_other = cls.env["stock.warehouse"].create(
            {"name": "Other store warehouse", "code": "OSW", "store_id": cls.store_other.id}
        )
        cls.order_other = cls.env["sale.order"].create(
            {
                "partner_id": cls.env["res.partner"].create({"name": "Customer"}).id,
                "warehouse_id": cls.warehouse_other.id,
            }
        )
        cls.store_user = cls.env["res.users"].create(
            {
                "name": "Store user",
                "login": "store_user",
                "store_ids": [(6, 0, cls.store_own.ids)],
                "groups_id": [(6, 0, cls.env.ref("sales_team.group_sale_salesman_all_leads").ids)],
            }
        )

    def test_read_other_store_order_but_not_choose_or_edit_it(self):
        order = self.order_other.with_user(self.store_user)
        # Opening an order of another store by id works, as up to 16.0
        self.assertEqual(order.read(["name"])[0]["name"], self.order_other.name)
        # Searching orders stays filtered by store
        orders = self.env["sale.order"].with_user(self.store_user).search([])
        self.assertNotIn(self.order_other, orders)
        # Editing orders of another store stays forbidden
        with self.assertRaises(AccessError):
            order.write({"client_order_ref": "Not allowed"})
