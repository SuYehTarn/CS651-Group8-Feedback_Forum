"""Module of the Admin blueprint
"""
from flask import Blueprint

admin = Blueprint('admin', __name__)

from app.admin import views
