from wood import Wood
from wood.support import Blueprint

def make_example_blueprint():
    b = Blueprint()
    b.empty(r"/example","example")

    return b


def test_blueprint_can_add_empty_handler():
    b = make_example_blueprint()

    assert b != None


def test_blueprint_can_add_handlers_to_wood():
    w = Wood()
    b = make_example_blueprint()

    b.to(w)

    assert len(w.application.handlers) > 0


def test_blueprint_can_get_new_wood():
    b = make_example_blueprint()

    w.get_wood()

    assert len(w.application.handlers) > 0
