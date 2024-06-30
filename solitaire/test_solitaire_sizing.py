
from solitaire import KlondikeSolitaire as kSol
from solitaire import Solitaire as Sol

import unittest


class TestSolitaireReSizing(unittest.TestCase):
    def setUp(self):
        """Test Klondike Solitaire resizing"""
        self.solitaire = kSol()
        self.solitaire.ratio = "4:3"
        self.solitaire.update = lambda: None  # mock update

    def test_resize(self):
        self.solitaire.create_slots()
        self.solitaire.resize(800, 600)

        self.assertEqual(self.solitaire.width, 800)
        self.assertEqual(self.solitaire.height, 600)
        self.assertEqual(self.solitaire.max_card_width, 75)
        self.assertEqual(self.solitaire.max_card_height, 112.5)
        self.assertEqual(self.solitaire.separator, 25)


class TestSolitaireSizing(unittest.TestCase):
    def setUp(self):
        """Test Solitaire initial sizing"""
        self.solitaire = Sol()
        self.solitaire.ratio = "4:3"
        self.solitaire.update = lambda: None  # mock update

    def test_max_square_800(self):
        width, height = self.solitaire._max_square(800, 600)
        self.assertEqual(width, 800)
        self.assertEqual(height, 600)

    def test_max_square_superwide(self):
        width, height = self.solitaire._max_square(1800, 600)
        self.assertEqual(width, 800)
        self.assertEqual(height, 600)

    def test_max_square_superhi(self):
        width, height = self.solitaire._max_square(800, 2600)
        self.assertEqual(width, 800)
        self.assertEqual(height, 600)

class TestCardSizing(unittest.TestCase):
    def setUp(self):
        """Test Solitaire initial sizing"""
        self.solitaire = kSol()
        self.solitaire.update = lambda: None  # mock update

    def test_card_size(self):
        width, height = self.solitaire._card_size(800, 600)
        self.assertEqual(width, 75)
        self.assertEqual(height, 112.5)

    def test_card_reSize(self):
        width, height = self.solitaire._card_size(800, 600)
        self.assertEqual(width, 75)
        self.assertEqual(height, 112.5)

        self.solitaire.create_slots()
        self.solitaire.resize(1024 , 768)
        width, height = self.solitaire.get_card_size()
        self.assertEqual(width, 78)
        self.assertEqual(height, 117.0)


if __name__ == '__main__':
    unittest.main()
