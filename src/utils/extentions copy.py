from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g, request
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_cors import CORS
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
cors = None
csrf = CSRFProtect()
mail = Mail()
#limiter = Limiter(key_func=get_remote_address, default_limits=[current_app.config['RATE_LIMIT']])
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day","50 per minute"])

# Method to load the application extentions
def load_extentions(*, app):
    """
    Initialize and load extensions for the Flask application.

    This function initializes and loads the following extensions for the given Flask application:
    - CSRF protection
    - CORS (Cross-Origin Resource Sharing)
    - Rate Limiting

    Args:
        app (Flask): The Flask application instance to which the extensions will be added.
    """
    csrf.init_app(app)
    mail.init_app(app)
    cors_origin = app.config['CORS_ORIGIN']

    
    """cors_p = CORS(
        app,
        supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS'],
        resources={
            r"/api/*": {
                "origins": cors_origin,
                "expose_headers": app.config['CORS_EXPOSE_HEADERS']  # ['Content-Type', 'X-CSRF-Token']
            }
        }
    )
    #cors_p.init_app(app)
    limiter.init_app(app)    """ 




def add_request_id_header(app, response):
    """Adiciona headers CORS com suporte para ambiente local e produção"""

    # Verifica se o header já foi definido em outro lugar
    if 'Access-Control-Allow-Origin' in response.headers:
        return response  # Não duplica se já existir
    
    # Configurações para ambiente de desenvolvimento
    if current_app.config.get('ENV') == 'development':
        # Permite qualquer origem em desenvolvimento (ajuste conforme necessário)
        origin = request.headers.get('Origin', '*')
        
        # Lista de IPs/domínios locais permitidos
        allowed_local = [   
            #BACKEND DOMAINS
            'http://localhost:8000', 'https://192.168.1.201:8443', 
            #FRONTEND DOMAINS
            'https://192.168.1.201:8000','https://192.168.1.224:8000',
            'https://192.168.1.224:8443', 'http://192.168.56.1:8000', 
            'http://0.0.0.0:8000'
        ]  


        #allowed_local = app.config['CORS_ORIGIN']
        
        # Verifica se a origem está na lista de permitidos ou permite todas em dev
        if origin in allowed_local or current_app.config.get('ALLOW_ALL_ORIGINS_DEV', True):
            response.headers.add('Access-Control-Allow-Origin', origin)
        else:
            response.headers.add('Access-Control-Allow-Origin', '')
    else:
        # Configuração de produção - domínios específicos
        production_domains = [
            'https://www.d-tuning.com',
            'https://outrodominio.com'
        ]
        origin = request.headers.get('Origin', '')
        if origin in production_domains:
            response.headers.add('Access-Control-Allow-Origin', origin)
        else:
            response.headers.add('Access-Control-Allow-Origin', '')

    # Headers comuns a ambos os ambientes
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Request-ID')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Max-Age', '86400')  # 24 horas
    
    # Adiciona o header X-Request-ID se existir no contexto
    #if hasattr(g, 'request_id'):
    #    response.headers.add('X-Request-ID', g.request_id)
    if hasattr(request, 'request_id'):
            response.headers['X-Request-ID'] = request.request_id
    
    return response


def configure_cors(app):
    """Configura o Flask-CORS de forma não conflitante"""
    cors_origin = app.config.get('CORS_ORIGINS', [])
    
    # Em desenvolvimento, permita todas as origens configuradas
    if app.config.get('ENV') == 'development':
        cors_origin = app.config.get('DEV_ALLOWED_ORIGINS', [
            'http://localhost:8000',
            'https://192.168.1.201:8443',
            'https://192.168.1.201:8000',
            'https://192.168.1.224:8000',
            'https://192.168.1.224:8443',
            'http://192.168.56.1:8000',
            'http://0.0.0.0:8000'
        ])

    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/api/*": {
                "origins": cors_origin,
                "expose_headers": app.config.get('CORS_EXPOSE_HEADERS', ['Content-Type', 'X-CSRF-Token']),
                "allow_headers": ['Content-Type', 'Authorization', 'X-Request-ID']
            }
        }
    )

def add_request_id_header(response):
    """
    Adiciona headers personalizados para rotas não-API
    e headers comuns para todas as rotas
    """
    
    # 1. Headers para rotas NÃO-API
    if not request.path.startswith('/api/'):
        origin = request.headers.get('Origin', '')
        
        # Lista de origens permitidas para rotas não-API
        non_api_allowed_origins = [
            'http://localhost:3000',
            'https://meufrontend.local'
        ]
        
        if origin in non_api_allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Expose-Headers'] = 'X-Request-ID'
    
    # 2. Headers para TODAS as rotas (incluindo APIs)
    if hasattr(g, 'request_id'):
        response.headers['X-Request-ID'] = g.request_id
    
    # 3. Headers especiais para rota específica
    if request.path == '/special-route':
        response.headers['X-Special-Feature'] = 'enabled'
    
    return response