#server backend
#todo:
# - connect with the db
# - manage the messages [idUser(parsed from the QRCode):Date:idPortique] from the passerelle:
    # - query the db: 
    #   - if the idUser is in the db -> Insert the ACCESS table
    #   - if the row has been INSERTED int doorStatus is 1 if open and 0 if closed -> id user found: doorStatus = 1 
import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="postgres",
                                  password="docker",
                                  host="10.11.6.151",
                                  port="5432",
                                  database="iot")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        print("connected to the pgsql db")