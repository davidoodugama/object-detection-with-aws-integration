import pymysql
HOST = "database-1.cyilbbylotha.us-east-2.rds.amazonaws.com"
USER = "dtvDB"
PASS = "dtvpassword"
db = pymysql.connect(host = HOST, user = USER, password = PASS)

cursor = db.cursor() # To execute sql queries