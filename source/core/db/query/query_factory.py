# coding: utf-8

from .. import db_config

db_type = db_config.DB_TYPE

if db_type == 'sqlite':
    from .sqlite import query_factory as factory_private
elif db_type == 'postgres':
    from .postgres import query_factory as factory_private
   
class QueryFactory():
    @staticmethod
    def stock_code_query():
        return factory_private.QueryFactory().stock_code_query()                
