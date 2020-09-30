# This is allowed.
from . import _reading

# This is not allowed
from ._reading import _private_name
