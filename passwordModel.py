from pymongo import MongoClient, errors, cursor
from pymongo.collection import Collection
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
        db = client[database_name]
        
       
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




def insertPassword(collection: Collection, email: str, password: str): #option 0 in passwords menu
    try:
           collection.insert_one({"email" : email, "password" : password})
           print("Successfully added details to database")
    except Exception as error:
        print("Error: ", error)
        
        
def deletePassword(collection: Collection, document: dict):
    try:
        collection.delete_one(document)
        print("Successfully deleted credentials from database")
    except Exception as error:
        print("Error: ", error)
        

def getPasswords(collection: Collection) -> cursor.Cursor: #option 2
    return collection.find()

