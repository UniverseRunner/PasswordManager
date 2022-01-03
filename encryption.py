from cryptography.fernet import Fernet
import json


class Encryption():
    def __init__(self):
        self.a=""
    def encrypt(self,key):
        print("triggered funciton")
        f = Fernet(key)
        with open("data.json","rb") as file:
            to_encrypt = file.read()
        encrypted_data = f.encrypt(to_encrypt)
        with open("data.json", "wb") as file:
            file.write(encrypted_data)


    def decrypt(self,key, to_decrypt):
        f = Fernet(key)
        decrypted_data = f.decrypt(to_decrypt)
        return json.loads(decrypted_data)


