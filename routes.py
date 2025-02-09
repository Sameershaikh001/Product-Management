from flask import Blueprint
from app import app

product_routes = Blueprint('product_routes', __name__)

@app.route('/')
def home():
    return "Welcome to Product Management System"
