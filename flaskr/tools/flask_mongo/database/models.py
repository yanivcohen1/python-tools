from enum import Enum
from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

class Embed(db.EmbeddedDocument):
    name: str = db.StringField(default='yan')
    value: str = db.StringField(default='con')

class Movie(db.Document):
    name: str = db.StringField(required=True, unique=True)
    casts: list[str] = db.ListField(db.StringField(), required=True)
    genres: list[str]  = db.ListField(db.StringField(), required=True)
    #find=Movie.objects(embeds__match={ "name": "xxx", "value": "xxx" }) # and query in embedded fields
    embeds: list[Embed] = db.ListField(db.EmbeddedDocumentField(Embed))
    added_by = db.ReferenceField('User')

class Role(Enum):
    USER = 'user'
    SUPER_USER = 'super_user'
    ADMIN = 'admin'

class User(db.Document):
    email: str = db.EmailField(required=True, unique=True)
    password: str = db.StringField(required=True, min_length=6)
    role: Role = db.EnumField(Role, default=Role.USER)
    movies: list[Movie] = db.ListField(db.ReferenceField('Movie', reverse_delete_rule=db.PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
User.register_delete_rule(Movie, 'added_by', db.CASCADE)
