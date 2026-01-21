from flask_restful import reqparse
import re
from flask import current_app

def sanitize_string2(text):
    """Sanitiza text, permitindo letras, números, espaços, e caracteres especiais (.,;'-+/\\)."""
    if not text or not isinstance(text, str):
        raise ValueError("Name cannot be empty or non-string!")
    
    text = text.strip()
    #if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s.,;'\-+/\\]+$", text):
    #    raise ValueError("Name contains invalid characters!")
    
    return text.title()


def sanitize_string(address):
    """
    Sanitiza endereços, permitindo:
    - Letras (incluindo acentuadas), números, espaços.
    - Caracteres especiais: ,.-ªº°/'\
    - Símbolos comuns em endereços.
    """
    if not address or not isinstance(address, str):
        raise ValueError("Address cannot be empty or non-string!")

    address = address.strip()
    if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s,.\-ªº°'/\\]+$", address, re.UNICODE):
        raise ValueError("Address contains invalid characters!")
    
    return address  # Opcional: .title() se quiser capitalizar palavras

def sanitize_name(name):
    """Remove extra spaces and allow alphabetic characters and digits."""
    name = name.strip()
    if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s.;'-+]+$", name):  # Allows letters, digits, spaces, periods, hyphens, and apostrophes
        raise ValueError("Name contains invalid characters!")
    return name.title()  # Capitalizes first letter of each word

def sanitize_username(username):
    """Ensure username contains only alphanumeric characters and underscores."""
    username = username.strip()
    if not re.match(r"^\w+$", username):  # Allows letters, numbers, and underscores
        raise ValueError("Username can only contain letters, numbers, and underscores!")
    return username.lower()  # Convert to lowercase

def sanitize_email(email):
    """Trim spaces, convert to lowercase, and validate email format."""
    email = email.strip().lower()
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):  
        raise ValueError("Invalid email format!")
    return email

def sanitize_country(country):
    """Allow only letters and spaces in country name."""
    country = country.strip()
    if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s-+]+$", country):  # Supports accented letters
        raise ValueError("Invalid country name!")
    return country.title()

def sanitize_phone(phone):
    """Remove spaces and ensure only numbers are present."""
    phone = str(phone).strip()  # Converte para string e remove espaços
    phone = re.sub(r"\D", "", phone)  # Remove non-digit characters
    if not re.match(r"^\d+$", phone):  
        raise ValueError("Phone number should contain only digits!")
    return phone

# Password validation is already strong


# Custom validation functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format!")
    return email

def validate_phone(phone):
    if not phone.isdigit() or len(phone) != 10:
        raise ValueError("Phone number must be exactly 10 digits!")
    return phone

def validate_password(password):
    """
    Validate password to be strong:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long!")
    
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter (A-Z)!")
    
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter (a-z)!")
    
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit (0-9)!")
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character (!@#$%^&* etc.)!")
    
    return password



# Create parser function
def get_user_parser():
    parser = reqparse.RequestParser()
    
    #parser.add_argument('email', type=validate_email, required=True, help="Valid email is required!")

    ALLOWED_COUNTRIES = current_app.config.get('ALLOWED_COUNTRIES', [])
    ALLOWED_COUNTRIES_CODE = current_app.config.get('ALLOWED_COUNTRIES_CODE', [])
   

    parser.add_argument('firstName', required=True, type=sanitize_name, help="First name cannot be blank!")
    parser.add_argument('lastName', required=True, type=sanitize_name, help="Last name cannot be blank!")
    #parser.add_argument('username', required=True, type=sanitize_username, help="Username cannot be blank!")
    parser.add_argument('authEmail', required=True, type=sanitize_email, help="Enter a valid email!")
    #choices=current_app.config.get('ALLOWED_COUNTRIES_CODE')
    parser.add_argument('authPassword', required=True, type=validate_password, help="Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
    parser.add_argument('countryName', required=True, type=sanitize_name, help=f"Country cannot be blank!")
    parser.add_argument('countryTelCode', required=True, type=sanitize_name, help="Country's phone code cannot be blank!")
    parser.add_argument('phoneNumber', required=True, type=sanitize_phone, help="Phone number cannot be blank!")
    parser.add_argument('postalCode', required=True, type=sanitize_phone, help="Postal code cannot be blank!")
    parser.add_argument('userAddress', required=True, type=sanitize_string, help="Address cannot be blank!")
    parser.add_argument('registeringAs', required=True, type=sanitize_name, help="The registered as field cannot be blank!")
    return parser
