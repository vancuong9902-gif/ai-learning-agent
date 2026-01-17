from app.db.base_class import Base

# Import tất cả models để Base.metadata có đủ table
from app.models.user import User
from app.models.document import Document
from app.models.quiz import Quiz
from app.models.attempt import Attempt
from app.models.session import Session
