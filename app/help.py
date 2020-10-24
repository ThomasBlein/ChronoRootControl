"""
The main views of the applications
"""

from docutils.core import publish_parts
from flask import Blueprint, abort, render_template
from jinja2 import Markup
from config import Config

help_page = Blueprint('help_page', __name__, template_folder='templates',
                      static_folder='static')


def rst_filter(rst):
    """
    Transform rst to html through docutils

    Args:
      rst: str
        the rst source to transform
    """
    return publish_parts( source=rst,
                          writer_name='html',
                          settings_overrides={"initial_header_level": 2}
                         )


@help_page.route('/', methods=['GET'])
@help_page.route('/<page>', methods=['GET'])
def help(page=None):
    """
    Display a specific help page

    Args:
      page : str
        The page to display (a rst file in doc subfolder)
    """
    if page is None:
        page = "index"
    try:
        with open("app/doc/%s.rst" % page) as myfile:
            rst_content = rst_filter(myfile.read())
    except FileNotFoundError:
        abort(404)
    return render_template('help.html',
                           content=Markup(rst_content['body']),
                           title=Markup(rst_content['title']),
                           subtitle=Markup(rst_content['subtitle']),
                           config=Config)
