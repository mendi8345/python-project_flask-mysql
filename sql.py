import mysql.connector
from mysql.connector import errorcode


class Database(object):
    def __init__(self, db_local):
        self.result_set = None
        self.db_local = db_local
        self.db_conn = None
        self.db_cursor = None

    def __enter__(self):
        # This ensure, whenever an object is created using "with"
        # this magic method is called, where you can create the connection.
        self.db_conn = mysql.connector.connect(**self.db_local)
        self.db_cursor = self.db_conn.cursor()
        return self

    def __exit__(self, exception_type, exception_val, trace):
        # once the with block is over, the _exit_ method would be called
        # with that, you close the connnection
        try:
            self.db_cursor.close()
            self.db_conn.close()
        except AttributeError:  # isn't closable
            print('Not closable.')
            return True  # exception handled successfully

    def get_row(self, sql, data=None):
        if data is None:
            self.db_cursor.execute(sql)
        else:
            self.db_cursor.execute(sql, data)
        # self.result_set = self.db_cursor.fetchall()
        self.result_set = [dict((self.db_cursor.description[i][0], value)
                                for i, value in enumerate(row)) for row in self.db_cursor.fetchall()]
        return self.result_set

    def insert_row(self, sql_query, data=None):
        if data is None:
            self.db_cursor.execute(sql_query)
        else:
            self.db_cursor.execute(sql_query, data)
        self.result_set = self.db_cursor.lastrowid
        self.db_conn.commit()
        return self.result_set

    def execute(self, sql_query, data=None):
        if data is None:
            self.db_cursor.execute(sql_query)
        else:
            self.db_cursor.execute(sql_query, data)
        self.db_conn.commit()
        return


db_config = {
    'user': 'root',
    'password': '12345',
    'host': 'localhost',
    # 'database': 'tes',
    'port': '3306'
}

sql = "SELECT * FROM mytest LIMIT 10"

add_product = ("INSERT INTO product "
               "(product_id, title, price, source) "
               "VALUES (%s, %s, %s, %s)")

add_user = ("INSERT INTO users "
            "(email_address) "
            "VALUES (%s)")

user_to_prod = ("INSERT INTO user_product "
                "(user_id, prod_id) "
                "VALUES (%s, %s)")

prod_by_id = ("SELECT product_id, title, price, source  FROM product "
              "WHERE product_id = %s")

user_by_email = ("SELECT * FROM users "
                 "WHERE email_address = %s")

user_products_query = ("SELECT product_id, title, price, source  FROM product "
                       "WHERE product_id in (select prod_id from user_product where user_product.user_id =  %s)")

DB_NAME = 'test5'

TABLES = {'product': (
    "CREATE TABLE `product` ("
    "  `id` int auto_increment primary key,"
    "  `product_id` nvarchar(40),"
    "  `title` varchar(200) NOT NULL,"
    "  `price` varchar(10) NOT NULL,"
    "  `source` varchar(20)"
    ") ENGINE=InnoDB"), 'users': (
    "CREATE TABLE `users` ("
    "  `user_id` int AUTO_INCREMENT primary key,"
    "  `email_address` nvarchar(40) NOT NULL"
    ") ENGINE=InnoDB"), 'user_product': (
    "CREATE TABLE `user_product` ("
    "  `user_id` int NOT NULL,"
    "  `prod_id` nvarchar(40) NOT NULL"
    ") ENGINE=InnoDB")}


def create_database():
    try:
        with Database(db_config) as test:
            test.execute(f"CREATE DATABASE {DB_NAME}")
            db_config['database'] = DB_NAME
            # test.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            print(" creating database")

    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def seed_db():
    try:
        with Database(db_config) as test:
            test.execute("USE {}".format(DB_NAME))
            db_config['database'] = DB_NAME
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database()
            print("Database {} created successfully.".format(DB_NAME))

        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            with Database(db_config) as test:
                test.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


seed_db()
# cursor.close()
# mydb.close()
