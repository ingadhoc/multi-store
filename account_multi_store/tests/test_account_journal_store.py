from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.exceptions import AccessError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAccountJournalStore(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        company = cls.company_data["company"]
        cls.store_own = cls.env["res.store"].create({"name": "Own store", "company_id": company.id})
        cls.store_other = cls.env["res.store"].create({"name": "Other store", "company_id": company.id})
        # The user that sets up the data works on every store
        cls.env.user.store_ids = cls.store_own | cls.store_other
        cls.journal_other = cls.company_data["default_journal_sale"].copy(
            {"name": "Other store sales", "code": "OSS", "store_id": cls.store_other.id}
        )
        cls.invoice_other = cls.init_invoice(
            "out_invoice", products=cls.product_a, journal=cls.journal_other, post=True
        )
        cls.store_user = cls.env["res.users"].create(
            {
                "name": "Store user",
                "login": "store_user",
                "company_id": company.id,
                "company_ids": [(6, 0, company.ids)],
                "store_ids": [(6, 0, cls.store_own.ids)],
                "groups_id": [(6, 0, cls.env.ref("account.group_account_invoice").ids)],
            }
        )

    def test_read_other_store_journal_but_not_choose_or_edit_it(self):
        invoice = self.invoice_other.with_user(self.store_user)
        # Opening an entry of another store reads its journal, as up to 16.0
        self.assertEqual(invoice.journal_id.display_name, self.journal_other.display_name)
        invoice.read(["name", "journal_id", "amount_total"])
        # Choosing journals stays filtered by store
        journals = self.env["account.journal"].with_user(self.store_user).search([])
        self.assertNotIn(self.journal_other, journals)
        # Editing entries of another store stays forbidden
        with self.assertRaises(AccessError):
            invoice.write({"ref": "Not allowed"})
