from django.db import models
from .main_models import *
from .transport import *


def get_model_transport(model):
    if model == 'cars': return Cars


def get_model(category, model):
    if category == 'transport': return get_model_transport(model)
