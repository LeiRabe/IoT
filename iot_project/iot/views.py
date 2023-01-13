from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import date
from django.contrib.auth import get_user_model
import psycopg2
from psycopg2 import Error
User = get_user_model()

# Create your views here.



def index(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password =password  )
        dateList=1
        if user is not None:
            auth.login(request , user)
            try:
                connection = psycopg2.connect(user="postgres",
                                            password="docker",
                                            host="10.11.6.151",
                                            port="5432",
                                            database="iot")
                #cursor to perform database operations
                cursor = connection.cursor()
                query = "SELECT dateAccess FROM public.\"Access\""
                cursor.execute(query)

                #fetch result 
                dateList = list(cursor.fetchall())
            except (Exception, Error) as error:
                print("Error while connecting to PostgreSQL", error)



            finally:
                if (connection):
                    print("connected to the pgsql db")

            scooter_production_data = [
                { "label": "12-01-2000", "y": 605 },
                { "label": "12-01-2000", "y": 805 },
                { "label": "12-01-2000", "y": 655 },
                { "label": "12-01-2000", "y": 75 },
                { "label": "12-01-2000", "y": 205 },
                { "label": "12-01-2000", "y": 55 },
                { "label": "12-01-2000", "y": 105 }
            ]
            motorcycle_production_data = [
                { "label": "12-01-2000", "y": 620 },
                { "label": "12-01-2000", "y": 711 },
                { "label": "12-01-2000", "y": 6503 },
                { "label": "12-01-2000","y": 679 },
                { "label": "12-01-2000", "y": 844 },
                { "label": "12-01-2000", "y": 1011 },
                { "label": "12-01-2000", "y": 19 }
            ]
            
            return render(request, 'home.html', { "dateList":'a' , "scooter_production_data" : scooter_production_data, "motorcycle_production_data": motorcycle_production_data, "user":user }) 

              
        else:
            messages.info(request, 'invalid username or password')
            return redirect("/")
    else:
        return render(request,'index.html')


def register(request):

    if request.method == 'POST':

        email = request.POST['email']
        username = request.POST['username']
        password= request.POST['password']
        password= request.POST['password']
        lastname= request.POST['lastname']
        firstname= request.POST['firstname']
        gender= request.POST['gender']

        user = User.objects.create_user(username = username , password = password , email = email, gender = gender, firstname = firstname, lastname = lastname,last_login=date.today(), status ='élève', qrcode="4545445484")
        user.save()
        print('user created')
        return redirect('/custom')

    return render(request,'register.html')


def custom(request):
    return render(request, 'custom.html')


def home(request):
    return render(request, 'home.html')








