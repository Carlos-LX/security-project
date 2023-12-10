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

def encrypt_inserted_message(key, string):
    cipher = Fernet(key)
    encryped_string = cipher.encrypt(string.encode())
    return encryped_string.decode()
def decrypt_inserted_message(key, encrypted_string):
    cipher = Fernet(key)
    decryped_string = cipher.decrypt(encrypted_string).decode()
    return decryped_string

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
            case 1:
                signed_up = False
                while signed_up  != True:
                    signed_up = sign_up(users_collection)
                break
            case 2:
                exit()

def encrypt_input_email_and_input_password(details_key):
            newly_added_email = getEmailInput()
            newly_added_password = getPasswordInput()
            encrypted_email = encrypt_inserted_message(details_key,newly_added_email)
            encrypted_password = encrypt_inserted_message(details_key,newly_added_password)
            return encrypted_email, encrypted_password

def user_action(user : User, action, collection: Collection): #do an action on the collection basically
    #clear the terminal
        os.system('cls||clear')
        match action:
            case 0:
                raise Exception("test")
                encrypted_email, encrypted_password = encrypt_input_email_and_input_password(user.generateKey())
                insertPassword(collection, encrypted_email, encrypted_password)
            case 1:
                details_key = user.generateKey()
                allpw = getPasswords(collection)
                length = collection.count_documents({}) #get the length of the collection
                options_list = []
                if length > 0:
                    for pw in allpw:
                        decrypted_email = decrypt_inserted_message(details_key, pw['email'])
                        decrypted_password = decrypt_inserted_message(details_key, pw['password'])
                        options_list.append("Email: " + decrypted_email + " Password: " + decrypted_password)
                    prompt = "Select an account to delete:"
                    selected_option, selected_index = pick.pick(options_list, prompt)
                    #Rewind cursor to the beginning and get the selected account
                    allpw.rewind()
                    selected_account = allpw[selected_index]
                    deletePassword(collection, selected_account)
                else:
                    print("No credentials have been registered yet")
            case 2:
                details_key = user.generateKey()
                allpw = getPasswords(collection)
                for pw in allpw:
                    decrypted_email = decrypt_inserted_message(details_key, pw['email'])
                    decrypted_password = decrypt_inserted_message(details_key, pw['password'])
                    print("Email: " + decrypted_email + "\t Password: " + decrypted_password)
            case 3:
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
