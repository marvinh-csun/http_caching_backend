from flask import Blueprint, render_template, abort

home_blueprint = Blueprint('home_blueprint', __name__, template_folder='templates')

@home_blueprint.route("/")
@home_blueprint.route("/home")
def index():
    return render_template("home/index.html")