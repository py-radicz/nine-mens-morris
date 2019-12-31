from exceptions import PositionOccupied, PositionEmpty


class Board:
    def __init__(self):
        self._empty = 0
        self._players = {"black": 10, "white": 33}
        self._board = [[self._empty] * 3 for x in range(8)]

    def insert(self, who, pos):
        x, y = pos

        if self._board[x][y] != self._empty:
            raise PositionOccupied

        mill_count = len(self._get_mills(who))
        self._board[x][y] = self._players.get(who)
        mill_count_after = len(self._get_mills(who))

        return True if mill_count_after > mill_count else False

    def remove(self, pos):
        x, y = pos

        if self._board[x][y] == self._empty:
            raise PositionEmpty

        self._board[x][y] = 0
        return True

    def _get_mills(self, who=None):
        mills = {"black": [], "white": []}

        # square side mills
        for point in range(8)[::2]:
            edges = self._board[point : point + 3]
            if len(edges) != 3:
                edges += [self._board[0]]

            for square, edge_sum in enumerate([x + y + z for x, y, z in zip(*edges)]):
                last_point = point + 2 if point + 2 < len(self._board) - 1 else 0
                if edge_sum == self._players.get("black") * 3:
                    mills["black"].append(
                        [(point, square), (point + 1, square), (last_point, square)]
                    )

                if edge_sum == self._players.get("white") * 3:
                    mills["white"].append(
                        [(point, square), (point + 1, square), (last_point, square)]
                    )

        # multi square mills
        for point, edge in enumerate(self._board, start=1):
            if point % 2 == 0:
                if sum(edge) == self._players.get("black") * 3:
                    mills["black"].append([(point - 1, square) for square in range(3)])

                if sum(edge) == self._players.get("white") * 3:
                    mills["white"].append([(point - 1, square) for square in range(3)])

        return mills.get(who) if who else mills

    def is_part_of_mill(self, pos):
        mills = self._get_mills()
        for mill in mills.get("black") + mills.get("white"):
            if any(position == pos for position in mill):
                return True

        return False
