# This is allowed
from . import _reading

# This is NOT allowed
from ._reading import _private_name
