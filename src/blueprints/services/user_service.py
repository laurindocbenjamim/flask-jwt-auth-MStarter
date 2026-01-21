
import logging, sys
from typing import Union, Dict, Any
from pydantic import ValidationError, ValidationInfo
from src.blueprints.repositories import UserRepository
from src.utils import DatabaseConnectionError, UserAlreadyExistsError, InvalidUserDataError
from src.models import User
from src.blueprints.schemas import UserCreateRequest

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

class UserService:

    def __init__(self, repository: UserRepository = None):
        self.repository = repository or UserRepository()

    def create(self, user_data: dict)-> Union[Dict[str, Any], Any]:


        try:

            user_data_validated = UserCreateRequest(**user_data)

            # Criar usuário com método factory
            user = User.create_user(user_data_validated)
            """user = User.create_user(
                username="joaosilva",
                email="joao@email.com",
                password_hash="hashed_password_123"
            )"""
            return user
            # User.serialize_all(users)
        except DatabaseConnectionError as e:
            logger.error(f"Error: {str(e)}")
            return { "success": False, "error": str(e), "type": "database_connection" }
        
        except UserAlreadyExistsError as e:
            logger.error(f"Error: {str(e)}")
            return { "success": False, "error": e.errors() }
            
        except InvalidUserDataError as e:
            logger.error(f"Error: Dados inválidos. {e}")
            return { "success": False, "error": f"Dados inválidos: { e.errors() }"  }
           
        except Exception as e:
            logger.error(f"Error: Erro inesperado. {e}")
    
        
    
    def get(self)-> Union[Dict[str, Any], Any]:
        try:
            users = UserRepository.get()
            return User.serialize_all(users)
        except ValidationError as e:
            logger.error(f"Error: {str(e)}")
            return { "success": False, "error": e.errors() }
        except DatabaseConnectionError as e:
            logger.error(f"Error: {str(e)}")
            return { "success": False, "error": str(e), "type": "database_connection" }
        
    def user_exists(self, user_id: int)-> Union[Dict[bool, Any], Any]:

        if not isinstance(user_id, int) or user_id <= 0:
            logger.warning(f"ID de usuário inválido: {user_id}")
            return False
    
        try:
            return UserRepository.user_exists(user_id)
        except ValidationError as e:
            logger.error(f"Error: {str(e)}")
            return { "success": False, "error": e.errors() }
        except DatabaseConnectionError as e:
            logger.error(f"Error: {str(e)}")
            return { "success": False, "error": str(e), "type": "database_connection" }
        
    def get_user_by_type(self, user_type)-> Union[Dict[str, Any], Any]:

        if not user_type:
            return { "success": False, "error": "user type not found" }

        try:
            users = UserRepository.get_users_by_type(user_type)
            return User.serialize_all(users)
        except ValidationError as e:
            logger.error(f"Error: {str(e)}")
            return { "success": False, "error": e.errors() }
        except DatabaseConnectionError as e:
            logger.error(f"Error: {str(e)}")
            return { "success": False, "error": str(e), "type": "database_connection" }