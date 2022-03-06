from flask import Blueprint, abort


admin = Blueprint('admin', __name__)


@admin.route('/does-not-exist')
def disqus():
    """Specifically needed for disqus"""
    abort(404)


@admin.route('/hello')
def hello():
    """Hello page"""
    return "Hello World!"
