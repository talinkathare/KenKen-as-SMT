"""solution.py -- KenKen as SMT. Fill in each section marked YOUR CODE HERE.

A puzzle is an n x n grid holding the values 1 to n, with no value repeated in
any row or column, divided into regions called cages. Each cage states a
target and an operation, and the values in the cage must combine under that
operation to give the target. A cage of one cell states its value and no
operation.

Two conventions used throughout:

    cells[r][c]   the z3 Int for row r, column c, both counted from 0
    cage          (op, target, positions), as parse_puzzle returns it:
                  op is "+", "-", "*", "/" or None, and positions is a list
                  of (row, column) pairs

Run this file directly to see a puzzle printed, which is a quicker way to
check an answer than reading a string of digits.
"""

import re

import z3


# Given: the parser, and a printer for looking at a puzzle or an answer.

CELL = re.compile(r"^(r\d+)(?:\.(\d+)([+\-*/])?)?$")


def parse_puzzle(text):
    """(n, cages) for a puzzle in the course's .txt format.

    Lines beginning with # are ignored. Each remaining line is one row of the
    grid, cells separated by commas. A cell carries its cage's label; the
    label's first occurrence, reading row by row, also carries the target
    and the operation.
    """
    grid = [l.strip() for l in text.splitlines()
            if l.strip() and not l.startswith("#")]
    n = len(grid)
    order, cells, spec = [], {}, {}
    for r, line in enumerate(grid):
        entries = line.split(",")
        if len(entries) != n:
            raise ValueError("row %d has %d cells, not %d" % (r, len(entries), n))
        for c, raw in enumerate(entries):
            m = CELL.match(raw.strip())
            if not m:
                raise ValueError("cannot read cell %r" % raw)
            region, target, op = m.groups()
            if region not in cells:
                order.append(region)
                cells[region] = []
            cells[region].append((r, c))
            if target is not None:
                spec[region] = (op, int(target))
    if order != ["r%d" % i for i in range(1, len(order) + 1)]:
        raise ValueError("cage labels are not numbered consecutively")
    missing = [r for r in order if r not in spec]
    if missing:
        raise ValueError("cages with no target: %s" % ", ".join(missing))
    return n, [(spec[r][0], spec[r][1], cells[r]) for r in order]


def print_puzzle(text, solution=None):
    """Print a puzzle, with a solution laid over it if one is given.

    Lines are drawn only where two cells belong to different cages, so what
    you see is the cage map. Each cage's target sits in its first cell.
    """
    n, cages = parse_puzzle(text)
    owner, label = {}, {}
    for k, (op, target, positions) in enumerate(cages):
        for p in positions:
            owner[p] = k
        label[min(positions)] = "%d%s" % (target, op or "")

    def same(a, b):
        return owner.get(a) is not None and owner.get(a) == owner.get(b)

    def rule(r):
        """The boundary above row r; r == n is the bottom edge.

        Outside the grid counts as a different cage, so the outer border
        comes out continuous without a special case.
        """
        out = ""
        for c in range(n + 1):
            # A corner is drawn when any of the four edges meets it.
            up = not same((r - 1, c - 1), (r - 1, c))
            down = not same((r, c - 1), (r, c))
            left = not same((r - 1, c - 1), (r, c - 1))
            right = not same((r - 1, c), (r, c))
            out += "+" if (up or down or left or right) else " "
            if c < n:
                out += "-----" if right else "     "
        return out

    def row(r, content):
        out = ""
        for c in range(n):
            out += "|" if not same((r, c - 1), (r, c)) else " "
            out += content(r, c)
        return out + "|"

    print()
    for r in range(n):
        print(rule(r))
        print(row(r, lambda r, c: "%-5s" % label.get((r, c), "")))
        if solution is None:
            print(row(r, lambda r, c: "     "))
        else:
            print(row(r, lambda r, c: "  %s  " % solution[n * r + c]))
    print(rule(n))
    print()


# YOUR CODE HERE, from this point on.


def cell_constraints(n, cells):
    """Every cell holds 1 to n, and no value repeats in a row or a column.

    Returns a list of z3 constraints. z3.Distinct(xs) says that the values in
    xs are pairwise different, which is shorter than writing out the pairs.
    """
    constraints = []

    # Every cell holds a value from 1 to n (done for you).
    for r in range(n):
        for c in range(n):
            constraints.append(cells[r][c] >= 1)
            constraints.append(cells[r][c] <= n)

    # No value twice in a row.
    # YOUR CODE HERE

    # No value twice in a column.
    # YOUR CODE HERE

    return constraints


def cage_constraints(cage, cells):
    """The arithmetic of one cage, as a list of z3 constraints.

    z3.Sum(xs) adds a list of terms and z3.Product(xs) multiplies one. There
    is no division on integers to reach for here: say what the division means
    by multiplying instead.
    """
    op, target, positions = cage
    values = [cells[r][c] for r, c in positions]

    # A cage with no operation states the value of its one cell (done for
    # you).
    if op is None:
        return [values[0] == target]

    # Addition, over any number of cells.
    # YOUR CODE HERE

    # Multiplication, over any number of cells.
    # YOUR CODE HERE

    # Subtraction and division. Each of these cages has exactly two cells,
    # and the puzzle does not say which cell is which: it gives the
    # difference, or the larger divided by the smaller, and either cell may
    # be the larger. So each needs two cases.
    # YOUR CODE HERE

    raise NotImplementedError("no constraint written for a %s cage" % op)


def solve_kenken(puzzle):
    """The solution of a puzzle as n*n characters, read row by row, or None.

    Four steps: parse the puzzle, make an n by n array of z3 Ints, add
    cell_constraints and the cage_constraints of every cage to a z3.Solver,
    and read the values out of its model. A solver answers z3.sat, and
    model[v].as_long() is the integer it gave v.

    Return None when there is no solution, rather than raising.
    """
    # YOUR CODE HERE
    raise NotImplementedError


if __name__ == "__main__":
    # A 4x4 to look at, with one cage of each kind. It has exactly one
    # solution. Once solve_kenken works, the second call prints it in the
    # grid.
    EXAMPLE = ("#kenken csc432 Puzzle 0 4x4 example\n"
               "r1.3/,r2.4/,r2,r3.8+\n"
               "r1,r4.6*,r3,r3\n"
               "r5.7+,r4,r6.2-,r6\n"
               "r5,r5,r7.7+,r7\n")
    print_puzzle(EXAMPLE)
    answer = solve_kenken(EXAMPLE)
    print_puzzle(EXAMPLE, answer)
