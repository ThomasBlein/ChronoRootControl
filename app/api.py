"""
The API definitions
"""

import os
from flask import Blueprint, abort, jsonify, make_response, request

from app.experiment.models import Experiment
from app.experimentlist.models import ExperimentList
from config import Config

api_exp = Blueprint('api_exp', __name__, template_folder='templates',
                    static_folder='static')


@api_exp.route('', methods=['GET'])
def get_experiment_list():
    """
    Return the full list of experiments
    """
    exps = ExperimentList()
    return jsonify(exps.to_dict())


@api_exp.route('', methods=['POST'])
def create_experiment():
    """
    Create an experiment

    required fields:
        start, end, timepoint_nb and camera
    """
    if (not request.json or
            'start' not in request.json or
            'end' not in request.json or
            'timepoint_nb' not in request.json or
            'cameras' not in request.json):
        abort(400)
    exp = Experiment()
    exp.from_dict(request.json)
    exp.create()
    return jsonify(exp.to_dict()), 201


# Return the json of an experiment
@api_exp.route('/<expid>', methods=['GET'])
def get_experiment(expid):
    """
    Return an experiment

    Args:
      expid : str
        The id of the experiment
    """
    try:
        exp = Experiment(directory=os.path.join(Config.WORKING_DIR, expid))
    except FileNotFoundError:
        abort(404)
    return jsonify(exp.to_dict())


@api_exp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@api_exp.route('/<expid>', methods=['DELETE'])
def delete_experiment(expid):
    """
    Delete an experiment

    Args:
      expid : str
        The id of the experiment
    """
    try:
        exp = Experiment(directory=os.path.join(Config.WORKING_DIR, expid))
    except FileNotFoundError:
        abort(404)
    exp.delete()
    return jsonify({'result': True})


@api_exp.route('/<expid>', methods=['PUT'])
def update_experiment(expid):
    """
    Update an experiment

    Args:
      expid : str
        The id of the experiment
    """
    try:
        exp = Experiment(directory=os.path.join(Config.WORKING_DIR, expid))
    except FileNotFoundError:
        abort(404)
    exp.from_dict(request.json)
    exp.create()
    return jsonify(exp.to_dict())


@api_exp.route('/<expid>/cancel', methods=['GET'])
def cancel_experiment(expid):
    """
    Cancel an experiment

    Args:
      expid : str
        The id of the experiment
    """
    try:
        exp = Experiment(directory=os.path.join(Config.WORKING_DIR, expid))
    except FileNotFoundError:
        abort(404)
    exp.cancel()
    return jsonify(exp.to_dict())
