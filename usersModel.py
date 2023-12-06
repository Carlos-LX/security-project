from pymongo import MongoClient, errors
from pymongo.errors import OperationFailure
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from dotenv import load_dotenv
import os
from InputValidator import email_validation
from InputValidator import password_validation


def initializeUsers(url):
    #create a client
    try:
        client = MongoClient(url, server_api=ServerApi('1'))
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        users_collection = client['users']['users'] #go in the users database and get the users collection
        print("Connected to MongoDb")
        
       
    except errors.ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
    except OperationFailure as e:
        print(f"MongoDB operation failed: {e}")
        if 'bad auth' in str(e):
            print("Authentication failed. Check your credentials.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        return users_collection



#to only be used when a user is signed up
#TODO: hash the password
def insertUser(db: Collection , email: str, password: str):
    try:
       if (email_validation(email) and password_validation(password)):
           db.insert_one({"email" : email, "password" : password})
           print("added a new user")
    except Exception as error:
        print("Error: ", error)

#to only be used in the login option
#TODO: hash the password
def findUser(db: Collection, email:str, password:str):
    try:
        result = db.find_one({"email" : email, "password" : password})
        if result is None:
            raise Exception("Could not find user in database")
    except Exception as error:
        print("Error: ", error)


