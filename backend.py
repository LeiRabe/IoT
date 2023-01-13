#Useful import
# module: database adapter 
import psycopg2
from psycopg2 import Error
# the Mqtt subscriber file
import mqttSubscriber as sub

try:
    # creation of a connection
    connection = psycopg2.connect(user="postgres",
                                  password="docker",
                                  host="10.11.6.151",
                                  port="5432",
                                  database="iot")
    # cursor to perform database operations
    cursor = connection.cursor()

    # the query to be executed: retrieve all the QR code within the db
    query = "SELECT qrcode FROM public.\"User\""

    # executing the query
    cursor.execute(query);

    #fetch result 
    qrcodeList = list(cursor.fetchall())
    print(qrcodeList)

# handling exception
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

# default behaviour after the try scope
finally:
    if (connection):
        print("connected to the pgsql db")

# --- MQTT SUBSCRIBE ---
# sub.run() 
# simulation received message 
msg = "454544,2021-12-01,1"

#parse msg
msgArray = msg.split(",")
qrcode = str(msgArray[0])
idPortique = msgArray[2]
dateAccess = msgArray[1]

#door statu: remain closed
doorStatus = 0;

# verify if there's a user associated with the qrcode
queryUser = ("SELECT \"idUser\" FROM public.\"User\" WHERE  qrcode = " + "\'" +qrcode+ "\'")
cursor.execute(queryUser)
exists = str(cursor.fetchone())
print("Row count "+str(cursor.rowcount))

# verify if any rows have been fetched
if(cursor.rowcount>0):
    print("Exists: " + exists)

    # insertion query
    queryInsert = ("INSERT INTO public.\"Access\"(\"idUser\", \"idPortique\", \"dateAccess\") VALUES (%s,%s,%s)")
    # values to be inserted
    record_to_insert = (5,idPortique,"\'" + dateAccess + "\'" )
    print(queryInsert)
    
    try:
        # execute the insertion query
        cursor.execute(queryInsert,record_to_insert)
        # commit it to the db
        connection.commit()
        # returned rows: the one that should have been inserted
        count = cursor.rowcount

        # if inserted then open the door: doorStatus: 1
        if(count>0):
            doorStatus = 1;
            print("Inserted! Now the door is: " + str(doorStatus))

    # exception handling
    except (Exception, Error) as error:
        print("Error while trying to insert", error)

#Send information to the broker
# to do
# [] Publish the doorState to the broker