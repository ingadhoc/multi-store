##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAccountJournalSearch(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Archived Journal",
                "code": "ARCHJ",
                "type": "general",
            }
        )
        cls.journal.active = False

    def test_archived_journal_not_returned_by_plain_search(self):
        journals = self.env["account.journal"].search([("code", "=", "ARCHJ")])
        self.assertNotIn(self.journal, journals)

    def test_archived_journal_returned_when_explicitly_asked_for(self):
        by_domain = self.env["account.journal"].search([("code", "=", "ARCHJ"), ("active", "=", False)])
        self.assertIn(self.journal, by_domain)
        by_context = self.env["account.journal"].with_context(active_test=False).search([("code", "=", "ARCHJ")])
        self.assertIn(self.journal, by_context)
