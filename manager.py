# from flask import Flask
from flask_script import Manager
from markupsafe import escape
from cloudcc_api import create_app


# flask
# app = Flask(__name__)
app = create_app()

# flask script
manager = Manager(app=app)



if __name__ == '__main__':
    # flask
    # app.run(debug=True,port=8000,host="127.0.0.1",threaded=True)

    # flask script
    manager.run()

