import os


SECRET_KEYS = [
    "JWT_SECRET",
    "JWT_ALGORITHM",
    "ACCESS_TOKEN",
    "SALT_GENERATOR",
    "ALPHABET",
    "ROOTUSERNAME",
    "ROOTPASSWORD",
    "ADMIN_USER",
    "ADMIN_PASSWORD",
    "ADMIN_EMAIL",
    "AES256_KEY",
    "AES256_IV",
]

envirinment = os.environ.get("ENVIRONMENT")

def fetch_secrets():
    
    response = {key: os.environ.get(key) for key in SECRET_KEYS}
    response['DATABASE_URL'] = os.environ.get("DATABASE_URL_LOCAL")
    return response

secrets = fetch_secrets()
