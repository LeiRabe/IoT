from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import date
from datetime import timedelta
from django.contrib.auth import get_user_model
import psycopg2
from psycopg2 import Error
User = get_user_model()

# Create your views here.


#Page principal du site avec le login
def index(request):

    if request.method == 'POST':
        username = request.POST['username']  #récupération du username entré par l'utilisateur
        password = request.POST['password']  #récupération du password entré par l'utilisateur

        user = auth.authenticate(username = username, password =password  )     #authentification du user
        dateList=1
        if user is not None:          #si le user éxiste
            auth.login(request , user)

            #récupération des accès dans la bdd pour créer le graphique
            today = date.today()
            offset = (today.weekday()) % 7
            last_monday = today - timedelta(days=offset)
            try:
                connection = psycopg2.connect(user="postgres",
                                            password="docker",
                                            host="10.11.6.151",
                                            port="5432",
                                            database="iot")
                #cursor to perform database operations
                cursor = connection.cursor()
                query = "SELECT \"idPortique\", count(\"idPortique\") FROM public.\"Access\" where \"dateAccess\" = \'" + str(today)+"\' group by \"idPortique\" order by \"idPortique\" "
                cursor.execute(query)

                #fetch result 
                dateList = list(cursor.fetchall())
            except (Exception, Error) as error:
                print("Error while connecting to PostgreSQL", error)



            finally:
                if (connection):
                    print("connected to the pgsql db")

                """portique_acces_data = [
                    { "label": "Portique "+ str(dateList[0][1]), "y": dateList[0][1] },
                    { "label": "Portique 2", "y": dateList[1][1] },
                    { "label": "Portique 3", "y": dateList[2][1] },
                    { "label": "Portique 4", "y": dateList[3][1] },
                    { "label": "Portique 5", "y": dateList[4][1] },
                    { "label": "Portique 6", "y": dateList[5][1] }
                ]"""
                portique_acces_data = []
                i = 0
                for i in range(0, len(dateList)):     #ajout des données existante dans la bdd pour la journée en cours
                    portique_acces_data.append({ "label": "Portique "+ str(dateList[i][0]), "y": dateList[i][1] })
                

                return render(request, 'home.html', { "datelist":dateList[0][0] , "portique_acces_data" : portique_acces_data, "user":user })  #redirection vers /home pour afficher le graphique et le qrcode du user connecté

              
        else:
            messages.info(request, 'invalid username or password')
            return redirect("/")
    else:
        return render(request,'index.html')


def register(request):

    #récupération des données dans les champs du formulaire d'inscription
    if request.method == 'POST':

        email = request.POST['email']
        username = request.POST['username']
        password= request.POST['password']
        password= request.POST['password']
        lastname= request.POST['lastname']
        firstname= request.POST['firstname']
        gender= request.POST['gender']
        #enregistrement du user dans la bdd
        user = User.objects.create_user(username = username , password = password , email = email, gender = gender, firstname = firstname, lastname = lastname,last_login=date.today(), status ='élève', qrcode="4545445484")
        user.save()
        print('user created')
        return redirect('/custom')

    return render(request,'register.html')


def custom(request):
    return render(request, 'custom.html')


def home(request):
    return render(request, 'home.html')








