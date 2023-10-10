# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/')
# def hello():
# 	return "Hello World!"

# @app.route('/cache-me')
# def cache():
# 	return "nginx will cache this response"

# @app.route('/info')
# def info():

# 	resp = {
# 		'connecting_ip': request.headers['X-Real-IP'],
# 		'proxy_ip': request.headers['X-Forwarded-For'],
# 		'host': request.headers['Host'],
# 		'user-agent': request.headers['User-Agent']
# 	}

# 	return jsonify(resp)

# @app.route('/flask-health-check')
# def flask_health_check():
# 	return "success"

from flask import Flask
from db import db
from flask_cors import CORS
def create_app():
    app = Flask(__name__,template_folder='templates')
    CORS(app)
    from home.routes import home_blueprint
    from task.routes import task_blueprint
    from api.routes  import api_blueprint
    from flask_json import FlaskJSON
    import flask_json
    app.register_blueprint(home_blueprint)
    app.register_blueprint(task_blueprint,url_prefix="/task")
    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:example@mysql:3306/task_app'
    app.config['SECRET_KEY'] = 'CELCecalkecn'
    db.init_app(app)
    json = FlaskJSON()
    json.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0",debug=True, load_dotenv=True)