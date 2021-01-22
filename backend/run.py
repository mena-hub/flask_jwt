from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, jwt_optional, fresh_jwt_required, get_raw_jwt, get_jwt_identity, 
                                create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, unset_access_cookies)
from application.app import create_app
from application.extensions import jwt

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)