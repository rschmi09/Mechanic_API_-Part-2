# Mechanic_API/App/utils/util.py

import os

import jose
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify


SECRET_KEY = os.environ.get('SECRET_KEY') or 'super secret secrets'

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(customer_id)
    }

    # HS256 is a hashing algorithm (scramble) code using secret key and imbed all payload inforamtion
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None #placeholder variable

        if 'Authorization' in request.headers:

            token = request.headers['Authorization'].split()[1]

            if not token:
                return jsonify({'message': 'missing token'}),400
            
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                print(data)
                customer_id = int(data['sub'])

            except ExpiredSignatureError:
                return jsonify({'message': 'Token expired'}), 400
            
            except JWTError:
                return jsonify({'message': 'Invalid token'}), 400

            return f(customer_id, *args, **kwargs)

        else:
            return jsonify({'message': 'You must be logged in'}),400
        
    return decorated
        


