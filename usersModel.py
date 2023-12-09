from pymongo import MongoClient, errors
from pymongo.errors import OperationFailure
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from dotenv import load_dotenv
import os
from InputValidator import email_validation
from InputValidator import password_validation
import hashlib


class UserNotFoundError(Exception):
    pass

def initializeUsers(url):
    #create a client
    try:
        client = MongoClient(url, server_api=ServerApi('1'))
        users_collection = client['users']['users'] #go in the users database and get the users collection
        
       
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
           
            #encode our email and passwords first
           email = email.encode('utf-8')
           password = password.encode('utf-8')
           #define our hasher:
           hasher = hashlib.sha512()
           #hash our email
           hasher.update(email)
           email = hasher.hexdigest()


           #hash our password
           hasher = hashlib.sha512()
           hasher.update(password)
           password = hasher.hexdigest()

 

            #insert user in database:
           db.insert_one({"email" : email, "password" : password})
           print("New User has been successfully added")
    except Exception as error:
        print("Error: ", error)

        
#to only be used in the login option
#TODO: hash the password
def findUser(db: Collection, email:str, password:str):
    try:
        #encode our email and passwords first
        email = email.encode('utf-8')
        password = password.encode('utf-8')
        #define our hasher:
        hasher = hashlib.sha512()
        #hash our email
        
        hasher.update(email)
        email = hasher.hexdigest()
        #reset the hasher
        hasher = hashlib.sha512()
        hasher.update(password)
        password = hasher.hexdigest()

      
        result = db.find_one({"email" : email, "password" : password})
        
        if result is None:
            raise UserNotFoundError("Email or password was incorrect")
    except Exception as error:
        print("Error: ", error)
    finally:
        return result

def findEmail(db: Collection, email: str):
    email = email.encode('utf-8')
    #define our hasher:
    hasher = hashlib.sha512()
    hasher.update(email)
    email = hasher.hexdigest()
    result = db.find_one({"email" : email})
    return result #let code continue if no email has been found