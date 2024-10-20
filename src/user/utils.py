import jwt


def encode_jwt(
        payload: dict,
        private_key: str | bytes
):
    return jwt.encode(payload, private_key, algorithm="RS256")


def decode_jwt(
    token,
    public_key: str | bytes
):
    return jwt.decode(token, public_key, algorithms=["RS256"])


def hash_password():
    pass

