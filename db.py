import pymongo
from flask import request
from urllib.parse import quote_plus

# Properly escape username and password using quote_plus
username = 'Geotech'  # Replace with your actual username
password = '@Locamade12182'  # Replace with your actual password

uri = f'mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@cluster0.r8itkxl.mongodb.net/?retryWrites=true&w=majority'

client = pymongo.MongoClient(uri)
userdb = client['userdb']
users = userdb.customers


def create_collections():
    # Check if the collection exists
    if 'customers' not in userdb.list_collection_names():
        userdb.create_collection('customers')


def insert_data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']

        reg_user = {
            'name': name,
            'email': email,
            'password': password
        }

        if users.find_one({"email": email}) is None:
            users.insert_one(reg_user)
            return True
        else:
            return False


def check_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        user = {
            "email": email,
            "password": password
        }

        user_data = users.find_one(user)
        if user_data is None:
            return False, ""
        else:
            return True, user_data["name"]


# Ensure collections exist before interacting with them
create_collections()
