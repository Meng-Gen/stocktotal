import postgresql



class Query():

    def __init__(self):
        self.CONN_STRING = 'pq://stocktotal:stocktotal@localhost:5432/stocktotal'
        self.DB_CONN = None
        
    def open(self):
        self.DB_CONN = postgresql.open(self.CONN_STRING)
        
    def close(self):
        self.DB_CONN.close()
        self.DB_CONN = None
