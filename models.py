from sqlalchemy import create_engine, Column, Integer, String, Text, Date, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(SQLEnum('admin', 'employee', name='user_roles'), default='employee', nullable=False)
    leave_balance = Column(Integer, default=20, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to leave requests
    leave_requests = relationship('LeaveRequest', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class LeaveRequest(Base):
    __tablename__ = 'leave_requests'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(SQLEnum('Pending', 'Approved', 'Rejected', name='leave_status'), 
                    default='Pending', nullable=False)
    applied_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    days = Column(Integer, nullable=False)  # Number of leave days
    
    # Relationship to user
    user = relationship('User', back_populates='leave_requests')
    
    def calculate_days(self):
        """Calculate number of leave days"""
        delta = self.end_date - self.start_date
        return delta.days + 1  # Include both start and end date
    
    def __repr__(self):
        return f'<LeaveRequest {self.id} - {self.status}>'


# Database setup functions
def init_db(app):
    """Initialize database"""
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.create_all(engine)
    
    Session = scoped_session(sessionmaker(bind=engine))
    return Session


def get_db_session(app):
    """Get database session"""
    if not hasattr(app, 'db_session'):
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        Session = scoped_session(sessionmaker(bind=engine))
        app.db_session = Session
    return app.db_session()