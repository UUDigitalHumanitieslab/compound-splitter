import csv
import os
from math import nan
from random import sample
from time import perf_counter
from typing import Tuple, List
from .splitter import get_method, list_methods

COMPOUND_SPLIT_CHAR = "_"
'''Character used to mark where string is split by a compound splitter'''

COMPOUND_INFIX_TOLERANCE = 4
'''
Maximum size of infixes that may be dropped when splitting.

For a word like `watersnood`, a splitter may
return `waters_nood` or `water_nood` (dropping the `-s-` infix).
Both of these should be treated as correct results.
'''

MAX_TEST_SET_SIZE = 100
'''
Maximum number of words to evaluate per test set

If the test set is larger, a random sample will be evaluated.
'''

class MisalignedError(Exception):
    pass


def compare_methods():
    '''
    Report an evaluation of all compound split methods per test set.

    Returns a generator which returns for each test set:
    - the name of the set
    - the data
    - evaluation statistics
    '''
    
    for test_set_name, test_set in read_test_sets():
        stats = list(evaluate_methods(test_set))
        stats.sort(key=lambda item: item["accuracy"], reverse=True)

        for stat in stats:
            stat["test_set"] = test_set_name

        yield test_set_name, test_set, stats


def read_test_sets():
    '''
    Import data from all test sets

    Each test set should be a CSV file in the test_sets directory.
    If the number of items in the set is greater than 100,
    a random sample will be used.
    
    Returns a generator which yields the name and data for each file.
    '''
    
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

        if len(test_set) > MAX_TEST_SET_SIZE:
            print(
                f"{test_set_name} limited from {len(test_set)} items to {MAX_TEST_SET_SIZE} (random sample).")
            test_set = sample(test_set, MAX_TEST_SET_SIZE)
        yield test_set_name, test_set


def only_main(compound: str):
    """
    Convert a splitted compound into a compound only split into
    a main component and its satelite e.g. fietsen_stalling_pas ->
    fietsenstalling_pas

    Args:
        compound (str): an underscore splitted compound
    """
    splitted = compound.split("_")
    if len(splitted) == 1:
        return splitted[0]
    return "".join(splitted[:-1]) + "_" + splitted[-1]


def evaluate_methods(test_set: List[Tuple[str, str]]):
    '''
    Evaluate all compound split methods on a test set

    Returns a dictionary with evaluation results
    '''
    
    methods = list_methods()
    main_test_set = list(
        (compound, only_main(expected)) for (compound, expected) in test_set)
    for method in methods:
        method_name = method["name"]
        result = call_method(method_name, test_set)
        splits = result["splits"]
        yield {
            **method,
            **result,
            **evaluate_method(method_name, test_set, splits)
        }
        main_splits = list(only_main(split) for split in splits)
        yield {
            **method,
            **{"displayName": method["displayName"] + " (main)"},
            **result,
            **evaluate_method(method_name, main_test_set, main_splits)
        }


def split(method, compound: str) -> str:
    '''
    Split a compound using a method

    Result is a string where splits are marked with _,
    e.g. `"kwaliteitscontrole"` -> `"kwaliteits_controle"`.

    If the method returns multiple results, the highest-scoring
    result is selected. If the method returns no results,
    returns the word without splits.
    '''
    
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


def evaluate_method(method_name: str,
                    test_set: List[Tuple[str, str]],
                    splits: List[str]):
    '''
    Run evaluation on the results of a method

    Returns a dict with evaluation statistics, namely:
    - precision (ratio of splits that was correct)
    - recall (ratio of places where words should have been split, where the method did so)
    - accuracy (ratio of words that were split correctly)
    - skipped (number of words with invalid results)
    '''
    
    skipped = 0
    # number of correctly passed through words
    # i.e. words which weren't split and should not have been split
    passed_correctly = 0

    splitted_correctly = 0  # number of correctly split words
    splitted_incorrectly = 0  # number of words which were splitted
    compounds = 0  # number of compounds in the test set

    for (compound, expected), actual in zip(test_set, splits):
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

    return {
        "precision": splitted_correctly / splitted if splitted else nan,
        "recall": splitted_correctly / compounds if compounds else nan,
        "accuracy": (passed_correctly + splitted_correctly) / len(test_set),
        "skipped": skipped,
    }


def call_method(method_name: str, test_set: List[Tuple[str, str]]):
    '''
    Call a compound split method and run it for everything
    in a test set.
    '''
    
    method = get_method(method_name)
    print("METHOD:", method_name)
    start = perf_counter()
    method.start()
    splits = []
    started = perf_counter()
    try:
        for compound, expected in test_set:
            actual = split(method, compound)

            splits.append(actual)
    finally:
        done = perf_counter()
        method.stop()

    return {
        "splits": splits,
        "startup_time": started - start,
        "parse_time": done - started
    }


def score(actual: str, expected: str) -> Tuple[int, int, int]:  # noqa: C901
    '''
    Score the split of a single word

    Input:
    - `actual`: the result of the compound splitter
    - `expected`: the correct split

    Both of these should be strings with _ marking where
    the word is split.

    Returns a tuple of:
    - the number of false negatives (places where the word
    should have been split, but wasn't)
    - the number of false positives (places where the word
    should not have been split, but was)
    - the number of true positives (correct splits)
    '''
    
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
            parse_time = stat["parse_time"]
            precision = stat["precision"]
            recall = stat["recall"]
            accuracy = stat["accuracy"]
            print("Method:    " + stat["displayName"])
            print(f"Word#:     {len(splits)}")
            if skipped > 0:
                print(f"Skipped:   {skipped} !!!")
            print("F1:        " + str(2 * (precision*recall) / (precision+recall)))
            print(f"Duration:  {parse_time} seconds")
            print(f"Precision: {precision}")
            print(f"Recall:    {recall}")
            print(f"Accuracy:  {accuracy}\n\n")
