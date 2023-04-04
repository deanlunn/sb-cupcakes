"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from models import db, connect_db, Cupcake

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000/"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
app.config['SECRET_KEY'] = "secret"

with app.app_context():
    connect_db(app)
    db.create_all()


@app.route("/")
def root():
    """Homepage"""
    
    return render_template("index.html")


@app.route("/api/cupcakes")
def list_cupcakes():
    """Return all cupcakes"""
    
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add cupcake, return data about new cupcake"""
    
    data = request.json
    
    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None
    )
    
    db.session.add(cupcake)
    db.session.commit()
    
    return (jsonify(cupcake=cupcake.to_dict()), 201)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Return data on specific cupcake"""
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake from data in request. Return updated cupcake"""
    
    data = request.json
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']
    
    db.session.add(cupcake)
    db.session.commit()
    
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete cupcake from db and return confirm msg"""
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(message="Deleted")