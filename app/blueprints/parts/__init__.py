from flask import Blueprint

part_bp = Blueprint('part_bp', __name__)

from . import routes