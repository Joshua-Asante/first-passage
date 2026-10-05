#!/usr/bin/env python3
"""Operator entry point for the T00 step-3 screen driver (build card amendment PF-2).

``.\\fp.ps1 python scripts/t00_screen.py <subcommand> ...`` puts the ``core`` and ``ops`` layer
roots on ``sys.path`` (``layer_bootstrap.add_layer_roots``) and runs
``c1_rail.qualification.t00_screen`` as ``__main__``. No other logic.
"""
import runpy

from layer_bootstrap import add_layer_roots

add_layer_roots('core', 'ops')

if __name__ == '__main__':
    runpy.run_module('c1_rail.qualification.t00_screen', run_name='__main__', alter_sys=True)
