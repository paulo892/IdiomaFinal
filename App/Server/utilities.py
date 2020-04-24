from flask import Flask, jsonify, request, redirect, session, render_template
from flask.json import JSONEncoder
from flask_pymongo import PyMongo
from flask_cas import login_required, CAS, login, logout
from flask_cors import CORS
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware
import pymongo
from bson.json_util import dumps
import json
from urllib.parse import quote_plus
from pymongo.errors import ConnectionFailure
from flask import Flask, jsonify, request, redirect, session, render_template
from toposort import toposort, toposort_flatten
from joblib import load
import pickle
import numpy as np
import spacy
import sklearn

# topologically sorts argument dictionary
def top_sort_topics(top_dict):
    return toposort_flatten(top_dict)
