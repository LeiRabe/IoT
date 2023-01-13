#server backend
#todo:
# [X] connect with the db
# [] manage the messages [idUser(parsed from the QRCode):Date:idPortique] from the capteur:
    # [] query the db: 
    #   [] if the idUser is in the db -> Insert the ACCESS table
    #   [] if the row has been INSERTED int doorStatus is 1 if open and 0 if closed -> id user found: doorStatus = 1 
import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="postgres",
                                  password="docker",
                                  host="10.11.6.151",
                                  port="5432",
                                  database="iot")
    #cursor to perform database operations
    cursor = connection.cursor()
    query = "SELECT qrcode FROM public.\"User\""
    cursor.execute(query);

    #fetch result 
    qrcodeList = list(cursor.fetchall())
    print(qrcodeList)


except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)



finally:
    if (connection):

        print("connected to the pgsql db")

# simulation message received
msg = '454544,2021-12-01,1'

#parse msg
msgArray = msg.split(",")
qrcode = str(msgArray[0])
idPortique = str(msgArray[2])
dateAccess = str(msgArray[1])
print("The user with " + qrcode + " enters the portique n" + idPortique + " the " + dateAccess)
