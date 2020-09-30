

# This is allowed
from ..person import api as person_api

# This is NOT allowed
from ..person import _reading

# This is allowed
from ._legal import api as legal_api

# This is NOT allowed
from ._legal import _compliance
