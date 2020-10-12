from flask import jsonify
from flask import abort
from . import app
from .models import *

#######################
# ACCESSING TUTORIALS #
#######################


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


#get all short form published tutorials from specific user
@app.route('/published/by-author/<int:author_id>', methods=['GET'])
def get_published_list_by_author(author_id):
    tutorials = User.query.get(author_id).published
    result = [tut.short() for tut in tutorials]
    return jsonify({
        'success': True,
        'tutorials': result
        }), 200

#get all shortform list by tag
@app.route('/published/tags/<string:tag>', methods=['GET'])
def get_published_by_tag(tag):
    search = "%{}%".format(tag)
    tutorials = Tag.query.filter(Tag.name.ilike(search)).first().published_tutorials
    result = [tut.short() for tut in tutorials]
    return jsonify({
        'success': True,
        'tutorials': result
        }), 200

#get all shortform list by tags
@app.route('/published/tags/<string:tag1>/<string:tag2>', methods=['GET'])
def get_published_by_tags(tag1,tag2):
    search1 = "%{}%".format(tag1)
    search2 = "%{}%".format(tag2)
    
    #Not happy about this, but flask-sqlalchemy does not seem to allow
    #calling ilike on a relationship: no way to call on Published_Tutorial.tags
    res1 = Tag.query.filter(Tag.name.ilike(search1)).first().published_tutorials
    res2 = Tag.query.filter(Tag.name.ilike(search2)).first().published_tutorials
    tutorials = [tut for tut in res1 if tut in res2]
  
    result = [tut.short() for tut in tutorials]
    return jsonify({
        'success': True,
        'tutorials': result
        }), 200 
   

########################
# PUBLISHING TUTORIALS #
########################

#For regular user:
#submit tutorial
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    tutorial = Unpublished_Tutorial(
            author_id=data.get('author_id'),
            title=data.get('title'),
            text=data.get('text')
            )
    for tag in data.get('tags'):
        dbtag = Tag.query.filter(str(Tag.name).lower() == tag.lower()).one_or_none()
        if not dbtag:
            dbtag = Tag(name=tag)
        tutorial.tags.append(dbtag)
    tutorial.insert()
            
#For Admin/Moderator:
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


