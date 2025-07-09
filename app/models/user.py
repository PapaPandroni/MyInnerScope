from .database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Auto-increment ID
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    user_name = db.Column(db.String(200), nullable=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        # Only hash if not already hashed (avoid double-hashing)
        if plaintext_password and not plaintext_password.startswith('pbkdf2:'):
            self._password = generate_password_hash(plaintext_password)
        else:
            self._password = plaintext_password

    def check_password(self, plaintext_password):
        return check_password_hash(self._password, plaintext_password)

    def __repr__(self):
        return f'<User {self.email}>'