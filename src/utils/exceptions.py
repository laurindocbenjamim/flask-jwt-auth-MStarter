

from sqlalchemy.exc import (SQLAlchemyError, 
                            DatabaseError, 
                            OperationalError, 
                            IntegrityError, 
                            DataError
                            )


class BusinessRuleError(Exception):
    """ .... """
    pass

class DuplicateError(Exception):
    """ .... """
    pass

class EntityNotFoundError(Exception):
    """ .... """
    pass

class DatabaseError(Exception):
    """Base exception for all database errors"""
    pass

class DatabaseConnectionError(DatabaseError):
    """Failed to connect to database"""
    pass

class DatabaseQueryError(DatabaseError):
    """Error in database query execution"""
    pass

class DatabaseIntegrityError(DatabaseError):
    """Data integrity violation error"""
    pass

class RecordNotFoundError(DatabaseError):
    """Requested record not found"""
    pass

class UserAlreadyExistsError(DatabaseError):
    """Usuário já existe no sistema"""
    pass

class InvalidUserDataError(DatabaseError):
    """Dados do usuário são inválidos"""
    pass

class DatabaseErrorFactory:
    """Factory para criar exceções personalizadas baseadas em erros do SQLAlchemy"""
    
    @staticmethod
    def create_from_sqlalchemy_error(error: SQLAlchemyError) -> DatabaseError:
        """Cria exceção personalizada baseada no erro do SQLAlchemy"""
        error_message = str(error.orig) if hasattr(error, 'orig') else str(error)
        
        if isinstance(error, OperationalError):
            return DatabaseConnectionError(f"Erro de conexão: {error_message}")
        elif isinstance(error, IntegrityError):
            return DatabaseIntegrityError(f"Erro de integridade: {error_message}")
        elif isinstance(error, DataError):
            return DatabaseQueryError(f"Erro de dados: {error_message}")
        else:
            return DatabaseQueryError(f"Erro de banco de dados: {error_message}")