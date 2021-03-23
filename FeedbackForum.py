"""The entry module of the web app
"""

import os
import click
from app import create_app, db
from app.models.feedback import Feedback
from app.models.administrator import Administrator
from app.models.review_status import ReviewStatus


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app_context = app.app_context()
app_context.push()
db.create_all()


@app.shell_context_processor
def make_shell_context():
    """Set the environment for Flask shell"""
    return dict(db=db, Feedback=Feedback,
                ReviewStatus=ReviewStatus,
                Administrator=Administrator)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
