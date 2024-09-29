# import bcrypt
# import hashlib
# import os

from argon2 import PasswordHasher


password_hassher = PasswordHasher()
class UserHashManager():
    def __init__(self, ph=password_hassher) -> None:
        self.ph = ph

    # @staticmethod
    # def hash_password(password: str):
    #     salt = os.urandom(32)
    #     return hashlib.sha256(salt + password).hexdigest()

    # @staticmethod
    # def check_pasword(stored_hashed_password, salt, input_password):
    #     return stored_hashed_password == hashlib.sha256(salt + input_password).hexdigest()


    def hash_password(self, password: str) -> str:
        return self.ph.hash(password)


    def check_password(self, stored_hashed_password: str, input_password: str) -> bool:
        try:
             self.ph.verify(stored_hashed_password, input_password)
             return True
        except Exception:
             return False


user_hash_manager = UserHashManager()
