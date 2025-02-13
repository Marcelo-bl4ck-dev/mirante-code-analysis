from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import threading
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

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
        # Read the environment variables
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        
        # Construct the PostgreSQL connection string
        connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        # Create the engine
        self.engine = create_engine(connection_string, echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.SessionLocal()

# Initialize the database singleton
db_instance = Database()
