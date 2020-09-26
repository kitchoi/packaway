from ._algorithm.api import has_enough, is_recent


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
    return has_enough(data["symptoms"]) and is_recent(data["days_since_onset"])
