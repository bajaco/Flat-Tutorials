from flask import jsonify
from . import app
from .models import User
from .models import Tag
from .models import Unpublished_Tutorial


@app.route('/', methods=['GET'])
def hello():
    user = User(auth0_id='FAKEAUTH0ID')
    user.insert()
    tag1 = Tag(name='Flask')
    tag1.insert()
    tag2 = Tag(name='Postgres')
    tag2.insert()
    tag3 = Tag(name='Docker')
    tag3.insert()
    tutorial = Unpublished_Tutorial(
            author_id=user.id,
            title='Great Tutorial with flask',
            text='The content of a great tutorial'
            )
    tutorial.tags.append(tag1)
    tutorial.tags.append(tag2)
    tutorial.tags.append(tag3)
    tutorial.insert()

    tutorial = user.unpublished
    return str(user.unpublished[0].author_id) + ' ' + ' '.join([str(tag.name) for tag in user.unpublished[0].tags])


   

