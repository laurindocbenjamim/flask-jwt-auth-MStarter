
import sys
import os

sys.path.append(os.path.abspath("flask-jwt-authentication-2025"))

from sqlalchemy.exc import SQLAlchemyError, OperationalError, IntegrityError, DataError
from sqlalchemy import or_
from datetime import datetime, timezone
from src.utils import db, UserAlreadyExistsError, DatabaseQueryError, RecordNotFoundError
from src.utils import DatabaseIntegrityError, InvalidUserDataError, DatabaseConnectionError
from werkzeug.security import generate_password_hash, check_password_hash
import logging

logger = logging.getLogger(__name__)


class User(db.Model):
    """
    User model representing registered users
    
    Attributes:
        id: Primary key
        email: User's email address (unique)
        password_hash: Hashed password
        confirmed: Email confirmation status
        created_at: Account creation timestamp
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    country = db.Column(db.String(100))
    country_tel_code = db.Column(db.String(6))
    phone_number = db.Column(db.String(10), unique=True)
    address = db.Column(db.Text)
    address_2 = db.Column(db.Text)
    postal_code = db.Column(db.String(8))
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    type_of_user = db.Column(db.String(30), nullable=True)
    #created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        """Securely hash and store password"""
        self.password_hash = generate_password_hash(password)

    # NOTE: In a real application make sure to properly hash and salt passwords
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)   
     
    def to_dict(self):
        """Convert user object to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            #"password_hash": self.password_hash,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "country": self.country,
            "country_tel_code": self.country_tel_code,
            "phone_number": self.phone_number,
            "address": self.address,
            "address_2": self.address_2,
            "postal_code": self.postal_code,
            "confirmed": self.confirmed,
            "type_of_user": self.type_of_user,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def serialize_all(users):
        """Convert a list of user objects to a list of dictionaries."""
        return [user.to_dict() for user in users]
    
    @classmethod
    def get_by_id(cls, user_id: int) -> 'User':
        """Busca usuário por ID"""
        try:
            user = cls.query.get(user_id)
            if not user:
                raise RecordNotFoundError(f"Usuário com ID {user_id} não encontrado")
            return user
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar usuário {user_id}: {e}")
            raise DatabaseQueryError(f"Erro ao buscar usuário: {e}") from e
        
    def save(self) -> 'User':
        """
        Salva o usuário no banco de dados.
        
        Returns:
            User: Instância do usuário salvo
            
        Raises:
            DatabaseConnectionError: Erro de conexão com o banco
            DatabaseIntegrityError: Violação de integridade de dados
            UserAlreadyExistsError: Usuário já existe
            InvalidUserDataError: Dados do usuário inválidos
            DatabaseQueryError: Erro genérico de banco de dados
        """
        # Validação básica dos dados
        self._validate_user_data()
        
        try:
            # Verifica se usuário já existe (username ou email)
            if self._user_already_exists():
                raise UserAlreadyExistsError("Usuário já cadastrado no sistema")
            
            # Adiciona e commita a transação
            db.session.add(self)
            db.session.commit()
            
            logger.info(f"Usuário salvo com sucesso: ID {self.id}, Username: {self.username}")
            return self
            
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao salvar usuário {self.username}: {e}")
            
            # Detalhamento do erro de integridade
            if "unique" in str(e).lower() and "username" in str(e).lower():
                raise UserAlreadyExistsError("Username já está em uso") from e
            elif "unique" in str(e).lower() and "email" in str(e).lower():
                raise UserAlreadyExistsError("Email já está em uso") from e
            else:
                raise DatabaseIntegrityError(f"Erro de integridade de dados: {e.orig}") from e
                
        except OperationalError as e:
            db.session.rollback()
            logger.error(f"Erro de conexão ao salvar usuário {self.username}: {e}")
            raise DatabaseConnectionError("Falha na conexão com o banco de dados") from e
            
        except DataError as e:
            db.session.rollback()
            logger.error(f"Erro de dados ao salvar usuário {self.username}: {e}")
            raise InvalidUserDataError(f"Dados inválidos: {e.orig}") from e
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro genérico ao salvar usuário {self.username}: {e}")
            raise DatabaseQueryError(f"Erro ao salvar usuário: {e.orig}") from e

    def _validate_user_data(self) -> None:
        """Valida os dados básicos do usuário"""
        if not self.username or len(self.username.strip()) < 3:
            raise InvalidUserDataError("Username deve ter pelo menos 3 caracteres")
        
        if not self.email or '@' not in self.email:
            raise InvalidUserDataError("Email deve ser válido")
        
        if not self.password_hash or len(self.password_hash) < 6:
            raise InvalidUserDataError("Senha deve ter pelo menos 6 caracteres")

    def _user_already_exists(self) -> bool:
        """
        Verifica se já existe usuário com mesmo username ou email
        
        Returns:
            bool: True se usuário já existe, False caso contrário
        """
        try:
            existing_user = User.query.filter(
                or_(User.username == self.username, User.email == self.email, User.phone_number == self.phone_number)
            ).first()
            
            return existing_user is not None
            
        except SQLAlchemyError as e:
            logger.warning(f"Erro ao verificar usuário existente: {e}")
            # Não levanta exceção aqui, deixa o save() tratar possíveis duplicatas
            return False
        
    @classmethod
    def create_user(cls, username: str, email: str, password_hash: str) -> 'User':
        """
        Método factory para criar e salvar um novo usuário.
        
        Args:
            username: Nome de usuário
            email: Email do usuário
            password_hash: Hash da senha
            
        Returns:
            User: Instância do usuário criado
        """
        user = cls(username=username, email=email, password_hash=password_hash)
        return user.save()
    
    def update(self, **kwargs) -> 'User':
        """
        Atualiza os dados do usuário.
        
        Args:
            **kwargs: Campos para atualizar
            
        Returns:
            User: Instância do usuário atualizado
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        return self.save()
    
    def delete(self) -> None:
        """Remove usuário do banco de dados"""
        try:
            db.session.delete(self)
            db.session.commit()
            logger.info(f"Usuário {self.id} removido com sucesso")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao remover usuário {self.id}: {e}")
            raise DatabaseQueryError(f"Erro ao remover usuário: {e}") from e
