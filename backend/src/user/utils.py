import jwt

my_private_key = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCq6zoSdzHsfo7T
Giy1sDtSHbNgwjdMQ1iPDGY5SPwayw1fRkyMUO+tXL4b/6OobJlmzIPwT7Ew8/em
FvHhkWy97pDIlUOZ4TervIVHQV3OQvFI2r1lk03HvKBu0aam11TaGiw3iP1SaDuX
ykk/o7lhYR8zv9f+WUH2bVNlEvqlswFKKX+RakqjRyNrjJNW244V8Ahkm/8Gea0o
/HPOKlPbyNcASp51OJq8pYtD4SGrFqjgi4hpEjgFXM4KsnjjagcGxnAbiqHTGS3D
e5Xsul6kLuWeazozj1mQeiU76cMzILfMq8Qy+RgeqU6Fnx9OOueTvmXztAIROVsP
+tvw3FznAgMBAAECggEAG7KwAAMR85XU1nAE89Kh4l5OzezbYj/9r3zeagUiWcMz
IQ/24rxRAwKnCkmEv4wN1gNplD2N5PV8Wg2Y2CmleigZjW/m+x5s06di39e/eGgP
yvMrwzS6Y5Z1V1AhViNKLGgWZ0+LYdnjYmdVNHt3VMkU8eFygtT7JBC2dYg8VzKl
xDfrK0udB9M/5XfqhXcinLK/w/vrum28DmpHy/hIMHkwl9a39SBFZJ6u6Zl90THU
jZ26ZG+W8fttRKdB0oPA3k8vE4mXPo997dlHnuekedUAQi66AyKB47JZPt6PQk75
o7DuS4RXui5hJLjR/lkwY811oWKQpqVD9YMrOZ67PQKBgQDR+c4ZwI48TuW4YDa6
iO1IQ1aYf0FSuWhqCWhrhwxD/Vl2X4LSdzNf7y/y+EbI+tY26uTHdyJrXOiM96iN
TMkqNJ2tdyn5B7he/auHKO6ue0ratRb1pH1aWjfBu2r4mrCzUY0uR9shChy8J9VQ
dbMudIYVJ39uWVlHNmMhkxRwMwKBgQDQYdowboHTXB+SY6uP51tnOSR72JYiIGpB
d/XwYmbRKtlEItPtHYgE8a+ylhmCxSifxWlunN970osZXE2hQZMNuiNT2nCGd1tZ
K+ni3cxB6DtDDtwmuJbrbe9BFncNAY0HP7mHT/2G4tfp/sUaOmCVgg0leVFkk8HJ
td3zQfQcfQKBgD5s4hVN5fuQCUPTdvHmG4VMX8ZervEFJkHAIkc1kzPzclF6+83O
mnt/BOZbYdAGowEYvIOAq773lDu0tWus1HGzytzzfIsI/IthJ0m7pZpCFXMIO5c0
HABsqf7y1U6rzrTBHhQQUNl1xC08OnL9SxQYmHRZlc0cyyocxUQKEh15AoGAaQdo
+dA5D1b3cslZx4ZMw5JBmUppIXpFFApqo2Z1fCekqnsDZhfkXtmSPOj6orbM6vqN
UXswCTDtezLSzdxHSjvvYmxPGvc9y4weroIsWWu7sujifYG8T51xYdT43E1Tz7uG
v3TJzBq5yO7oWXfjBnguOB0VsSPoIMrRu7IaX+ECgYEA0S9U5KdCPSW5J5hDLsSe
abO13Hec0UDgMVhrFn0xoHQL9FnwZiflW+ygrUtCKmUv8XQHDNkEI+bpUjC8B8vX
e4HnoxkC4PX9PtTTzWU1KqE/1pViTwdmD8+FUWhxvSzJU1sAzPp2g73vHlB8jnBS
6uSSAiJxhpU6EBF0bENQ/TQ=
-----END PRIVATE KEY-----
"""

my_public_key = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqus6Encx7H6O0xostbA7
Uh2zYMI3TENYjwxmOUj8GssNX0ZMjFDvrVy+G/+jqGyZZsyD8E+xMPP3phbx4ZFs
ve6QyJVDmeE3q7yFR0FdzkLxSNq9ZZNNx7ygbtGmptdU2hosN4j9Umg7l8pJP6O5
YWEfM7/X/llB9m1TZRL6pbMBSil/kWpKo0cja4yTVtuOFfAIZJv/BnmtKPxzzipT
28jXAEqedTiavKWLQ+Ehqxao4IuIaRI4BVzOCrJ442oHBsZwG4qh0xktw3uV7Lpe
pC7lnms6M49ZkHolO+nDMyC3zKvEMvkYHqlOhZ8fTjrnk75l87QCETlbD/rb8Nxc
5wIDAQAB
-----END PUBLIC KEY-----
"""


def encode_jwt(
        payload: dict,
        private_key: str | bytes = my_private_key
):
    return jwt.encode(payload, private_key, algorithm="RS256")


def decode_jwt(
    token,
    public_key: str | bytes = my_public_key
):
    return jwt.decode(token, public_key, algorithms=["RS256"])


def hash_password():
    pass


d = {
  "id": 1,
  "password": "string",
  "is_banned": False,
  "username": "string",
  "email": "user@example.com",
  "register_at": "2024-10-19T11:06:54"
}
print(encode_jwt(d))
