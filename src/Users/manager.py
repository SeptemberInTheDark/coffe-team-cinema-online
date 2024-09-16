import hashlib

class UserHashManager():
    def __init__(self, id, user_password, user_salt) :
        self.password = user_password
        self.user_salt = user_salt

    @staticmethod
    def hash_str(str, salt):
        return hashlib.sha3_256((str + salt).encode('utf-8')).hexdigest()
