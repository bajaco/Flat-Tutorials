from flask import Blueprint
from flask import jsonify
from flask import request
from sqlalchemy import func
from .models import *
from .auth import requires_auth
from .auth import AuthError
from werkzeug.exceptions import abort
import requests
bp = Blueprint('views', __name__)

# Helper functions

# When called this will get userinformation to be used
# for context in various views. If the user is not present
# in the database it will be created.
def user_context(payload):
    a_id = payload['sub']
    user = User.query.filter_by(auth0_id=a_id).one_or_none()
    if not user:
        try:
            # Authorization is assumed to exist because user_context will
            # only be called within authorized endpoints.
            token = request.headers.get('Authorization', None).split()[1]
            
            user_url = 'https://agyx.auth0.com/userinfo'
            authorization = {'Authorization': 'Bearer {}'.format(token)}
            r = requests.get(url=user_url,headers=authorization)
            user_info = r.json()   
            user = User(
                    auth0_id=user_info['sub'],
                    username=user_info['sub'][:20]
                    )
            if 'email' in user_info:
                user.email = user_info['email']
            
            # This is a little atypical, but I want to use the user id in the
            # username to ensure it's unique. Auth0_id used as a temporary
            # placeholder until the id is created.
            user.insert()
            user.username=''.join(user_info['nickname'].split()) + '#' + str(user.id)
            user.update()
        except:
            abort(500)
    return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            }

###############
# OPEN ACCESS #
###############


#get all short form published tutorials
@bp.route('/published', methods=['GET'])
def get_published_list():
    query = Published_Tutorial.query.all()
    if not query:
        abort(404)
    result = [tut.short() for tut in query]
    return jsonify({
        'success': True,
        'tutorials': result
        }), 200

#get long form of published tutorial
@bp.route('/published/<int:tutorial_id>', methods=['GET'])
def get_published_tutorial(tutorial_id):
    result = Published_Tutorial.query.get_or_404(tutorial_id).long()
    return jsonify({
        'success': True,
        'tutorial': result
    }), 200


#get all short form published tutorials from specific user
@bp.route('/published/by-author/<int:author_id>', methods=['GET'])
def get_published_list_by_author(author_id):
    tutorials = User.query.get_or_404(author_id).published
    if len(tutorials) == 0:
        abort(404)
    result = [tut.short() for tut in tutorials]
    return jsonify({
        'success': True,
        'tutorials': result
        }), 200

#get all shortform list by tag
@bp.route('/published/tags/<string:tag>', methods=['GET'])
def get_published_by_tag(tag):
    tutorials = Tag.query.filter(func.lower(Tag.name) == tag.lower()).first_or_404().published_tutorials
    if not tutorials:
        abort(404)
    result = [tut.short() for tut in tutorials]
    return jsonify({
        'success': True,
        'tutorials': result
        }), 200

#get all shortform list by tags
@bp.route('/published/tags/<string:tag1>/<string:tag2>', methods=['GET'])
def get_published_by_tags(tag1,tag2):
    res1 = Tag.query.filter(func.lower(Tag.name) == tag1.lower()).first_or_404().published_tutorials
    res2 = Tag.query.filter(func.lower(Tag.name) == tag2.lower()).first_or_404().published_tutorials
    tutorials = [tut for tut in res1 if tut in res2]
    if not tutorials:
        abort(404)
    result = [tut.short() for tut in tutorials]
    return jsonify({
        'success': True,
        'tutorials': result
        }), 200 
   

###################
# REGISTERED USER #
###################

#For regular user:
#submit tutorial
@bp.route('/submit', methods=['POST'])
@requires_auth('submit:tutorial')
def submit(payload):
    context = user_context(payload)
    try:
        data = request.get_json()
        tutorial = Unpublished_Tutorial(
                author_id=context['id'],
                title=data.get('title'),
                text=data.get('text'),
                under_review=True,
                published=False
                )
        if data.get('tags'):
            for tag_name in data.get('tags').split(', '):
                tag = Tag.query.filter_by(name=tag_name).one_or_none()
                if not tag:
                    tag = Tag(name=tag_name)
                    tag.insert()
                tutorial.tags.append(tag)
        tutorial.insert()
        result = tutorial.long()
    except:
        abort(500)
    return jsonify({
        'success': True,
        'user_id': tutorial.author_id,
        'tutorial': result
    }), 200

#edit and resubmit tutorial
@bp.route('/edit/<int:tutorial_id>', methods=['PATCH'])
@requires_auth('edit:tutorial')
def edit(payload, tutorial_id):
    context = user_context(payload)
    data = request.get_json()
    tutorial = Unpublished_Tutorial.query.get_or_404(tutorial_id)
    if tutorial.author_id != int(context['id']):
        abort(403)
    try:
        tutorial.title = data.get('title')
        tutorial.text = data.get('text')
        tutorial.under_review=True
        tutorial.tags.clear()
        if data.get('tags'):
            for tag_name in data.get('tags').split(', '):
                tag = Tag.query.filter_by(name=tag_name).one_or_none()
                if not tag:
                    tag = Tag(name=tag_name)
                    tag.insert()
                tutorial.tags.append(tag)
        tutorial.update()
    except:
        abort(500)

    result = tutorial.long()
    return jsonify({
        'success': True,
        'tutorial': result
        }),200

# Get short form submitted tutorials
@bp.route('/submitted', methods=['GET'])
@requires_auth('submit:tutorial')
def get_submitted_list(payload):
    context = user_context(payload)
    tutorials = Unpublished_Tutorial.query.filter_by(author_id=context['id']).all()
    result = [tutorial.short() for tutorial in tutorials]
    return jsonify({
        'success': True,
        'tutorials': result
        }), 200 
    
# Get long form submitted tutorial
@bp.route('/submitted/<int:tutorial_id>', methods=['GET'])
@requires_auth('submit:tutorial')
def get_submitted_tutorial(payload, tutorial_id):
    context = user_context(payload)
    tutorial = Unpublished_Tutorial.query.get_or_404(tutorial_id)
    result = tutorial.long()
    if context['id'] != result['author_id']:
        abort(403)
    return jsonify({
        'success': True,
        'tutorial': result
        }), 200 
 
##############
# MODERATION #
##############

# get all short form unpublished tutorials
# Only returns tutorials not yet published
# since they were last changed.
@bp.route('/unpublished', methods=['GET'])
@requires_auth('view:unpublished_list')
def get_unpublished_list(payload):
    context = user_context(payload)
    query = Unpublished_Tutorial.query.filter_by(under_review=True).all()
    if not query:
        abort(404)
    result = [tut.short() for tut in query]
    
    return jsonify({
        'success': True,
        'tutorials': result
        }), 200 
    
#get long form of unpublished tutorial
@bp.route('/unpublished/<int:tutorial_id>', methods=['GET'])
@requires_auth('view:unpublished')
def get_unpublished_tutorial(payload,tutorial_id):
    context = user_context(payload)
    query = Unpublished_Tutorial.query.get_or_404(tutorial_id)
    result = query.long()
    return jsonify({
        'success': True,
        'tutorial': result
    }), 200

#create or update published tutorial by copying unpublished
#returns newly published tutorial
@bp.route('/publish/<int:tutorial_id>', methods=['GET'])
@requires_auth('approve:tutorial')
def publish(payload, tutorial_id):
    context = user_context(payload)
    unpublished = Unpublished_Tutorial.query.get_or_404(tutorial_id)
    
    #No or_404 because we are testing for None
    published = Published_Tutorial.query.get(tutorial_id)
    
    try:
        # If it doesn't exist create it
        # Update flag notes whether the tutorial is being published
        # for the first time or simply updated.
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
        unpublished.under_review = False
        unpublished.published = True
        unpublished.update()
        
        #update or insert depending on whether it exists
        if update:
            published.update()
        else:
            published.insert()
    except:
        abort(500)
    
    #return newly published tutorial
    result = Published_Tutorial.query.get_or_404(tutorial_id).long()
    return jsonify({
        'success': True,
        'updated': update,
        'tutorial': result
        }), 200

# Deny a tutorial from being published due to content or 
# quality concerns.
@bp.route('/deny/<int:tutorial_id>', methods=['PATCH'])
@requires_auth('deny:tutorial')
def deny(payload, tutorial_id):
    context = user_context(payload)
    data = request.get_json()
    tutorial = Unpublished_Tutorial.query.get_or_404(tutorial_id)
    try:
        tutorial.reviewer_notes = data.get('reviewer_notes')
        tutorial.under_review = False
        tutorial.update()
    except:
        abort(500)
    return jsonify({
        'success': True,
        'denied_id': tutorial.id,
        'reviewer_notes': data.get('reviewer_notes')
        }),200


##################
# ADMINISTRATION #
##################

#list users
@bp.route('/admin/users', methods=['GET'])
@requires_auth('list:users')
def list_users(payload):
    context = user_context(payload)
    try:
        users = User.query.all()
        if len(users) == 0:
            abort(404)
        result = [user.description() for user in users]
        return jsonify({
            'success': True,
            'users': result
            }), 200
    except:
        abort(500)

# delete tutorial
# The reason for this atypical endpoint is that it deletes both
# published and unpublished tutorials
@bp.route('/admin/tutorial/<int:tutorial_id>', methods=['DELETE'])
@requires_auth('delete:tutorial')
def delete_tutorial(payload,tutorial_id):
    context = user_context(payload)
    unpublished = Unpublished_Tutorial.query.get_or_404(tutorial_id)
    published = Published_Tutorial.query.get_or_404(tutorial_id)
    try:
        unpublished.delete()
        published.delete()
        return jsonify({
            'success': True,
            'deleted_id': tutorial_id
            }), 200
    except:
        abort(500)

# Unpublish tutorial.
# Similar to delete tutorial but does not delete the unpublished version.
@bp.route('/admin/unpublish/<int:tutorial_id>', methods=['PATCH'])
@requires_auth('unpublish:tutorial')
def unpublish_tutorial(payload,tutorial_id):
    context = user_context(payload)
    data = request.get_json()
    published_tutorial = Published_Tutorial.query.get_or_404(tutorial_id)
    unpublished_tutorial = Unpublished_Tutorial.query.get_or_404(tutorial_id)
    try:
        published_tutorial.delete()

        # Add notes to unpublished tutorial to inform user why it was deleted.
        unpublished_tutorial.reviewer_notes = data.get('reviewer_notes')
        unpublished_tutorial.update()
    except:
        abort(500)

    return jsonify({
        'success': True,
        'unpublished_id': unpublished_tutorial.id,
        'reviewer_notes': data.get('reviewer_notes')
        }), 200
