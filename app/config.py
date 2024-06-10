""" Module for configuration about tokens"""

from datetime import timedelta

class Config:
    """
    Configuration class for Flask application.

    Attributes:
        JWT_SECRET_KEY (str): Secret key used for signing JWT tokens.
        JWT_ACCESS_TOKEN_EXPIRES (timedelta): Expiration time for access tokens.
    """
    # Clave secreta para firmar los tokens JWT
    JWT_SECRET_KEY = 'itsAs3cr34tkeyforJWT'
    
    # Tiempo de expiración del token de acceso
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)