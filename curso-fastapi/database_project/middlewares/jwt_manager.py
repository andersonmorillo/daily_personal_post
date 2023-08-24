from jwt import decode, encode
import bcrypt

def decode_token(token_encode: str) -> dict:
    user_info: dict = decode(token_encode, key="secreto", algorithms=["HS256"])
    return user_info


def encode_token(data: dict) -> str:
    token_encode: str = encode(payload=data, key="secreto", algorithm="HS256")
    return token_encode


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(hashed_password: str, password: str) -> bool:
    response: bool = bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    return response
