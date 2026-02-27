from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    domain_force = (
        "['|', ('picking_type_id.code', '=', 'dropship'), "
        "'|', ('picking_type_id.warehouse_id', '=', False), "
        "'|', ('picking_type_id.warehouse_id.store_id', '=', False), "
        "('picking_type_id.warehouse_id.store_id', 'child_of', "
        "user.store_ids.ids)]"
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_rule rule
           SET domain_force = %s
          FROM ir_model_data data
         WHERE data.model = 'ir.rule'
           AND data.module = 'stock_multi_store'
           AND data.name = 'stock_picking_store_rule'
           AND data.res_id = rule.id
        """,
        (domain_force,),
    )
