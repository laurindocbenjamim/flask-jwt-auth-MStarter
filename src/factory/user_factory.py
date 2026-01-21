
import sys
import os

sys.path.append(os.path.abspath("flask-jwt-authentication-2025"))

import sqlalchemy
from src.models import User
from src.utils import db

def create_user_object(user_data):
    user = User()  # Create an instance
    
    # Set password correctly before returning the object
    user.set_password(user_data.get("authPassword"))

    return User(
        email=user_data.get("authEmail"),
        username=user_data.get("authEmail"),
        password_hash=user.password_hash,
        firstname=user_data.get("firstName"),
        lastname=user_data.get("lastName"),
        country=user_data.get("countryName"),
        country_tel_code=user_data.get("countryTelCode"),
        phone_number=user_data.get("phoneNumber"),
        address=user_data.get("userAddress"),
        postal_code=user_data.get("postalCode"),
        type_of_user=user_data.get("registeringAs"),
        confirmed=user_data.get("user_confirmed")
        #created_at=user_data.get("created_at")
        
    )


def create_user(new_user: User):
    """
    Create a new user and add it to the database.

    Args:
        new_user (User): The user object to be added to the database.

    Returns:
        tuple: A tuple containing a boolean indicating success or failure, and the user object or error message.
    """
    if not new_user:
        return False, "User object is None"
    try:
        db.session.add(new_user)
        db.session.commit()
        return True, new_user
    #except db.IntegrityError as e:
    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        error_message = str(e.orig)
        if "email" in error_message:
            return False, "IntegrityError: The email already exists."
        if "username" in error_message:
            return False, "IntegrityError: The username already exists."
        if "phone_number" in error_message:
            return False, "IntegrityError: The phone number already exists."
        return False, f"IntegrityError: {error_message}"
    except sqlalchemy.exc.OperationalError as e:
        db.session.rollback()
        return False, f"OperationalError: {str(e)}"
    except Exception as e:
        db.session.rollback()
        return False, f"Unexpected error: {str(e)}"
    #finally:


def delete_user(user_id: int):
    """
    Delete user and add it to the database.

    Args:
        new_user (User): The user object to be added to the database.

    Returns:
        tuple: A tuple containing a boolean indicating success or failure, and the user object or error message.
    """
    if not user_id:
        return False, "User object is None"
    try:
        
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
        
        db.session.delete(user)
        db.session.commit()
        return True, user_id
    except sqlalchemy.exc.OperationalError as e:
        db.session.rollback()
        return False, f"OperationalError: {str(e)}"
    except Exception as e:
        db.session.rollback()
        return False, f"Unexpected error: {str(e)}"
    #finally:

        


def confirm_user_email(user: User):
    """
    Confirm the user's email.

    Args:
        user (User): The user object whose email is to be confirmed.

    Returns:
        tuple: A tuple containing a boolean indicating success or failure, and a message.
    """
    if not user:
        return False, "User object is None"

    if user.confirmed:
        return True, "Account already confirmed"
    
    try:
        user.confirmed = True
        db.session.commit()
        return True, "Account successfully confirmed. "
    except db.OperationalError as e:
        db.session.rollback()
        return False, f"OperationalError: {str(e)}"
    except Exception as e:
        db.session.rollback()
        return False, f"Unexpected error: {str(e)}"