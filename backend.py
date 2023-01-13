#server backend
#todo:
# [X] connect with the db
# [] manage the messages [idUser(parsed from the QRCode):Date:idPortique] from the capteur:
    # [X] query the db: 
    #   [X] if the idUser is in the db -> Insert the ACCESS table
    #   [X] if the row has been INSERTED int doorStatus is 1 if open and 0 if closed -> id user found: doorStatus = 1 
import psycopg2
from psycopg2 import Error
import mqttSubscriber as sub

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
# MQTT SUBSCRIBE 
sub.run()
msg = sub.retrieveMsg()

#parse msg
msgArray = msg.split(",")
qrcode = str(msgArray[0])
idPortique = msgArray[2]
dateAccess = msgArray[1]

#door status
doorStatus = 0;

# verify if there's a user associated with the qrcode
queryUser = ("SELECT \"idUser\" FROM public.\"User\" WHERE  qrcode = " + "\'" +qrcode+ "\'")
cursor.execute(queryUser)
exists = str(cursor.fetchone())
print("Row count "+str(cursor.rowcount))
if(cursor.rowcount>0):
    print("Exists: " + exists)
    queryInsert = ("INSERT INTO public.\"Access\"(\"idUser\", \"idPortique\", \"dateAccess\") VALUES (%s,%s,%s)")
    record_to_insert = (1,idPortique,"\'" + dateAccess + "\'" )
    print(queryInsert)
    try:
        cursor.execute(queryInsert,record_to_insert)
        connection.commit()
        count = cursor.rowcount
        if(count>0):
            doorStatus = 1;
            print("Inserted! Now the door is: " + str(doorStatus))

    except (Exception, Error) as error:
        print("Error while trying to insert", error)

#Send information to the broker