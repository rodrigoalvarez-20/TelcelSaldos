from typing import Dict
from os import getcwd
import random
import jwt

def sign_jwt() -> Dict[str, str]:
    payload = {
        "rd": random.randint(0, 1000000)
    }

    with open(f"{getcwd()}/keys/private.key", "r", encoding="utf8") as f:
        token = jwt.encode(payload, f.read(), algorithm="RS256")
        return {"token": token}


def auth(token: str) -> Dict[str, str]:
    try:
        with open(f"{getcwd()}/keys/public.pub", "r", encoding="utf8") as f:
            decoded = jwt.decode(token, f.read(), algorithms=["RS256"])
            return {"status": 200, **decoded}
    except jwt.PyJWTError as error:
        print(error)
        return {"status": 401, "error": str(error)}


if __name__ == "__main__":
    print(sign_jwt())