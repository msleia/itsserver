from flask import Blueprint
from flask import Flask, render_template, Response, request, jsonify

from dao import DAO 
from entities import *

display_api = Blueprint('actions', __name__)
dao_obj = DAO()

@display_api.route('/display/<word>')
def push_word(word):
    pass
    
 