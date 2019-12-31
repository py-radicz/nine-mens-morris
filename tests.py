from unittest import TestCase, main

from exceptions import PositionOccupied, PositionEmpty
from engine import Board


class TestBoard(TestCase):
    def setUp(self):
        self.chips = [
            ("black", 1, 0),
            ("black", 1, 1),
            ("black", 1, 2),
            ("white", 0, 2),
            ("white", 6, 2),
            ("white", 7, 2),
        ]
        self.board = Board()

    def test_board_insert(self):
        self.assertFalse(self.board.insert("black", (0, 0)))
        self.assertFalse(self.board.insert("black", (1, 0)))
        self.assertTrue(self.board.insert("black", (2, 0)))
        self.assertEqual(self.board._board[0][0], self.board._players.get("black"))
        self.assertRaises(PositionOccupied, self.board.insert, "black", (0, 0))

    def test_remove(self):
        x, y = 0, 0
        self.assertFalse(self.board.insert("black", (x, y)))
        self.assertTrue(self.board.remove((x, y)))
        self.assertRaises(PositionEmpty, self.board.remove, (x, y))

    def test_board_get_mills(self):
        for chip in self.chips:
            color, *pos = chip
            self.board.insert(color, pos)

        mills = {
            "white": [[(6, 2), (7, 2), (0, 2)]],
            "black": [[(1, 0), (1, 1), (1, 2)]],
        }
        self.assertEqual(self.board._get_mills(), mills)
        self.assertEqual(self.board._get_mills("white"), mills.get("white"))
        self.assertEqual(self.board._get_mills("black"), mills.get("black"))

    def test_board_is_part_of_mill(self):
        for chip in self.chips:
            color, *pos = chip
            self.board.insert(color, pos)

        self.assertTrue(self.board.is_part_of_mill((1, 0)))
        self.assertTrue(self.board.is_part_of_mill((7, 2)))
        self.assertFalse(self.board.is_part_of_mill((3, 2)))


if __name__ == "__main__":
    main()
