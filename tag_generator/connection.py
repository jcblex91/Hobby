import pymysql
import config as cfg

# Open database connection
db = pymysql.connect(cfg.mysql['host'],cfg.mysql['user'],cfg.mysql['password'], cfg.mysql['db'])

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Database version : %s " % data)

# disconnect from server
db.close()
