from flask import redirect, make_response, render_template
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

@app.route('/token/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user_id))
    response = make_response(redirect(app.config['BASE_URL'] + '/', 302))
    set_access_cookies(response, access_token)
    return response

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

@app.route('/account')
@fresh_jwt_required
def account():
    username = get_jwt_identity()
    csrf_token = (get_raw_jwt() or {}).get("csrf")
    return render_template("frontend/account.html", csrf_token=csrf_token), 200
    # Very important account settings 

@app.route('/services', methods=['GET'])
@jwt_required
def services():
    username = get_jwt_identity()
    return render_template("frontend/services.html"), 200
    # Not important stuff but still needs to be logged in 

@app.route('/')
@jwt_optional
def home():
    username = get_jwt_identity() # None if not logged in
    return render_template("frontend/home.html"), 200
    # Accessible to everyone but maybe different to logged in users 

@app.route('/login', methods=['POST'])
def login():
    # Verify username and password 
    return assign_access_refresh_tokens('test', app.config['BASE_URL'] + '/')

@app.route('/logout')
@jwt_required
def logout():
    # Revoke Fresh/Non-fresh Access and Refresh tokens
    return unset_jwt(), 302

if __name__ == '__main__':
    app.run(debug=True)