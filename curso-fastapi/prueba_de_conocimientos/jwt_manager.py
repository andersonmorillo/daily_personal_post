from jwt import decode, encode

def encode_token(token: dict):
   token: str = encode(payload=token, key="secreto", algorithm="HS256")
   return token 

def decode_token(token: str):
    data: str = decode(token,key="secreto", algorithms=["HS256"])
    return data

