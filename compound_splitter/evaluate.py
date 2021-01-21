import csv
import os
from math import nan
from typing import Tuple, List
from .splitter import get_method, list_methods

COMPOUND_SPLIT_CHAR = "_"
COMPOUND_INFIX_TOLERANCE = 4


class MisalignedError(Exception):
    pass


def compare_methods():
    for test_set_name, test_set in read_test_sets():
        stats = list(evaluate_methods(test_set))
        stats.sort(key=lambda item: item["accuracy"], reverse=True)

        for stat in stats:
            stat["test_set"] = test_set_name

        yield test_set_name, test_set, stats


def read_test_sets():
    dirname = os.path.dirname(__file__)
    test_sets_dir = os.path.join(dirname, "..", "test_sets")
    for test_set_name in os.listdir(test_sets_dir):
        if not test_set_name.endswith(".csv"):
            continue
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


def split(method, compound: str) -> str:
    candidates = method.split(compound)["candidates"]
    highest_score = 0
    best_candidate = None
    for candidate in candidates:
        if candidate["score"] >= highest_score:
            best_candidate = candidate
            highest_score = candidate["score"]

    if best_candidate is None:
        # Nothing returned! Evaluate as if nothing was split
        return compound
    else:
        return str.join(COMPOUND_SPLIT_CHAR, best_candidate["parts"])


def evaluate_method(method_name: str, test_set: List[Tuple[str, str]]):
    method = get_method(method_name)
    print("METHOD:", method_name)
    method.start()
    skipped = 0
    splits = []
    try:
        # number of correctly passed through words
        # i.e. words which weren't split and should not have been split
        passed_correctly = 0

        splitted_correctly = 0  # number of correctly split words
        splitted_incorrectly = 0  # number of words which were splitted
        compounds = 0  # number of compounds in the test set

        for compound, expected in test_set:
            actual = split(method, compound)

            splits.append(actual)

            try:
                false_negatives, false_positives, true_positives = score(
                    actual, expected)

                if not false_negatives and not false_positives:
                    if true_positives:
                        splitted_correctly += 1
                    else:
                        passed_correctly += 1
                if false_positives:
                    splitted_incorrectly += 1
                if true_positives or false_negatives:
                    compounds += 1
            except MisalignedError as e:
                skipped += 1
                print(e)

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
    finally:
        method.stop()

    return {
        "precision": splitted_correctly / splitted if splitted else nan,
        "recall": splitted_correctly / compounds if compounds else nan,
        "accuracy": (passed_correctly + splitted_correctly) / len(test_set),
        "splits": splits,
        "skipped": skipped
    }


def score(actual: str, expected: str) -> Tuple[int, int, int]:  # noqa: C901
    actual_len = len(actual)
    expected_len = len(expected)

    actual_index = 0
    expected_index = 0

    false_negatives = 0
    false_positives = 0
    true_positives = 0

    misalignment_tolerance = COMPOUND_INFIX_TOLERANCE

    while True:
        if actual_index >= actual_len:
            if expected_index == expected_len:
                # done processing!
                break
            else:
                raise MisalignedError(
                    f"Misaligned A ({actual}:{actual_index},{expected}:{expected_index})")
        elif expected_index >= expected_len:
            raise MisalignedError(
                f"Misaligned B ({actual}:{actual_index},{expected}:{expected_index})")

        if actual[actual_index] == expected[expected_index]:
            misalignment_tolerance = COMPOUND_INFIX_TOLERANCE
            if actual[actual_index] == COMPOUND_SPLIT_CHAR:
                true_positives += 1
            actual_index += 1
            expected_index += 1
        elif actual[actual_index] == COMPOUND_SPLIT_CHAR:
            # lookahead in the expected to allow for some tolerance
            # TODO: only in the ending of a compound part
            infix_jump = infix_index(
                actual[actual_index+1], expected[expected_index:])
            if infix_jump:
                true_positives += 1
                expected_index += infix_jump
            else:
                false_positives += 1
            actual_index += 1
        elif expected[expected_index] == COMPOUND_SPLIT_CHAR:
            infix_jump = infix_index(
                expected[expected_index+1], actual[actual_index:])
            if infix_jump:
                true_positives += 1
                actual_index += infix_jump
            else:
                false_negatives += 1
            expected_index += 1
        else:
            misalignment_tolerance -= 1
            if misalignment_tolerance <= 0:
                raise MisalignedError(
                    f"Misaligned C ({actual}:{actual_index},{expected}:{expected_index})")
            else:
                actual_index += 1
                expected_index += 1

    return false_negatives, \
        false_positives, \
        true_positives


def infix_index(start_char: str, candidate: str) -> int:
    """

    Parameters
    ----------
    start_char
        Starting character of the next compound part
    candidate
        Candidate splitted string to look for a split
        followed by the next compound part

    Returns
    -------
    int
        The position of the start of the next compound part
        or 0 if none is found.
    """
    for i in range(0, min(len(candidate) - 1, COMPOUND_INFIX_TOLERANCE)):
        if candidate[i] == COMPOUND_SPLIT_CHAR:
            if candidate[i+1] == start_char:
                return i+1
            else:
                return 0
    return 0


def splits_table(test_set, stats):
    """
    Prints a table with the actual splits applied
    by each method and the input and reference split.
    """
    headers = ["Input", "Gold Standard"]
    for stat in stats:
        headers.append(stat["displayName"])

    rows = [headers]

    i = 0
    for compound, expected in test_set:
        row = [compound, expected]
        for stat in stats:
            row.append(stat["splits"][i])
        i += 1
        rows.append(row)

    for row in rows:
        print(str.join(",", row))


if __name__ == '__main__':
    for test_set_name, test_set, stats in compare_methods():
        print(f"=== TEST SET {test_set_name} ===")
        splits_table(test_set, stats)
        for stat in stats:
            skipped = stat["skipped"]
            splits = stat["splits"]
            precision = stat["precision"]
            recall = stat["recall"]
            accuracy = stat["accuracy"]
            print("Method:    " + stat["displayName"])
            print(f"Word#:     {len(splits)}")
            if skipped > 0:
                print(f"Skipped:   {skipped} !!!")
            print("F1:        " + str(2 * (precision*recall) / (precision+recall)))
            print(f"Precision: {precision}")
            print(f"Recall:    {recall}")
            print(f"Accuracy:  {accuracy}\n\n")
