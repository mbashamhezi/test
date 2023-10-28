from django.shortcuts import render,redirect
import pyrebase
from firebase_admin import auth
from firebase_admin.firestore import firestore
from django.http import HttpResponse, JsonResponse
from google.cloud import firestore
from google.cloud import storage


 
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


def index(request):
    return render(request, "tt365/index.html")

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authe.sign_in_with_email_and_password(email, password)
        session_id = user['idToken']
        request.session['uid']=str(session_id)
        return redirect('index')
    else:
        print("Invalid credentials")      
    return render(request, "tt365/login.html")


        # try:
        #     user = authe.sign_in_with_email_and_password(email, password)
        #     session_id=user['idToken']
        #     request.session['uid']=str(session_id)
        # except auth.InvalidIdTokenError:
        #     message="Invalid Credentials!!Please ChecK your Data"
        #     return render(request,"tt365/login.html",{"message":message})
        # except Exception as e:
        #     # Handle other exceptions as needed
        #     message = f"An error occurred: {str(e)}"
        #     return render(request, "login.html", {"message": message})

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


def cart(request):
    return render(request, "tt365/cart.html")

def admin_homepage(request):
    return render(request, "tt365/admin_homepage.html")

def shipping(request):
    return render(request, "tt365/shipping.html")







import os




def admin_homepage(request):

    # print(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category = request.POST.get('category')
        description = request.POST.get('description')
        price = float(request.POST.get('price'))
        size = request.POST.get('size')
        color = request.POST.get('color')
        image = request.FILES.get('image')

        if image:
            storage_client = storage.Client()
            bucket = storage_client.get_bucket('gs://ecommerce-e8ac5.appspot.com')

            image_filename = f"{product_name}_{image}"

              # Upload the image to the storage bucket
            blob = bucket.blob(image_filename)
            blob.upload_from_string(image.read(), content_type=image.content_type)

            # Get the download URL of the uploaded image
            image_url = blob.public_url
       
        # You can add code here to upload the image to a storage service
        # (e.g., Firebase Storage) and get the download URL, or you can directly save the image as base64 in Firestore.

        # Initialize the Firestore client
        db = firestore.Client()

        # Create a Firestore document
        data = {
            'product_name': product_name,
            'category': category,
            'description': description,
            'price': price,
            'size': size,
            'color': color,
            'image': image_url,
        }

        # Access the Firestore collection and add the data to it
        doc_ref = db.collection('products').add(data)

        return redirect('admin_homepage')

        # return HttpResponse(f'Data added to Firestore with ID: {doc_ref}')

    return render(request, 'tt365/admin_homepage.html')
