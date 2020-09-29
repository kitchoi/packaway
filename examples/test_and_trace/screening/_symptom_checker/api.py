from ._algorithm import api as _algorithm_api
from ._symptom_names import NAMES

# Bad import! Using private things!
from ._algorithm import _duration  # noqa: F401


def get_form():
    return {
        "symptoms": {
            "type": "zero or more",
            "options": NAMES,
        },
        "days_since_onset": {
            "type": "nonnegative integer",
        }
    }


def is_eligible(data):
    return (
        _algorithm_api.has_enough(data["symptoms"]) and
        _algorithm_api.is_recent(data["days_since_onset"])
    )
