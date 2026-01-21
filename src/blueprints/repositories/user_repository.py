
import logging, sys
from typing import Union, Dict, Any
from sqlalchemy.exc import OperationalError, IntegrityError
from pydantic import ValidationError, ValidationInfo
from src.utils import DatabaseConnectionError, DatabaseIntegrityError, DatabaseQueryError
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from src.models import User

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

class UserRepository:

    @staticmethod
    def create(user_data):
        return {}
    
    @staticmethod
    def get():
        try:
            return User.query.all()
        except OperationalError as e:
            logger.error(f"Error: {str(e)}", exc_info=True)
            raise DatabaseConnectionError("Database connection has failed") from e
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Database error ") from e

    
    @staticmethod
    def user_exists(user_id: int) -> bool:
        """
        Verifica se um usuário existe no banco de dados pelo ID.
        
        Args:
            user_id: ID do usuário a ser verificado
            
        Returns:
            bool: True se o usuário existe, False caso contrário
            
        Raises:
            DatabaseConnectionError: Em caso de erro de conexão com o banco
            DatabaseError: Em caso de outros erros do banco de dados
        """
        
        try:
            # Usando first() em vez de all() para melhor performance
            user = User.query.filter_by(id=user_id).first()
            return user is not None
            
        except OperationalError as e:
            logger.error(f"Erro de conexão com o banco ao verificar usuário {user_id}: {str(e)}", exc_info=True)
            raise DatabaseConnectionError("Falha na conexão com o banco de dados") from e
            
        except SQLAlchemyError as e:
            logger.error(f"Erro de banco de dados ao verificar usuário {user_id}: {str(e)}", exc_info=True)
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Database error ") from e

    @staticmethod
    def get_users_by_type(user_type: str):
        try:
            return User.query.filter_by(type_of_user=user_type).all()
        except OperationalError as e:
            logger.error(f"Error: {str(e)}", exc_info=True)
            raise DatabaseConnectionError("Database connection has failed") from e
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Database error ") from e

        
    @staticmethod
    def get_users_by_id(user_id: int):
        
        try:
            return User.query.filter_by(id=user_id).all()
        except OperationalError as e:
            logger.error(f"Error: {str(e)}", exc_info=True)
            raise DatabaseConnectionError("Database connection has failed") from e
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Database error ") from e

    
    @staticmethod
    def get_users_by_email(user_email: str):
        
        try:
            return User.query.filter_by(email=user_email).all()
        except OperationalError as e:
            logger.error(f"Error: {str(e)}", exc_info=True)
            raise DatabaseConnectionError("Database connection has failed") from e
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Database error ") from e
    
    @staticmethod
    def get_users_by_username(user_name: str):
        
        try:
            return User.query.filter_by(username=user_name).all()
        except OperationalError as e:
            logger.error(f"Error: {str(e)}", exc_info=True)
            raise DatabaseConnectionError("Database connection has failed") from e
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Database error ") from e
            