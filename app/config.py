import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta, timezone

class Config:
    # Clave secreta para firmar los tokens JWT
    JWT_SECRET_KEY = 'itsAs3cr34tkeyforJWT'
    
    # Tiempo de expiración del token de acceso
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)