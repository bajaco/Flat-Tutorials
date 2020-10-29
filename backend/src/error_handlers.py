    
from flask import Blueprint
from flask import jsonify
from .auth import AuthError
bp = Blueprint('error_handlers', __name__)

@bp.app_errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'resource is forbidden'
        }), 403

@bp.app_errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'unauthorized'
        }), 401


@bp.app_errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
        }), 404

@bp.app_errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
        }), 405

@bp.app_errorhandler(500)
def internal_server_error(error):
    #db.session.rollback()
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
        }), 500


