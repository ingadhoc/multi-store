from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr, 'account_multi_store', 'migrations/11.0.1.2.0/mig_data.xml')
