from pymongo import MongoClient, errors
from pymongo.errors import OperationFailure
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from InputValidator import email_validation
from InputValidator import password_validation



def initialize(url, database_name):
    #create a client
    try:
        client = MongoClient(url, server_api=ServerApi('1'))
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        db = client[database_name]
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
        return db




def insertPassword(db, email: str, password: str):
    try:
       if (email_validation(email) and password_validation(password)):
           collection =  db['test']
           collection.insert_one({"email" : email, "password" : password})
           print("gamer")
    except Exception as error:
        print("Error: ", error)


