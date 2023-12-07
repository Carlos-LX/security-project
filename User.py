import base64

class User:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def generateKey(self):
        repeated_pass = (self.password * (32 // len(self.password) + 1))[:32] #got this from chatGPT, it repeats the password until the length is 32 for the key
        return base64.urlsafe_b64encode(repeated_pass.encode())