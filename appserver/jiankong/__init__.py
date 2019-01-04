from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
#app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/static')

print(app.root_path)  #D:\webauth\appserver\jiankong
print(app.static_folder) #D:\webauth\appserver\jiankong\static
print(app.static_url_path) #/static

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/monitor.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.debug=True
db = SQLAlchemy(app)

from jiankong.views.usersview import user
app.register_blueprint(user)

