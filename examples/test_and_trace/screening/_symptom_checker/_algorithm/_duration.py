# packaway.name: test_and_trace.screening._symptom_checker._algorithm._duration

# This is okay
from test_and_trace.screening._symptom_checker._symptom_names import NAMES

# This is NOT okay.
from test_and_trace.screening._urgency_checker import _priority

# But this is okay
from test_and_trace.screening._urgency_checker import api

len(NAMES)
dir(_priority)
dir(api)
