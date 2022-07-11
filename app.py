"""Flask app for Cupcakes"""
from crypt import methods
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "don't touch"

connect_db(app)

@app.route('/')
def root():
    """Homepage"""
    return render_template("index.html")

@app.route("/api/cupcakes")
def list_cupcakes():
    """Return cupcakes in system.
    Return JSON like:
        {cupcakes: [{id, flavor, rating, size, image
    """

    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add cupcake and return data about new cupcakes.
    Return JSON like:
        {cupcakes: [{id, flavor, rating, size, image
    """
    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)
        
    db.session.add(cupcake)
    db.session.commit()

    # POST should return HTTP status of 201 
    return(jsonify(cupcake=cupcake.to_dict()), 201)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Return data on specific cupcake.
    Return JSON like:
        {cupcakes: [{id, flavor, rating, size, image
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake and return data about new cupcakes.
    Return JSON like:
        {cupcakes: [{id, flavor, rating, size, image
    """

    data = request.json
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data["flavor"],
    cupcake.rating = data["rating"],
    cupcake.size = data["size"],
    cupcake.image = data["image"]

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"]) 
def remove_cupcake(cupcake_id):
    """Delete cupcake and return comfirmation message.
    Return JSON of { message: "Deleted"
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id) 

    db.session.delete(cupcake)
    db.session.commit() 

    return jsonify(message='Deleted')