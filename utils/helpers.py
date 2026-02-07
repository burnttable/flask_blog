from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)

def truncate_text(text, length=150):
    if len(text) <= length:
        return text
    return text[:length] + '...'
