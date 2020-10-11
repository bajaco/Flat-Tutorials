from src import app
from src.database.models import User

@app.route('/', methods=['GET'])
def hello():
    testing = User(username='Test_User', email='test@email')
    
    return ' '.join([str(user.id) + ' ' + user.username for user in User.query.all()])

