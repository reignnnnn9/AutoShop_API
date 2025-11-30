from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from jose import jwt
import jose, os

SECRET_KEY = os.environ.get('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Look for token in Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 404
        
        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            customer_id = data['sub'] # Fetch customer_id

        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Invalid'}), 401
        
        return f(customer_id, *args, **kwargs)
    
    return decorated

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1), # Setting the expiration time to 1 hour past now
        'iat': datetime.now(timezone.utc), # Issued at
        'sub': str(customer_id) # This needs to be a string or the token will be malformed and won't be able to be decoded
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token