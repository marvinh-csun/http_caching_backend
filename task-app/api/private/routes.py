from flask import make_response,jsonify,request,Blueprint, render_template, abort
from sqlalchemy import text
from db import db
from flask_json import FlaskJSON, JsonError, json_response, as_json
import time
api_private_blueprint = Blueprint('api_private_blueprint', __name__ )
import hmac
import hashlib
import logging
@api_private_blueprint.route("")
def index():
    #shallow call generate the entire response
    #and if etag matches client it doesnt send response
    print("Shallow Call")
    print(request.headers)
    statement = text(
        """
        SELECT * FROM task LIMIT 500
        """
    )
    tasks = db.session.execute(statement,None)
    tasks_dict = [t._asdict() for t in tasks]
    data = jsonify(tasks_dict)
    hash_et = hashlib.md5(str(data).encode(),usedforsecurity=False).hexdigest()
    response = make_response(data)
    response.cache_control.must_revalidate = True
    response.cache_control.private = True
    response.cache_control.max_age = 60

    print("Anything")
    print(hash_et)
    print(request.if_none_match)
    response.set_etag(hash_et)

    if hash_et in request.if_none_match:
        print("etags match last api call")
        some_response = make_response("",304)
        some_response.cache_control.must_revalidate = True
        some_response.cache_control.private = True
        some_response.cache_control.max_age = 60

        some_response.set_etag(hash_et)
        return some_response

    return response

@api_private_blueprint.route("/last")
def last():
    last_statement = text(
        """
        SELECT MAX(updated_at) as LastUpdated FROM task
        """
    )
    last_updated_task = db.session.execute(last_statement, None).fetchone()
    last_updated_task = last_updated_task._asdict()

    hash_etag = hashlib.md5(str(last_updated_task['LastUpdated']).encode(),usedforsecurity=False).hexdigest()

    print(hash_etag)
    print("below is what we received from client request")
    print(request.if_none_match)

    print(request.headers)

    if hash_etag not in request.if_none_match:
        print("Record was updated etags dont match")

        statement = text(
            """
            SELECT * FROM task
            """
        )
        tasks = db.session.execute(statement,None)
        tasks_dict = [t._asdict() for t in tasks]

        some_response = make_response(jsonify(tasks_dict))
        some_response.cache_control.must_revalidate = True
        some_response.cache_control.public = True
        some_response.cache_control.max_age = 60

        some_response.set_etag(hash_etag)
        return some_response
    else:
        print("etags match last api call")
        some_response = make_response("",304)
        some_response.cache_control.must_revalidate = True
        some_response.cache_control.public = True
        some_response.cache_control.max_age = 60

        some_response.set_etag(hash_etag)
        return some_response
    
@api_private_blueprint.route("/search")
def search():
    since = request.if_modified_since
    
    page = int(request.args.get('page'))
    page_size = int(request.args.get('page_size'))
    task_name = request.args.get('task_name')

    if page==0:
        page = 1
    if page_size==0:
        page_size = 100

    if task_name is None:
        task_name = "" 

    statement = text(
        """
        SELECT * FROM task
        LIMIT
        :page_size
        OFFSET
        :page
        """
    )

    tasks = db.session.execute(statement,({
        "task_name": task_name,
        "page_size": page_size,
        "page": (page-1)*page_size
    }))

    tasks_dict = [t._asdict() for t in tasks]
    response = make_response(jsonify(tasks_dict))
    response.cache_control.public = True
    response.cache_control.max_age = 120
    response.cache_control.must_revalidate = True
    response.add_etag()
    print("Search Called page_size: " + str(page_size) + "page: " + str(page))
    return response