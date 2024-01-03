#storing the key
from cryptography.fernet import Fernet #to encrypt password
from InputValidator import *
from dotenv import load_dotenv
from passwordModel import *
from usersModel import *
import os
import pick
from User import User
import base64


#initialize the .env variables
load_dotenv()
currentUser = None

def encrypt_details(key, email, password, service):
    cipher = Fernet(key)
    encrypted_email = (cipher.encrypt(email.encode())).decode() #Gotta use decode because cipher.encrypt returns bytes.
    encrypted_password = (cipher.encrypt(password.encode())).decode()
    encrypted_service = (cipher.encrypt(service.encode())).decode()
    return encrypted_email, encrypted_password, encrypted_service



def decrypt_details(key, enc_email, enc_password, enc_service):
    cipher = Fernet(key)
    decrypted_email = cipher.encrypt(enc_email).decode()
    decrypted_password = cipher.encrypt(enc_password).decode()
    decrypted_service = cipher.encrypt(enc_service).decode()
    
    return decrypted_email, decrypted_password, decrypted_service

def startup_selection(selected_index):
    currentUser = None
    if selected_index == 2:
        exit()
    users_collection=initializeUsers(url)
    while selected_index != 2:
        match selected_index: #basically a switch statement
            case 0:
                try:
                    
                    if currentUser is None: #if any error is thrown while adding/deleting or reading all account credentials then user will not be logged out
                        login_email = getEmailInput()
                        login_password = input("Please enter your password: ") #no need to bother the user with password requirements, so this is a simple input. When signing up the user is forced to pick a strong password anyway.
                        result = findUser(users_collection, login_email, login_password)
                        if (result):#If a match was found
                            picked_action = None
                            currentUser = User(login_email,login_password)
                    #search for a collection in the passwords database that corresponds to the users ID
                    pw_db = initialize(url, 'passwords')
                    pw_collection = pw_db[str(result["_id"])] #create/select a collection that corresponds to the user ID
                    while picked_action != 3:
                        picked_action = user_selection()
                        user_action(currentUser, picked_action, pw_collection)
                    if picked_action == 3:
                        currentUser = None
                        break
                      

                except Exception as e:
                    print("An error has occurred:" + str(e))
                    input("Press enter to return to menu ") #wait for the user to input
                    break
            case 1:
                signed_up = False
                while signed_up  != True:
                    signed_up = sign_up(users_collection)
                break
            case 2:
                exit()

def get_details_and_encrypt(details_key):
            newly_added_email, newly_added_password, newly_added_service = getDetailsInput()
            encrypted_email, encrypted_password, encrypted_service = encrypt_details(details_key,newly_added_email, newly_added_password, newly_added_service)
            return encrypted_email, encrypted_password, encrypted_service

def user_action(user : User, action, collection: Collection): #do an action on the collection basically
    #clear the terminal
        os.system('cls||clear')

        if (action == 0):
                encrypted_email, encrypted_password, encrypted_service = get_details_and_encrypt(user.generateKey())
                insertDetails(collection, encrypted_email, encrypted_password, encrypted_service)
        elif (action == 1):
                details_key = user.generateKey()
                allpw = getPasswords(collection)
                length = collection.count_documents({}) #get the length of the collection
                options_list = []
                if length > 0:
                    for pw in allpw:
                        decrypted_email, decrypted_password, decrypted_service = decrypt_details(details_key, pw['email'], pw['password'], pw['service'])
                        options_list.append("Email: " + decrypted_email + " Password: " + decrypted_password + " Service: " + decrypted_service)
                    prompt = "Select an account to delete:"
                    selected_option, selected_index = pick.pick(options_list, prompt)
                    #Rewind cursor to the beginning and get the selected account
                    allpw.rewind()
                    selected_account = allpw[selected_index]
                    deletePassword(collection, selected_account)
                else:
                    print("No credentials have been registered yet")
        elif (action == 2):
                details_key = user.generateKey()
                allpw = getPasswords(collection)
                for pw in allpw:
                    decrypted_email, decrypted_password, decrypted_service = decrypt_details(details_key, pw['email'], pw['password'], pw['service'])
                    print("Email: " + decrypted_email + "\t Password: " + decrypted_password + "\t Service: " + decrypted_service)
        else:
                return None
        print()
        input("Press Enter to return to menu\n")

    


def user_selection():
    prompt = "What do you want to do? "
    options = ['Add an account credentials', 'Delete an account credentials', 'View all credentials', 'Logout']
    selected_option, selected_index = pick.pick(options, prompt)
    return selected_index

def sign_up(users_collection):
        signup_email = getEmailInput()
        signup_password = getPasswordInput()
        #Check if user is already in database
        result = findEmail(users_collection, signup_email)
        if result is None:
            insertUser(users_collection, signup_email, signup_password)
            input("Press any key to continue.\n")
            return True
        else:
            print("Email has already been used for sign up, please try again")
            return False


#GET THE URL FROM ENVIRONMENT
# VARIABLES
selected_index = None
url = os.getenv('ENV_URL_PRE')+os.getenv('ENV_PASSWORD')+os.getenv('ENV_URL_POST')
#Define the title using pick
while selected_index != 2:
    prompt = "Welcome to the password manager! \n" + "Please select one of the following options: "
    options = ['Log in', 'Sign up', 'Exit']
    selected_option, selected_index = pick.pick(options, prompt)
    os.system('cls||clear') #this clears the terminal, cls is for windows and clear is for linux
    print("You have selected to", selected_option)
    startup_selection(selected_index)
