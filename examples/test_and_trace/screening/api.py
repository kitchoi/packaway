import test_and_trace.screening._symptom_checker.api as symptom_checker
import test_and_trace.screening._urgency_checker.api as urgency_checker


def get_form():
    return {
        "symptom": symptom_checker.get_form(),
        "urgency": urgency_checker.get_form(),
    }


def is_eligible(data):
    return (
        symptom_checker.is_eligible(data["symptom"]) and
        urgency_checker.is_eligible(data["urgency"])
    )
