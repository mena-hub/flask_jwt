from flask import redirect, make_response
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, jwt_optional, fresh_jwt_required, get_raw_jwt, get_jwt_identity, 
                                create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, unset_access_cookies)
from application.app import create_app
from application.extensions import jwt

app = create_app()

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    # No auth header
    return redirect(app.config['BASE_URL'] + '/', 302)

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    # Invalid Fresh/Non-Fresh Access token in auth header
    response = make_response(redirect(app.config['BASE_URL'] + '/'))
    unset_jwt_cookies(response)
    return response, 302

@jwt.expired_token_loader
def expired_token_callback(callback):
    # Expired auth header
    response = make_response(redirect(app.config['BASE_URL'] + '/token/refresh'))
    unset_access_cookies(response)
    return response, 302

def assign_access_refresh_tokens(user_id, url):
    access_token = create_access_token(identity=str(user_id), fresh=True)
    refresh_token = create_refresh_token(identity=str(user_id))
    response = make_response(redirect(url, 302))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response

def unset_jwt():
    response = make_response(redirect(app.config['BASE_URL'] + '/', 302))
    unset_jwt_cookies(response)
    return response

if __name__ == '__main__':
    app.run(debug=True)