from . import auth


@auth.route('/auth')
def hello():
    return 'This is auth page'
