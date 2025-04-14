from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Import models
from .user import User
from .table_definition import TableDefinition
from .field_definition import FieldDefinition
from .menu_item import MenuItem 