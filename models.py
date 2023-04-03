"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE = "https://sallysbakingaddiction.com/wp-content/uploads/2017/06/moist-chocolate-cupcakes-5.jpg"

class Cupcake(db.Model):
    """Cupcake"""
    
    __tablename__ = "cupcakes"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable = False)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE)
    
    def to_dict(self):
        """Serialize cupcake to a dict"""
        
        return {
            "id": self.id,
            "flavor": self.flavor,
            "rating": self.rating,
            "size": self.size,
            "image": self.image,
        }
        
def connect_db(app):
    """Connect to DB"""
    
    db.app = app
    db.init_app(app)