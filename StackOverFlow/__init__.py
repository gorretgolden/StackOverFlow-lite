import imp
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint


#Application Factory Function
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    

    if test_config is None:
        # load the instance config, if it exists, when not testing
       app.config.from_mapping(
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY'),
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        CORS_HEADERS= 'Content-Type'
 
    )
    else:
        # load the test config if passed in , resources=r'/*'
        app.config.from_mapping(test_config)
    CORS(app,resources={r"/*": {"origins": "*"}})
    
  
    app.static_folder = 'static'
    
   
    from StackOverFlow.questions.routes import questions
    from StackOverFlow.auth.routes import auth
 
    #registering blueprints    
  
    app.register_blueprint(questions)
    app.register_blueprint(auth)
    
    JWTManager(app)
    
    SWAGGER_URL = "/api/docs"
    API_URL = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,API_URL,
    config={'app_name': "Fast Food First API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
   
    return app

