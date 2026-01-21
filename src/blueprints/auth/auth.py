
import sys
import os

sys.path.append(os.path.abspath("flask-jwt-authentication-2025"))

from flask_restful import Api, Resource, reqparse
from src.utils import db
from src.models import User, TokenBlocklist, TokenBlocklist2

from flask import (
    Blueprint, jsonify,
    make_response, current_app
)

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    current_user,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies
)
from sqlalchemy.sql import func
import secrets
import jwt
from src.blueprints.emails import send_confirmation_email

from src.factory import (
    create_user, create_user_object
)

auth_api = Blueprint('auth_api', __name__, url_prefix='/api/v1/auth')
api = Api(auth_api)

@auth_api.route('/test-create')
def test_create():
    from src.blueprints.services import UserService

    user = User()  # Create an instance
    
    # Set password correctly before returning the object
    user.set_password("Admin90#")


    status, response = create_user(new_user=User(
        email="panther@pidio.com",
        username="panther@",
        password_hash=user.password_hash,
        firstname="Pidion",
        lastname="Sonan",
        country="Portugal",
        country_tel_code="+351",
        phone_number="9299299",
        address="Porto",
        postal_code="4000-233",
        type_of_user="admin",
        confirmed=True
        #created_at=user_data.get("created_at")
        
    ))
    return {"success": status, "data": response}
    """user_data = {
        firstname="Ann", 
         lastname="Takamaki", 
         username="panther", 
         email="panther@datatuning.pt", 
         confirmed=True, 
         password_hash=generate_password_hash(""),
         type_of_user="Admin"
    }"""
    """User(firstname="Ann", 
         lastname="Takamaki", 
         username="panther", 
         email="panther@datatuning.pt", 
         confirmed=True, 
         password_hash=generate_password_hash(""),
         type_of_user="Admin"
         )"""
    #user = UserService().create(user_data=user_data)

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        data = parser.parse_args()
        
        # Here you would add your authentication logic
        
        username = data.get('username')
        password = data.get('password')
        

        user = User.query.filter_by(email=username).one_or_none()
        if not user:
            return make_response(jsonify(status_code=401, error="User has not found."),401)
        if not user.check_password(password):
            return make_response(jsonify(status_code=401, error="Wrong password. Try again"),401)
        # Generate a JWT token

        if not user.confirmed:
            status = send_confirmation_email(user.email)
            if not status:
                return make_response(jsonify(status_code=401, error="Your account has not been confirmed yet."),401)
            return make_response(jsonify(status_code=201, message=f"Your account has not been confirmed yet. We've sent a confirmation link to [{user.email}]. "),200)
        
        access_token = create_access_token(identity=str(user.id), expires_delta=current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES'))
        
        response = make_response(jsonify({'status_code': 200, 'message':"User logged successfull!", "username": user.email, "registered_as": user.type_of_user}),200)
        
        if current_app.config['JWT_COOKIE_SECURE']:
            response.set_cookie(
                'access_token_cookie',
                value=access_token,
                #domain='.d-tuning.com',  # Note the leading dot for subdomains
                secure=current_app.config['JWT_COOKIE_SECURE'],  # Required for HTTPS in production
                httponly=False,  # Allow JS access
                samesite=current_app.config['JWT_COOKIE_SAMESITE'],  # Required for cross-origin
                path="/",  # Ensure it’s available site-wide
                max_age=3600  # Tempo de vida em segundos
            )
        else:
            response.set_cookie(
                "access_token_cookie",
                value=access_token,
                #domain=".yourdomain.com",  # Critical for cross-origin
                secure=True,  # Allow non-HTTPS in development. When set to True works in localhost
                httponly=False,
                samesite="None",
                path="/"
            )
        
        """
        set_access_cookies(response, access_token, domain="www.d-tuning.com")
        removed becasue of the error: "Cookies is missing. And Token has been revoked"
        """
        #set_access_cookies(response, access_token) #domain="http://localhost:5000"
        # For production, set domain and secure properly
        
        current_app.logger.info(f"Set-Cookies headers: {response.headers}")
        return response


class Logout(Resource):
    @jwt_required(verify_type=False)
    def get(self): 
        
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)
        block_list=None

        try:
            block_list = TokenBlocklist(jti=jti, type=ttype, created_at=now)
            db.session.add(block_list)
            db.session.commit()
            response = make_response(jsonify(msg=f"{ttype.capitalize()} token successfully revoked", logout="Your session has been terminated!", block_list=block_list.to_dict()), 200)
        except Exception as e:
            response = make_response(jsonify(error=str(e)),500)      
        
        #unset_jwt_cookies(response)
        return response


    # Delete
    @jwt_required(verify_type=False)
    def delete(self):

        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)
        block_list=None

        try:
            block_list = TokenBlocklist(jti=jti, type=ttype, created_at=now)
            db.session.add(block_list)
            db.session.commit()
            response = jsonify(msg=f"{ttype.capitalize()} token successfully revoked", logout="Your session has been terminated!", block_list=block_list.to_dict())
        except Exception as e:
            return jsonify(error=str(e))        
        
        #unset_jwt_cookies(response)
        return response

    

 

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')


