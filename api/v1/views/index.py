#!/usr/bin/python3
"""index"""

from api.v1.views import app_views
from flask import jsonify
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from models import storage


@app_views.route('/status', methods=["GET"], strict_slashes=False)
def status():
    """show the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=["GET"], strict_slashes=False)
def stats():
    """
    Endpoint that retrieves the number
      of each objects by type
    """
    object_counts = {}
    object_counts["amenities"] = storage.count(Amenity)
    object_counts["cities"] = storage.count(City)
    object_counts["places"] = storage.count(Place)
    object_counts["reviews"] = storage.count(Review)
    object_counts["states"] = storage.count(State)
    object_counts["users"] = storage.count(User)
    return jsonify(object_counts)
