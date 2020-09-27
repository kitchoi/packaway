from ._algorithm import api as _algorithm_api


def get_form():
    return {
        "symptoms": {
            "type": "zero or more",
            "options": ["headache", "cough", "loss of smell"],
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
