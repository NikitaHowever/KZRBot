import pyodbc

class DataBase:
    def __init__(self):
        self.conn_string = "Driver={ODBC Driver 17 for SQL Server};SERVER=217.107.219.93;DATABASE=KZRBotDb;UID=SA;PWD=Wsr12345678;"
        self.conn = None

        self._init_connection()


        
    

    def _init_connection(self):
        self.conn = pyodbc.connect(self.conn_string)

    @property
    def get_conn(self):
        return self.conn    
