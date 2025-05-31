"""
The main views of the applications
"""

import markdown
from flask import Blueprint, abort, render_template
from jinja2 import Markup
from config import Config

help_page = Blueprint('help_page', __name__, template_folder='templates',
                      static_folder='static')


def md_filter(md_content):
    """
    Transform markdown to html through markdown

    Args:
      md_content: str
        the markdown source to transform
    """

    title = ""
    md_body = ""
    for line in md_content.split('\n'):
        # Extract title from first h1 if present
        if title == "" and line.startswith('# '):
            title = line[2:].strip()
        else:
            md_body = md_body + '\n' + line

    body_html = markdown.markdown(md_body, extensions=['attr_list', 'fenced_code'])

    return {
        'body': body_html,
        'title': title
    }


@help_page.route('/', methods=['GET'])
@help_page.route('/<page>', methods=['GET'])
def help(page=None):
    """
    Display a specific help page

    Args:
      page : str
        The page to display (a markdown file in doc subfolder)
    """
    if page is None:
        page = "index"
    try:
        with open("app/doc/%s.md" % page) as myfile:
            md_content = md_filter(myfile.read())
    except FileNotFoundError:
        abort(404)
    return render_template('help.html',
                           content=Markup(md_content['body']),
                           title=Markup(md_content['title']),
                           config=Config)
