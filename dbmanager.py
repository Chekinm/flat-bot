import psycopg2
from psycopg2 import sql


class DBconnect():
    """class to work with database"""
    """instance of class is a database, with connection as property"""

    def __init__(self, **DB_CONFIG):
        """create an instance of connection to the database
        will be none if there some poblem with DB"""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.connection.autocommit = True
            with self.connection.cursor() as cursor:
                cursor.execute(open('./tables_create.sql', 'r').read())
        except psycopg2.OperationalError as error:
            self.connection = None
            print(error)

    def run_change_query(self, query) -> bool:
        """function runs change query, return True if change done
        succesefully, otherwise return False
        inside it check if id already exist and update
        existing record with new values"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                # self.commit()
        except psycopg2.OperationalError as er:
            print(str(er))
            return False
        return True

    async def add_user(self, user_id: str) -> bool:
        """function create user with default values"""
        query = f"INSERT INTO request_data (telegram_id) VALUES('{user_id}') ON CONFLICT (telegram_id) DO NOTHING;"
        return self.run_change_query(query)

    async def db_change_coordinates(self,
                                    latitude,
                                    longitude,
                                    user_id) -> bool:
        """function changes the coordinates to search to desired"""
        query = f"UPDATE request_data SET latitude = {latitude}, longitude={longitude}  WHERE telegram_id = '{user_id}'"
        return self.run_change_query(query)

    async def change_properties(self, query, user_id) -> bool:
        """function changes the properties  to desired"""
        print(query)
        query = f"UPDATE request_data SET {query[0]}={query[1]}  WHERE telegram_id = '{user_id}'"
        return self.run_change_query(query)

    async def get_request_data(self, user_id: str):
        """get request datafrom DB by used_id"""
        with self.connection.cursor() as cursor:
            query = sql.SQL("""SELECT * FROM request_data WHERE telegram_id = {0}""").format(sql.Literal(user_id))
            cursor.execute(query)
            res = cursor.fetchall()
            return res[0] if res else []

    def _display_tables_names(self):
        '''lookup for table names, not need outside'''
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'""")
            return cursor.fetchall()
