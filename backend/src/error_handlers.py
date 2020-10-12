    
from flask import Blueprint
from flask import jsonify
bp = Blueprint('error_handlers', __name__)

@bp.app_errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
        })

@bp.app_errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
        })

@bp.app_errorhandler(500)
def internal_server_error(error):
    #db.session.rollback()
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
        })


