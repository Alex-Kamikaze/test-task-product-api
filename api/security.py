import bcrypt

class PasswordSecurity():
    """ Утилита для хэширования и проверки паролей пользователей """
    def hash_password(plain_text_password: str) -> str:
        return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())
    
    def check_password_hash(plain_text_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_text_password, hashed_password)