#storing the key
from cryptography.fernet import Fernet #to encrypt password
from InputValidator import *
from dotenv import load_dotenv
from passwordModel import *
from usersModel import *
import os
import pick
from User import User


#initialize the .env variables
load_dotenv()
currentUser = None
def startup_selection(selected_index):
    users_collection=initializeUsers(url)
    match selected_index: #basically a switch statement
        case 0:
            try:
                login_email = getEmailInput()
                login_password = input("Please enter your password: ") #no need to bother the user with password requirements, so this is a simple input. When signing up the user is forced to pick a strong password anyway.
                result = findUser(users_collection, login_email, login_password)
                if (result):#If a match was found
                    
                    currentUser = User(login_email,login_password)
                   #search for a collection in the passwords database that corresponds to the users ID
                    pw_db = initialize(url, 'passwords')
                    print(pw_db)
                    print()
                    pw_collection = pw_db[str(result["_id"])] #create/select a collection that corresponds to the user ID
                    picked_action = user_selection()
                    user_action(picked_action, pw_collection)
            except Exception as e:
                print(e)
        case 1:
            signed_up = False
            while signed_up  != True:
              signed_up = sign_up(users_collection)



def user_action(action, collection: Collection): #do an action on the collection basically
    #clear the terminal
    os.system('cls||clear')
    match action:
        case 0:
            newly_added_email = getEmailInput()
            newly_added_password = getPasswordInput()
            insertPassword(collection, newly_added_email, newly_added_password)
        case 1:
            print("test1")
        case 2:
            allpw = getPasswords(collection)
            for pw in allpw:
                print("Email: " + pw['email'] + "\t Password: " + pw['password'])

def user_selection():
    prompt = "What do you want to do? "
    options = ['Add an account credentials', 'Delete an account credentials', 'View all credentials']
    selected_option, selected_index = pick.pick(options, prompt)
    return selected_index


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
startup_selection(selected_index)



#TODO: store the login information in a database
'''database = initialize(url, 'gamer')
email = getEmailInput()
pw = getPasswordInput()

insertPassword(database, email, pw)
'''
