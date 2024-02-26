#!/usr/bin/python3
"""Views for city"""

from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route(
    '/states/<state_id>/cities', methods=['GET'])
def list_cities(state_id):
    """
    retrieve the list of all city
    """
    city_list = []
    state = storage.get(State, state_id)
    if state:
        for city in state.cities:
            city_list.append(city.to_dict())
        return jsonify(city_list)

    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def show_city(city_id):
    """
    Retrieve just one city
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    delete a city
    """
    city = storage.get("City", city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}, 200)
    else:
        abort(404)


@app_views.route(
    '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    create a city
    """
    error_message = ""
    state = storage.get(State, state_id)
    if state:
        content = request.get_json()
        if isinstance(content, dict):
            if "name" in content.keys():
                city = City(**content)
                setattr(city, "state_id", state_id)
                storage.new(city)
                storage.save()
                response = jsonify(city.to_dict())
                response.status_code = 201
                return response
            else:
                error_message = "Missing name"
        else:
            error_message = "Not a JSON"
        response = jsonify({"error": error_message})
        response.status_code = 400
        return response
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    update a city
    """
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    city = storage.get(City, city_id)
    if city:
        content = request.get_json()
        if isinstance(content, dict):
            for key, value in content.items():
                if key not in ignore:
                    setattr(city, key, value)
            storage.save()
            return jsonify(city.to_dict())
        else:
            response = jsonify({"error": "Not a JSON"})
            response.status_code = 400
            return response
    else:
        abort(404)
