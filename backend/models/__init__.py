"""
Importing all models here ensures SQLAlchemy's Base.metadata is aware of
every table before create_all() is called in database/seed.py or main.py.
"""
from backend.models.user import User, RoleEnum  # noqa
from backend.models.student import Student  # noqa
from backend.models.teacher import Teacher  # noqa
from backend.models.class_model import ClassModel, ClassMember  # noqa
from backend.models.subject import Subject  # noqa
from backend.models.topic import Topic  # noqa
from backend.models.question import Question  # noqa
from backend.models.quiz import Quiz, QuizQuestion  # noqa
from backend.models.attempt import Attempt, Answer  # noqa
from backend.models.doubt import Doubt  # noqa
from backend.models.document import Document, DocumentChunk  # noqa
from backend.models.recommendation import StudentProgress, Recommendation  # noqa
