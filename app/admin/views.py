from . import admin


@admin.route('/admin')
def hello():
    return "This is admin page"
