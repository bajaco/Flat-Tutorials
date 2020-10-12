from flask import jsonify
from flask import abort
from . import app
from .models import *

# get all short form unpublished tutorials
@app.route('/unpublished', methods=['GET'])
def get_unpublished_list():
    query = Unpublished_Tutorial.query.all()
    result = [tut.short() for tut in query]
    return jsonify({
        'success': True,
        'tutorials': result
        }), 200
    
#get long form of unpublished tutorial
@app.route('/unpublished/<int:tutorial_id>', methods=['GET'])
def get_unpublished_tutorial(tutorial_id):
    result = Unpublished_Tutorial.query.get(tutorial_id).long()
    return jsonify({
        'success': True,
        'tutorial': result
    }), 200

#get all short form published tutorials
@app.route('/published', methods=['GET'])
def get_published_list():
    query = Published_Tutorial.query.all()
    result = [tut.short() for tut in query]
    return jsonify({
        'success': True,
        'tutorials': result
        }), 200

#get long form of published tutorial
@app.route('/published/<int:tutorial_id>', methods=['GET'])
def get_published_tutorial(tutorial_id):
    result = Published_Tutorial.query.get(tutorial_id).long()
    return jsonify({
        'success': True,
        'tutorial': result
    }), 200


#create or update published tutorial by copying unpublished
#returns newly published tutorial
@app.route('/publish/<int:tutorial_id>', methods=['GET'])
def publish(tutorial_id):
    unpublished = Unpublished_Tutorial.query.get(tutorial_id)
    published = Published_Tutorial.query.get(tutorial_id)
    
    #if it doesn't exist create it
    update = False
    if published:
        update = True
    else:
        published = Published_Tutorial(id=unpublished.id)
    
    #make updates
    published.author_id = unpublished.author_id
    published.title = unpublished.title
    published.text = unpublished.text
    published.tags = unpublished.tags
    
    #update or insert depending on whether it exists
    if update:
        published.update()
    else:
        published.insert()
    
    #return newly published tutorial
    result = Published_Tutorial.query.get(tutorial_id).long()
    return jsonify({
        'success': True,
        'updated': update,
        'tutorial': result
        }), 200


