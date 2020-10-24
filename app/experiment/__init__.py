"""
Management of an experiment
"""
import os

from app.experiment.form import SettingsForm
from app.experiment.models import Experiment
from .models import Experiment
from config import Config
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from wtforms import SelectMultipleField, TextAreaField

experiment_page = Blueprint('experiment_page', __name__,
                            template_folder='templates',
                            static_folder='static')


@experiment_page.route('/', methods=['GET', 'POST'])
def new_experiment():
    """
    Creation of a new experiment
    """
    form = SettingsForm()

    for name, item in form.camera.settings.items():
        if item['type'] == 'list':
            tmpfield = SelectMultipleField( name,
                                            choices=[(value, effect) for effect, value in item['values'].items()],
                                            default=item['default'],
                                            coerce=int,
                                            description=name)
            setattr(form, name, tmpfield)

    actions = "new"
    exp = Experiment()

    if form.validate_on_submit():
        form.populate_obj(exp)
        exp.create()
        flash('Experience %s was added' % exp.expid, 'success')
    return render_template('experiment.html', form=form, exp=exp,
                            config=Config, actions=actions)


@experiment_page.route('/<expid>', methods=['GET', 'POST'])
def setuped_experiment(expid):
    """
    Edit an existing experiemnt

    Args:
      expid : str
        The experiment id

    GET: display
    POST: three action possible
       - edit
       - cancel
       - delete
    """
    try:
        exp = Experiment(directory=os.path.join(Config.WORKING_DIR, expid))
    except FileNotFoundError:
        abort(404)
    form = SettingsForm(obj=exp)
    if request.method == 'POST':
        if request.form['action'] == "edit":
            if form.validate_on_submit():
                form.populate_obj(exp)
                exp.create()
                flash('The experiment %s has been modified' % exp.expid, 'info')
        elif request.form['action'] == "cancel":
            exp.cancel()
            flash('The experiment %s has been canceled' % exp.expid, 'warning')
        elif request.form['action'] == "delete":
            exp.delete()
            flash('The experiment %s has been deleted' % exp.expid, 'danger')
            # return redirect(url_for('main_page.experiment_status'))
    if exp.status in ["ENDED", "Error", "Canceled"]:
        actions = "readonly"
    elif exp.status == "RUNNING":
        actions = "cancelable"
    else:
        actions = "editable"
    return render_template('experiment.html', form=form, exp=exp, config=Config,
                           actions=actions)
