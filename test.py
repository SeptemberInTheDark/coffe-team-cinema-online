from argon2 import PasswordHasher


ph = PasswordHasher()

def hash_password(password: str) -> str:

    return ph.hash(password)


def check_password(stored_hashed_password: str, input_password: str) -> bool:
    try:
        ph.verify(stored_hashed_password, input_password)
        return True
    except Exception:
        return False


user_pass = '123'

user_hash = hash_password(user_pass)
user_unhash = check_password(user_hash, user_pass)

print(f'user_hash: {user_hash}')
print(f'user_unhash: {user_unhash}')
