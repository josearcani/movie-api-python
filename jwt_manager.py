from jwt import encode, encode

def create_token(data: dict) -> str:
    token: str = encode(payload=data, key="my_secret_key", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = encode(token, key="my_secret_key", algorithms=['HS256'])
    return data

if __name__ == "__main__":
    print(create_token({"username": "admin"}))