

"""
Python implementation of the Microsoft Solitaire deal number generator.
"""

import random

import unittest
import pytest


def randomGenerator(seed=1):
    """
    taken from 
    https://rosettacode.org/wiki/Deal_cards_for_FreeCell#Python
    """
    max_int32 = (1 << 31) - 1
    seed = seed & max_int32

    while True:
        seed = (seed * 214013 + 2531011) & max_int32
        yield seed >> 16


def shuffle(seed):
    nc = 52
    cards = list(range(nc - 1, -1, -1))
    rnd = randomGenerator(seed)
    for i, r in zip(range(nc), rnd):
        j = (nc - 1) - r % (nc - i)
        cards[i], cards[j] = cards[j], cards[i]
    return cards


def format_cards(cards):
    """
    put in lists of 8 cards per line
    """
    deck = []
    for i in range(0, len(cards), 8):
        deck.append(cards[i: i+8])
    return deck


def show_cards(cards):
    l = ["A23456789TJQK"[int(c/4)] + "CDHS"[c % 4] for c in cards]
    rows = []
    for i in range(0, len(cards), 8):
        row = " ".join(l[i: i+8])
        rows.append(row)
    return rows


if __name__ == '__main__':
    from sys import argv
    seed = int(argv[1]) if len(argv) == 2 else 11982
    print("Hand {}".format(seed))
    deck = shuffle(seed)
    show_cards(deck)

# Tests


class Test_MS_Random(unittest.TestCase):
    def test_randomGenerator(self):
        seed = 1
        randg = randomGenerator(seed)
        self.assertEqual(next(randg), 41)

    def test_deal_hard_freecell(self):
        cards = shuffle(94717719)
        rows = show_cards(cards)
        expected = [
            "7D AH AS TD 6C TC JH AC",
            "2S 4H 2C 3C TH 5H 9C 7H",
            "9H KH 3H AD 9D 8S JD 7C",
            "5C 4D 8C 6D QS 5D KS 7S",
            "9S 8D JC 6H 4S 3S QH 2D",
            "TS QD 8H QC 2H 6S JS KC",
            "3D KD 4C 5S",
        ]
        self.assertEqual(rows, expected)

    def test_first_deal(self):
        cards = shuffle(1)
        rows = show_cards(cards)
        expected = [
            "JD 2D 9H JC 5D 7H 7C 5H",
            "KD KC 9S 5S AD QC KH 3H",
            "2S KS 9D QD JS AS AH 3C",
            "4C 5C TS QH 4H AC 4D 7S",
            "3S TD 4S TH 8H 2C JH 7D",
            "6D 8S 8D QS 6C 3D 8C TC",
            "6S 9C 2H 6H",
        ]
        self.assertEqual(rows, expected)


"""
deal_freecell(1)
deal_freecell(617)
deal_freecell(94717719)
"""

if __name__ == "__main__":
    unittest.main()
