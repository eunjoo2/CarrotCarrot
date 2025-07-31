import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.0.56",
  user="root",
  password="0000",
  database="carot"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM user")

myresult = mycursor.fetchall()

print(myresult)