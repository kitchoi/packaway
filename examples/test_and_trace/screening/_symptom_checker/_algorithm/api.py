""" This package contains the algorithm for computing whether a person
is eligible for a test based on their symptoms.
"""

from .._symptom_names import NAMES


def has_enough(symptoms):
    return sum(symptom in NAMES for symptom in symptoms) > 0


def is_recent(days_since_onset):
    return 0 <= days_since_onset < 5
