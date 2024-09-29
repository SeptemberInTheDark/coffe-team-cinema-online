# import bcrypt
# import hashlib
# import os

from argon2 import PasswordHasher


ph = PasswordHasher()
class UserHashManager():

    # @staticmethod
    # def hash_password(password: str):
    #     salt = os.urandom(32)
    #     return hashlib.sha256(salt + password).hexdigest()

    # @staticmethod
    # def check_pasword(stored_hashed_password, salt, input_password):
    #     return stored_hashed_password == hashlib.sha256(salt + input_password).hexdigest()


    @staticmethod
    def hash_password(password: str) -> str:
        return ph.hash(password)


    @staticmethod
    def check_password(stored_hashed_password: str, input_password: str) -> bool:
        try:
             ph.verify(stored_hashed_password, input_password)
             return True
        except Exception:
             return False
