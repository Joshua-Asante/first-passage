"""validation-controls: see research_utils.camp_import + CATALOG camp-layout note.

Hyphenated camp slugs are not valid packages. CI uses ``--import-mode=importlib``.
Camps that ``import`` a sibling ``*.py`` by basename should load it via
``research_utils.camp_import.load_camp_sibling`` so shared names like
``construct_lib`` do not cross-wire across camps.
"""
