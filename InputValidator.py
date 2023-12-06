
from email_validator import validate_email, EmailNotValidError #to validate email
import re

#define functions

def email_validation(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError as e:
        print(e)
        return False


def password_validation(password: str):
    #Check the length first
    try:
        if (len(password) < 5):
            raise ValueError("Password must be at least 5 characters long")
        #Check for a capital
        capital_result = re.search(".*[A-Z].*", password)
        
        if (capital_result == None):
            raise ValueError("Password have at least 1 capital character")
        
        #check for lowercase

        lowercase_result = re.search(".*[a-z].*", password)
        
        if (lowercase_result == None):
            raise ValueError("Password have at least 1 lowercase character")
        
        #Search for a number
        number_result = re.search(r'\d', password)
        if (number_result == None):
            raise ValueError("Password must contain at least 1 digit")
        
        return True
    except ValueError as e:
        print(e)
        return False
    


    
def getEmailInput():
    email = input("Please input an email: ")
    while (email_validation(email) == False):
        email = input("Please input an email: ")
    return email

def getPasswordInput():
    password = input("Please input a password: ")
    while (password_validation(password=password) == False):
        password = input("Please input a password: ")
    return password

