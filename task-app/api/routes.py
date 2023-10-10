from flask import Blueprint, render_template, abort
from api.public.routes import api_public_blueprint
from api.private.routes import api_private_blueprint


api_blueprint = Blueprint('api_blueprint', __name__ )

api_blueprint.register_blueprint(api_public_blueprint,url_prefix="/public")
api_blueprint.register_blueprint(api_private_blueprint,url_prefix="/private")