from .. import db_configdb_type = db_config.DB_TYPEif db_type == 'sqlite':    from .sqlite import insertion_factory as factory_privateelif db_type == 'postgres':    from .postgres import insertion_factory as factory_private    class InsertionFactory():    @staticmethod    def insertion():        return factory_private.InsertionFactory().insertion()