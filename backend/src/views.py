from . import app
from .models import User

@app.route('/', methods=['GET'])
def hello():
    testing = User(username='Test_User', email='test@email')
    testing.insert() 
    return ' '.join([str(user.id) + ' ' + user.username for user in User.query.all()])

