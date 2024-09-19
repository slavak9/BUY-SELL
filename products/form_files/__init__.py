from .transport import *


def get_form_transport(model):
    if model == 'cars': return CarsForm


def get_form(category, model):
    if category == 'transport': return get_form_transport(model)
