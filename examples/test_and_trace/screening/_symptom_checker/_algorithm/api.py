""" This package contains the algorithm for computing whether a person
is eligible for a test based on their symptoms.
"""


def has_enough(symptoms):
    return len(symptoms) > 0


def is_recent(days_since_onset):
    return 0 <= days_since_onset < 5
