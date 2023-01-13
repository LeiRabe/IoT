#Script for sample data insertion

#Connection 
import psycopg2
from psycopg2 import Error

try:
    #connection creation
    connection = psycopg2.connect(user="postgres",
                                  password="docker",
                                  host="10.11.6.151",
                                  port="5432",
                                  database="iot")
    #cursor to perform database operations
    cursor = connection.cursor()
    query = "INSERT INTO public.\"Portique\"" + " (\"idPortique\", \"nomBat\") VALUES (%s, %s);"
    valuesToInsert = [
        (2,"Batiment 2"),
        (3,"Batiment 3"),
        (4,"Batiment 4"),
        (5,"Batiment 5"),
        (6,"Batiment 6"),
        
    ]
    #execute several queries at the same time: several input
    cursor.executemany(query,valuesToInsert);

    #commit to the db
    connection.commit

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)


finally:
    if (connection):

        print("connected to the pgsql db")
