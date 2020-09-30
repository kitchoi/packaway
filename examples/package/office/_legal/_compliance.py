# This is allowed
from .. import _hours

# This is allowed
from .._accounting import api

# This is NOT allowed
from .._accounting import _booking
