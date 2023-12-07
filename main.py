#storing the key
from cryptography.fernet import Fernet #to encrypt password
from InputValidator import *
from dotenv import load_dotenv
from passwordModel import *
from usersModel import *
import os
import pick



#initialize the .env variables
load_dotenv()
def user_selection(selected_index):
    users_collection=initializeUsers(url)
    match selected_index: #basically a switch statement
        case 0:
            try:
                login_email = getEmailInput()
                login_password = input("Please enter your password: ") #no need to bother the user with password requirements, so this is a simple input. When signing up the user is forced to pick a strong password anyway.
                print(findUser(users_collection, login_email, login_password))
            except Exception as e:
                print(e)
        case 1:
            signed_up = False
            while signed_up  != True:
              signed_up = sign_up(users_collection)


def sign_up(users_collection):
    signup_email = getEmailInput()
    signup_password = getPasswordInput()
    #Check if user is already in database
    result = findUser(users_collection, signup_email, signup_password)
    if result is None:
        insertUser(users_collection, signup_email, signup_password)
        return True
    else:
        print("Email has already been used for sign up, please try again")
        return False


#GET THE URL FROM ENVIRONMENT
# VARIABLES
url = os.getenv('ENV_URL_PRE')+os.getenv('ENV_PASSWORD')+os.getenv('ENV_URL_POST')
#Define the title using pick
prompt = "Welcome to the password manager! \n" + "Please select one of the following options: "
options = ['Log in', 'Sign up']
selected_option, selected_index = pick.pick(options, prompt)
os.system('cls||clear') #this clears the terminal, cls is for windows and clear is for linux
print("You have selected to", selected_option)
user_selection(selected_index)



#TODO: store the login information in a database
'''database = initialize(url, 'gamer')
email = getEmailInput()
pw = getPasswordInput()

insertPassword(database, email, pw)
'''
