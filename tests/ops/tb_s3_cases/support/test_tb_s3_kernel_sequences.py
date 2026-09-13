"""Short event permutations checked against a hand-derived obligation oracle.

Neither the oracle nor expected allocations use the kernel's rule helpers.
Independent symbol deliveries commute; older facts cannot undo a newer completion.
"""


import copy


from itertools import permutations


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.harness import MIN, Sequence, entry, fill_lot, make_world
