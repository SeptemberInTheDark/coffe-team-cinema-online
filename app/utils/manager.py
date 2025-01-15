from argon2 import PasswordHasher


password_hassher = PasswordHasher()
class UserHashManager():
    def __init__(self, ph=password_hassher) -> None:
        self.ph = ph


    def hash_password(self, password: str) -> str:
        return self.ph.hash(password)


    def check_password(self, stored_hashed_password: str, input_password: str) -> bool:
        try:
             self.ph.verify(stored_hashed_password, input_password)
             return True
        except Exception:
             return False


user_hash_manager = UserHashManager()
