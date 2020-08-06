#!/usr/bin/env python3
import unittest
from compound_splitter.evaluate import score
from typing import List


class TestEvaluate(unittest.TestCase):
    def test_score(self):
        # word length
        # every position could be either
        parts = ["abc", "def", "gh", "ijklm", "no", "p"]

        for pairs in generate_test_boolean_pairs(5):
            # generate an "actual" and "expected" word to compare
            actual_splits, expected_splits = zip(*pairs)
            actual = generate_test_word(parts, actual_splits)
            expected = generate_test_word(parts, expected_splits)

            true_positives = 0
            false_negatives = 0
            false_positives = 0

            for actual_split, expected_split in pairs:
                if actual_split == expected_split:
                    if actual_split:
                        true_positives += 1
                    # both negative: nothing happens, not counted
                elif actual_split:
                    false_positives += 1
                elif expected_split:
                    false_negatives += 1

            expected_score = (false_negatives, false_positives, true_positives)
            actual_score = score(actual, expected)

            try:
                assert expected_score == actual_score
            except Exception as err:
                print(
                    f'Miscalculated distance between "{actual}" and "{expected}"!')
                print(f'Expected: {expected_score} Actual: {actual_score}')
                raise err


def generate_test_boolean_pairs(length: int):
    pairs = [(True, True), (True, False), (False, True), (False, False)]

    if length == 1:
        for pair in pairs:
            yield [pair]
    else:
        for next_pairs in generate_test_boolean_pairs(length-1):
            for pair in pairs:
                yield [pair] + next_pairs


def generate_test_word(parts: List[str], splits: List[bool]):
    word = ''
    for part, split in zip(parts, splits):
        word += part
        if split:
            word += '_'
    return word + parts[-1]


def generate_test_words(parts: List[str]):
    if len(parts) == 1:
        yield (0, parts[0])
    else:
        for (splits, word) in generate_test_words(parts[:-1]):
            yield (splits+1, word + '_' + parts[-1])
            yield (splits, word + parts[-1])
    # if length == 0:
    #     yield ''
    #     return
    # if can_split and length > 1:
    #     for word in generate_test_words(length-1, False, splits+1):
    #         yield 'a_' + word
    # for word in generate_test_words(length-1, True, splits):
    #     yield 'a' + word
    # start:
    # can't split

    # then to split or not to split:
    # if split, can't split afterwards
    # if did not split can or cannot split
