from django.shortcuts import render,redirect
import pyrebase
from django.contrib.auth.decorators import login_required
from firebase_admin import auth
from firebase_admin.firestore import firestore
from django.http import HttpResponse
from google.cloud import firestore
from google.cloud import storage
from django.contrib import messages

 
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

def cart(request):
    return render(request, "tt365/cart.html")

def shipping(request):
    return render(request, "tt365/shipping.html")

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authe.sign_in_with_email_and_password(email, password)
        request.session['user_id'] = user['localId']
        return redirect('special_offer')
    else: 
        messages.error(request, 'Login failed. Please check your credentials.')
    return render(request, "tt365/login.html")
  

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authe.create_user_with_email_and_password(email=email,password=password)
        uid = user.get('uid')
        db = firestore.Client()
        # Create a collection named 'address' for each user using their ID
        address_ref = db.collection('users').document(uid).collection('address')

        # You can expand the address_data dictionary with other details
        address_data = {
            'email': email,
            'phone-number': request.POST.get('phone-number'),
            'fullname': request.POST.get('fullname'),
            # Add other user details as needed
        }

        address_ref.add(address_data)
        return redirect('login')
    else:
        print("not saved")      
    return render(request, "tt365/signup.html")


def admin_homepage(request):
    if request.method == 'POST':
        images = request.FILES.getlist('image')
        image_urls = []
        # Initialize the Google Cloud Storage client
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('ecommerce-e8ac5.appspot.com')
        for image in images:
            if image:
                blob = bucket.blob(f'products/images/{image.name}')
                blob.upload_from_file(image)
                image_urls.append(blob.public_url)
        name = request.POST.get('name')
        category = request.POST.get('category')
        description = request.POST.get('description')
        price = float(request.POST.get('price'))
        size = request.POST.get('size')
        color = request.POST.get('color')
        db = firestore.Client()
        # Create a Firestore document
        data = {
            'name': name,
            'category': category,
            'description': description,
            'price': price,
            'size': size,
            'color': color,
            'images': image_urls 
        }
        # Access the Firestore collection and add the data to it
        db.collection('products').add(data)
        return redirect('admin_homepage')
    return render(request, 'tt365/admin_homepage.html')


def special_offer(request):
    try:
        db = firestore.Client()
        products_ref = db.collection('products').where('category', '==', 'Men')  # Warning here
        query_result = products_ref.stream()

        # Create a list to store the product data (rename to avoid overwriting)
        products_data_list = []

        for product in query_result:
            product_dict = product.to_dict()
            # Ensure that each product has an 'id' attribute
            product_dict['id'] = product.id
            products_data_list.append(product_dict)

        return render(request, 'tt365/special_offer.html', {'products_data': products_data_list})

    except Exception as generic_error:
        print(f"An unexpected error occurred: {generic_error}")
        return HttpResponse("An unexpected error occurred. Please try again later.")


from google.cloud import firestore
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import auth as authe

def add_to_cart(request, product_id):
    try:
        db = firestore.Client()

        # Check if the user is authenticated
        if request.user.is_authenticated:
            user = request.user
            uid = user.uid
        else:
            # If not authenticated, you can handle it as needed (redirect to login, show an error, etc.)
            return HttpResponse("User not authenticated. Please log in.")

        if request.method == "POST":
            # Reference the user's document in the "users" collection
            user_ref = db.collection('users').document(uid)
            
            # Reference the "products" collection to retrieve product details
            product_ref = db.collection('products').document(product_id)
            product_data = product_ref.get().to_dict()

            if product_data:
                # Create a 'cart' collection within the user's document
                cart_ref = user_ref.collection('cart')
                
                # Check if the user has an existing cart
                existing_cart = cart_ref.stream()

                # Flag to check if the product is already in the cart
                product_in_cart = False

                for cart_item in existing_cart:
                    cart_item_data = cart_item.to_dict()

                    if cart_item_data['product_id'] == product_id:
                        # Product is already in the cart, update the quantity
                        cart_ref.document(cart_item.id).update({
                            'quantity': cart_item_data['quantity'] + 1
                        })
                        product_in_cart = True
                        break

                if not product_in_cart:
                    # Product is not in the cart, add it as a new item
                    cart_ref.add({
                        'product_id': product_id,
                        'quantity': 1,
                        'price': product_data.get('price', 0)  # Set the price from product data if available
                    })
        return redirect('special_offer')

    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponse("An error occurred while processing your request.")
