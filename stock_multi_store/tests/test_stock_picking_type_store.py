from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestStockPickingTypeStore(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.store_own = cls.env["res.store"].create({"name": "Own store"})
        cls.store_other = cls.env["res.store"].create({"name": "Other store"})
        cls.warehouse_other = cls.env["stock.warehouse"].create(
            {"name": "Other store warehouse", "code": "OSW", "store_id": cls.store_other.id}
        )
        cls.picking_other = cls.env["stock.picking"].create(
            {
                "picking_type_id": cls.warehouse_other.out_type_id.id,
                "location_id": cls.warehouse_other.lot_stock_id.id,
                "location_dest_id": cls.env.ref("stock.stock_location_customers").id,
            }
        )
        cls.store_user = cls.env["res.users"].create(
            {
                "name": "Store user",
                "login": "store_user",
                "store_ids": [(6, 0, cls.store_own.ids)],
                "groups_id": [(6, 0, cls.env.ref("stock.group_stock_user").ids)],
            }
        )

    def test_read_other_store_picking_type_but_not_choose_or_edit_it(self):
        picking = self.picking_other.with_user(self.store_user)
        # Opening a transfer of another store reads its operation type, as up to 16.0
        self.assertEqual(picking.picking_type_id.display_name, self.warehouse_other.out_type_id.display_name)
        # Choosing operation types stays filtered by store
        picking_types = self.env["stock.picking.type"].with_user(self.store_user).search([])
        self.assertNotIn(self.warehouse_other.out_type_id, picking_types)
        # Editing transfers of another store stays forbidden
        with self.assertRaises(AccessError):
            picking.write({"origin": "Not allowed"})
