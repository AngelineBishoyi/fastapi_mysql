import mysql.connector

# Database connection configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "student"
}

def connect_to_database():
    return mysql.connector.connect(**db_config)

#conn=connect_to_database()
#mycursor=conn.cursor()
#mycursor.execute("CREATE TABLE std_games(game_id INT PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50) NOT NULL)")
#mycursor.execute("SHOW TABLES")
#for s in mycursor:
 #   print(s)
