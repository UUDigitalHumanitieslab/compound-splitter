from typing import Tuple
# from .splitter import list_methods, split

# # go through the methods
# methods = list_methods()

# go through the test data
# take the best scoring candidate for each

# calculate evaluation metrics

# precision recall
# word level: compound split is is either considered wrong or false
# sub-word level: whether the compound is split the same way (or too often, too little)
# sub-consideration: editing distance of splits perhaps? more complicated, but
# should give some nuance if a split is off by just one character it might be considered acceptable
# perhaps it should be a fuzzy passing grade
# So sub-word EXACT
# sub-word +1 tolerance
# sub-word +2 tolerance


def score(actual: str, expected: str) -> Tuple[int, int, int]:
    # TODO: tolerance for connectors
    actual_len = len(actual)
    expected_len = len(expected)

    actual_index = 0
    expected_index = 0

    false_negatives = 0
    false_positives = 0
    true_positives = 0

    while True:
        if actual_index >= actual_len:
            if expected_index == expected_len:
                # done processing!
                break
            else:
                raise Exception(f"Missaligned at actual index {actual_index}")
        elif expected_index >= expected_len:
            raise Exception(f"Missaligned at actual index {expected_index}")

        if actual[actual_index] == expected[expected_index]:
            if actual[actual_index] == "_":
                true_positives += 1
            actual_index += 1
            expected_index += 1
        elif actual[actual_index] == "_":
            false_positives += 1
            actual_index += 1
        elif expected[expected_index] == "_":
            false_negatives += 1
            expected_index += 1

    return false_negatives, \
        false_positives, \
        true_positives
