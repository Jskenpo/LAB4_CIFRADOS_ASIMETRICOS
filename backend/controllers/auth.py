import hashlib
import jwt
from datetime import datetime, timedelta

from backend.database import db, User
from backend.controllers.keys import generate_rsa_keys, generate_ecc_keys

SECRET_KEY = "clave_secreta_super_segura"

def _hash_password(password: str) -> str:
    """Hashea la contraseña con SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def _generate_jwt_token(user: User) -> str:
    """Genera un JWT con el ID del usuario y una expiración de 1 hora."""
    payload = {
        "user_id": user.email,
        "exp": datetime.now() + timedelta(hours=1),
        "iat": datetime.now(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def get_user_by_email(email: str) -> User:
    """Obtiene un usuario por su correo electrónico."""
    with db.read() as session:
        return session.query(User).filter_by(email=email).first()


def register(email: str, password: str) -> User:
    """Crea un nuevo usuario con la contraseña hasheada usando SHA-256."""
    hashed_password = _hash_password(password)
    with db.write() as session:
        user = User(email=email, password=hashed_password)
        session.add(user)
        session.commit()
        return user


def login(email: str, password: str, key_type: str = "RSA") -> tuple[str, str, str]:
    """Inicia sesión y genera un par de claves si el usuario no tiene una."""
    with db.write() as session:  # Abre sesión de escritura desde el inicio
        user = session.query(User).filter_by(email=email).first()

        if not user or user.password != _hash_password(password):
            return "", "", ""

        private_key = ""
        if not user.public_key:
            private_key, public_key = (
                generate_rsa_keys() if key_type == "RSA" else generate_ecc_keys()
            )
            user.public_key = public_key  # Ahora está vinculado a la sesión activa
            session.commit()  # Guarda cambios en la BD

        return user.email, _generate_jwt_token(user), private_key  # La clave privada solo se genera una vez





if __name__ == "__main__":
    # Test the functions
    try:
        register(email="test@email.com", password="password123")
    except Exception as e:
        print(f"Error creating user: {e}")

    print(login(email="test@email.com", password="password123"))
