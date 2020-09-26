from ._symptom_checker import api as symptom_checker_api
from ._urgency_checker import api as urgency_checker_api


def get_form():
    return {
        "symptom": symptom_checker_api.get_form(),
        "urgency": urgency_checker_api.get_form(),
    }


def is_eligible(data):
    return (
        symptom_checker_api.is_eligible(data["symptom"]) and
        urgency_checker_api.is_eligible(data["urgency"])
    )
