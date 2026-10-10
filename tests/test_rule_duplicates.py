"""Gate: no domain may be claimed by two hand-written lists that route it differently.

Runs the duplicate audit; the iCloud consumer files are required to see the phone/gateway policies,
so the check is skipped where they are not present (they are this workstation's source of truth).
"""
import importlib.util
import pathlib
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
DOCS = pathlib.Path.home() / 'Library/Mobile Documents/iCloud~com~nssurge~inc/Documents'


def audit():
    spec = importlib.util.spec_from_file_location('audit_duplicates', REPO / 'scripts' / 'audit-duplicates.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@unittest.skipUnless(DOCS.exists(), 'consumer rule files not available')
class DuplicateOwnershipTest(unittest.TestCase):
    def test_no_conflicting_ownership(self):
        mod = audit()
        argv = sys.argv
        sys.argv = ['audit-duplicates.py']          # main() parses argv; keep unittest's out of it
        try:
            code = mod.main()
        finally:
            sys.argv = argv
        self.assertEqual(0, code, 'rule ownership conflict: see scripts/audit-duplicates.py')

    def test_declared_layers_win(self):
        mod = audit()
        rules = mod.lists_rules()
        for specific, generic in mod.LAYERS:
            self.assertIn(specific, rules, specific)
            self.assertIn(generic, rules, generic)
            overlap = set(rules[specific][1]) & set(rules[generic][1])
            self.assertTrue(overlap, 'declared layer %s/%s no longer overlaps' % (specific, generic))


if __name__ == '__main__':
    unittest.main()
