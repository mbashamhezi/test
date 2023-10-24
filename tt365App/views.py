from django.shortcuts import render,redirect
import pyrebase
from firebase_admin import auth
# from firebase_admin.auth import AuthError



 
config = {
  "apiKey": "AIzaSyAIWJEa4__8OmcCygd7mYXEAd2YIWDQjbA",
  "authDomain": "ecommerce-e8ac5.firebaseapp.com",
  "projectId": "ecommerce-e8ac5",
  "storageBucket": "ecommerce-e8ac5.appspot.com",
  "messagingSenderId": "431645281470",
  "appId": "1:431645281470:web:9a4dda1b6ef40f1db362ef",
    "databaseURL": ""
}

#  Initialising database,auth and firebase for further use 
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()


# Create your views here.

def index(request):
    return render(request, "tt365/index.html")

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            session_id=user['idToken']
            request.session['uid']=str(session_id)
        except auth.InvalidIdTokenError:
            message="Invalid Credentials!!Please ChecK your Data"
            return render(request,"login",{"message":message})
        except Exception as e:
            # Handle other exceptions as needed
            message = f"An error occurred: {str(e)}"
            return render(request, "login.html", {"message": message})

    return render(request, "tt365/login.html")

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authe.create_user_with_email_and_password(email=email,password=password)
        uid = user['localId']
        print(uid)
        return redirect('login')
    else:
        print("not saved")      
    return render(request, "tt365/signup.html")


def men_fashion(request):
    return render(request, "tt365/men_fashion.html")

def women_fashion(request):
    return render(request, "tt365/women_fashion.html")

def kids_fashion(request):
    return render(request, "tt365/kids_fashion.html")

def cart(request):
    return render(request, "tt365/cart.html")

def admin_homepage(request):
    return render(request, "tt365/admin_homepage.html")

def shipping(request):
    return render(request, "tt365/shipping.html")