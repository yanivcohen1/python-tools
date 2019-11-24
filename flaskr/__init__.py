import os
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

app = None
# request.headers.get('your-header-name') // read from header parameters
# session.get("user_id") // read from session parameters
# request.args.get('username') // read from url parameters
# if request.method == "POST": // not mast
#        username = request.form.get("user_id") // read post parameters

# init      
def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    print('_init_.py')
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from flaskr import db

    db.init_app(app)

    # apply the blueprints to the app
    from flaskr import auth, blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    # add by yaniv for angular
    api = Api(app)
    CORS(app)
    # if Employees class is from file then 
    # from folderName import fileName
    # from .folder.folder import fileName //nested dir
    # from . import fileName //current dir
    # from ...folder.folder import fileName // three backwords dirs
    # fileName.className
    #api.add_resource(Employees, '/employees') # Route_1 
    #api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3
    #for angular
    from flaskr import employees
    app.register_blueprint(employees.bp)
    #end config
    return app

# add by yaniv for angular
class Employees(Resource):
    def get(self):
        return {'employees': [{'id':1, 'name':'Balram'},{'id':2, 'name':'Tom'}]} 

class Employees_Name(Resource):
    def get(self, employee_id):
        print('Employee id:' + employee_id)
        result = {'data': {'id':1, 'name':'Balram'}}
        return jsonify(result) 
