from extensions import db

class Property(db.Model):
    __tablename__ = 'property'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # Title of the property
    description = db.Column(db.Text, nullable=False)   # Description of the property
    location = db.Column(db.String(100), nullable=False)  # Location of the property
    price = db.Column(db.Float, nullable=False)        # Price of the property
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)  # Owner's ID
    
    # Relationship to User model (assuming one owner per property)
    owner = db.relationship('User', backref='properties')  # Defines the owner relationship

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)       # Name of the user
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email, should be unique

    # Add any additional fields or relationships needed
