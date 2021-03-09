from . import main


@main.route('/')
def hello():
    return 'This is the Feedback Forum.'
