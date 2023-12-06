#storing the key
from cryptography.fernet import Fernet #to encrypt password
from InputValidator import *
from dotenv import load_dotenv
from passwordModel import *
from usersModel import *
import os


#initialize the .env variables
load_dotenv()





try:
    key_file = open("key.txt")
except FileNotFoundError as e:


    key = Fernet.generate_key()
    key_file = open("key.txt" , "w")
    key_file.write(key)
    key_file.close()




#GET THE URL FROM ENVIRONMENT VARIABLES
url = os.getenv('ENV_URL_PRE')+os.getenv('ENV_PASSWORD')+os.getenv('ENV_URL_POST')
print(url)


print("Welcome to the password manager!")
print("Please log in to continue")
try:
    loginEmail = getEmailInput()
    loginPassword = input("Please enter your password: ") #no need to bother the user with password requirements, so this is a simple input. When signing up the user is forced to pick a strong password anyway.
    usersCollection=initializeUsers(url)
    print(findUser(usersCollection, loginEmail, loginPassword))
except Exception as e:
    print(e)




#TODO: store the login information in a database
'''database = initialize(url, 'gamer')
email = getEmailInput()
pw = getPasswordInput()

insertPassword(database, email, pw)
'''
