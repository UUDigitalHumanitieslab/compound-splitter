import csv
import os
from math import nan
from typing import Tuple, List
from .splitter import get_method, list_methods

COMPOUND_SPLIT_CHAR = "_"


def compare_methods():
    for test_set_name, test_set in read_test_sets():
        stats = list(evaluate_methods(test_set))
        stats.sort(key=lambda item: item["accuracy"], reverse=True)

        for stat in stats:
            stat["test_set"] = test_set_name
        yield test_set_name, stats


def read_test_sets():
    dirname = os.path.dirname(__file__)
    test_sets_dir = os.path.join(dirname, "..", "test_sets")
    for test_set_name in os.listdir(test_sets_dir):
        test_set = []
        with open(os.path.join(test_sets_dir, test_set_name)) as csvfile:
            test_reader = csv.DictReader(csvfile)
            for row in test_reader:
                test_set.append((row["compound"], row["expected"]))

        yield test_set_name, test_set


def evaluate_methods(test_set: List[Tuple[str, str]]):
    methods = list_methods()
    for method in methods:
        method_name = method["name"]
        yield {
            **method,
            **evaluate_method(method_name, test_set)
        }


def evaluate_method(method_name: str, test_set: List[Tuple[str, str]]):
    method = get_method(method_name)

    # number of correctly passed through words
    # i.e. words which weren't split and should not have been split
    passed_correctly = 0

    splitted_correctly = 0  # number of correctly split words
    splitted_incorrectly = 0  # number of words which were splitted
    compounds = 0  # number of compounds in the test set

    for compound, expected in test_set:
        candidates = method.split(compound)["candidates"]
        highest_score = 0
        best_candidate = None
        for candidate in candidates:
            if candidate["score"] >= highest_score:
                best_candidate = candidate

        if best_candidate == None:
            # Nothing returned! Evaluate as if nothing was split
            actual = compound
        else:
            actual = str.join(COMPOUND_SPLIT_CHAR, best_candidate["parts"])

        false_negatives, false_positives, true_positives = score(
            actual, expected)

        if not false_negatives and not false_positives:
            if true_positives:
                splitted_correctly += 1
            else:
                passed_correctly += 1
        if true_positives or false_positives:
            splitted_incorrectly += 1
        if true_positives or false_negatives:
            compounds += 1

    splitted = splitted_correctly + splitted_incorrectly

    # TODO:
    # precision recall
    # word level: compound split is is either considered wrong or false
    # sub-word level: whether the compound is split the same way (or too often, too little)
    # sub-consideration: editing distance of splits perhaps? more complicated, but
    # should give some nuance if a split is off by just one character it might be considered acceptable
    # perhaps it should be a fuzzy passing grade
    # So sub-word EXACT
    # sub-word +1 tolerance
    # sub-word +2 tolerance

    return {
        "precision": splitted_correctly / splitted if splitted else nan,
        "recall": splitted_correctly / compounds if compounds else nan,
        "accuracy": (passed_correctly + splitted_correctly) / len(test_set)
    }


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
                raise Exception(f"Misaligned at actual index {actual_index}")
        elif expected_index >= expected_len:
            raise Exception(f"Misaligned at actual index {expected_index}")

        if actual[actual_index] == expected[expected_index]:
            if actual[actual_index] == COMPOUND_SPLIT_CHAR:
                true_positives += 1
            actual_index += 1
            expected_index += 1
        elif actual[actual_index] == COMPOUND_SPLIT_CHAR:
            false_positives += 1
            actual_index += 1
        elif expected[expected_index] == COMPOUND_SPLIT_CHAR:
            false_negatives += 1
            expected_index += 1

    return false_negatives, \
        false_positives, \
        true_positives


if __name__ == '__main__':
    for test_set_name, stats in compare_methods():
        print(f"=== TEST SET {test_set_name} ===")
        for stat in stats:
            precision = stat["precision"]
            recall = stat["recall"]
            accuracy = stat["accuracy"]
            print("Method:    " + stat["displayName"])
            print("F1:        " + str(2 * (precision*recall) / (precision+recall)))
            print(f"Precision: {precision}")
            print(f"Recall:    {recall}")
            print(f"Accuracy:  {accuracy}\n\n")
