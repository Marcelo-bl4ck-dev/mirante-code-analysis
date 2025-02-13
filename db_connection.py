from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import threading

class Database:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:  # Thread-safe singleton
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        self.engine = create_engine("sqlite:///analysis.db", echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.SessionLocal()

# Initialize the database singleton
db_instance = Database()
