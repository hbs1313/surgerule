"""Regression tests for source preservation, portability and generated bindings."""
import json
from pathlib import Path
import runpy
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
B = runpy.run_path(str(ROOT / 'scripts/build-rules.py'))


class RuleTests(unittest.TestCase):
    def fixture(self, rules='DOMAIN-SUFFIX,example.com\n', mode='full', category='ai'):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        (root / 'test.list').write_text(rules)
        order = [['test', 'AI']] if mode == 'full' else []
        manifest = {'schema_version': 1, 'lists': {'test': {'category': category, 'mihomo': mode, 'description': 'fixture'}}, 'rules': order}
        if not order:
            (root / 'shared.list').write_text('DOMAIN,shared.example\n')
            manifest['lists']['shared'] = {'category': 'ai', 'mihomo': 'full', 'description': 'shared fixture'}
            manifest['rules'] = [['shared', 'AI']]
        (root / 'routing.json').write_text(json.dumps(manifest))
        return root

    def test_indented_comments_and_crlf(self):
        self.assertEqual(B['read_rules']('  # comment\r\n ; comment\r\n // comment\r\n \r\nDOMAIN,a.example\r\n', 'fixture'), ['DOMAIN,a.example'])

    def test_reject_embedded_policy(self):
        with self.assertRaisesRegex(ValueError, 'embedded policy'):
            B['read_rules']('DOMAIN,example.com,DIRECT', 'fixture')

    def test_reject_unknown_type(self):
        with self.assertRaisesRegex(ValueError, 'unsupported rule type'):
            B['read_rules']('NEW-TYPE,example.com', 'fixture')

    def test_reject_quoted_fields_and_hidden_extra_comma(self):
        for rule in ['DOMAIN,"example.com"', 'IP-ASN,"13335"', 'DOMAIN-KEYWORD,"example.com,DIRECT"']:
            with self.subTest(rule=rule), self.assertRaisesRegex(ValueError, 'quoted fields'):
                B['read_rules'](rule, 'fixture')

    def test_cidr_requires_explicit_prefix(self):
        for rule in ['IP-CIDR,192.0.2.1', 'IP-CIDR6,2001:db8::1']:
            with self.subTest(rule=rule), self.assertRaisesRegex(ValueError, 'CIDR prefix'):
                B['read_rules'](rule, 'fixture')

    def test_reject_bad_network_and_family(self):
        for rule in ['IP-CIDR,192.0.2.1/24', 'IP-CIDR,2001:db8::/32', 'IP-CIDR6,192.0.2.0/24']:
            with self.subTest(rule=rule), self.assertRaises(ValueError):
                B['read_rules'](rule, 'fixture')

    def test_reject_bad_domain_or_url(self):
        for value in ['https://example.com/path', 'a..example', '*.example.com', 'bad host.example']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                B['read_rules']('DOMAIN-SUFFIX,' + value, 'fixture')

    def test_reject_duplicate_active_rule(self):
        with self.assertRaisesRegex(ValueError, 'duplicate rule'):
            B['read_rules']('DOMAIN,a.example\nDOMAIN,a.example\n', 'fixture')

    def test_full_lists_cannot_silently_drop_user_agent(self):
        root = self.fixture('DOMAIN,a.example\nUSER-AGENT,SomeApp*\n')
        with self.assertRaisesRegex(ValueError, 'full parity'):
            B['compile_repository'](root)

    def test_partial_records_omission_without_changing_source(self):
        source = 'DOMAIN,a.example\nUSER-AGENT,SomeApp*\n'
        root = self.fixture(source, 'partial', 'client-direct')
        output = B['compile_repository'](root)
        self.assertNotIn('USER-AGENT', output['test.yaml'])
        catalog = json.loads(output['docs/catalog.json'])['lists'][0]
        self.assertEqual((catalog['surge_rules'], catalog['mihomo_rules'], catalog['excluded_count']), (2, 1, 1))
        self.assertEqual(catalog['excluded_types'], ['USER-AGENT'])
        self.assertEqual((root / 'test.list').read_text(), source)

    def test_source_device_rules_stay_client_only(self):
        root = self.fixture('SRC-IP,192.0.2.10/32,no-resolve\n', 'none', 'client-source')
        self.assertNotIn('test.yaml', B['compile_repository'](root))

    def test_src_ip_cannot_enter_partial_hub_list(self):
        root = self.fixture('DOMAIN,a.example\nSRC-IP,192.0.2.10\n', 'partial', 'client-direct')
        with self.assertRaisesRegex(ValueError, 'partial mode'):
            B['compile_repository'](root)

    def test_uncatalogued_source_fails(self):
        root = self.fixture()
        (root / 'new.list').write_text('DOMAIN,new.example\n')
        with self.assertRaisesRegex(ValueError, 'every .list'):
            B['compile_repository'](root)

    def test_stale_check_is_read_only(self):
        root = self.fixture()
        with self.assertRaisesRegex(ValueError, 'missing or stale'):
            B['synchronize'](root, True)
        self.assertFalse((root / 'test.yaml').exists())
        self.assertFalse((root / 'docs').exists())

    def test_idempotent_generation_and_stale_detection(self):
        root = self.fixture()
        self.assertGreater(B['synchronize'](root, False)[1], 0)
        self.assertEqual(B['synchronize'](root, False)[1], 0)
        self.assertEqual(B['synchronize'](root, True)[1], 0)
        (root / 'test.yaml').write_text('payload: []\n')
        with self.assertRaisesRegex(ValueError, 'stale'):
            B['synchronize'](root, True)

    def test_unknown_yaml_fails(self):
        root = self.fixture()
        (root / 'orphan.yaml').write_text('payload: []\n')
        with self.assertRaisesRegex(ValueError, 'unexpected root YAML'):
            B['synchronize'](root, False)

    def test_validate_all_before_any_output_write(self):
        root = self.fixture('UNKNOWN,example.com\n')
        with self.assertRaises(ValueError):
            B['synchronize'](root, False)
        self.assertEqual(set(p.name for p in root.iterdir()), {'test.list', 'routing.json'})

    def test_repository_has_complete_inventory(self):
        output = B['compile_repository'](ROOT)
        rows = json.loads(output['docs/catalog.json'])['lists']
        sources = list(ROOT.glob('*.list'))
        all_rules = [rule for path in sources for rule in B['read_rules'](path.read_text(), path.name)]
        self.assertEqual({r['name'] for r in rows}, {p.stem for p in sources})
        self.assertEqual(sum(r['surge_rules'] for r in rows), len(all_rules))
        portable_count = sum(rule.split(',', 1)[0] in B['PORTABLE'] for rule in all_rules)
        self.assertEqual(sum(r['mihomo_rules'] for r in rows), portable_count)
        self.assertEqual(sum(r['excluded_count'] for r in rows), len(all_rules) - portable_count)

    def test_existing_manifest_order_and_policy_preserved(self):
        order = B['load_manifest'](ROOT)['rules']
        self.assertEqual(order, [['ai-apple', 'AI-Apple'], ['ai-claude', 'AI-Claude'], ['ai-chat', 'AI-OpenAI'], ['ai-google', 'AI-Google'], ['ai', 'AI'], ['us', 'AI'], ['ben', 'Work-US'], ['video-proxy', 'Proxy'], ['twitter', 'Work-US'], ['mmc', 'Work-US']])

    def test_generated_yaml_exactly_preserves_portable_rule_order(self):
        output = B['compile_repository'](ROOT)
        for name, item in B['load_manifest'](ROOT)['lists'].items():
            if item['mihomo'] == 'none':
                continue
            expected = [r for r in B['read_rules']((ROOT / (name + '.list')).read_text(), name) if r.split(',', 1)[0] in B['PORTABLE']]
            actual = [json.loads(line[4:]) for line in output[name + '.yaml'].splitlines()[1:]]
            self.assertEqual(actual, expected, name)

    def test_examples_bind_same_sources_in_same_order(self):
        order = B['load_manifest'](ROOT)['rules']
        examples = B['render_examples'](order)
        for filename in ['examples/surge-shared.dconf', 'examples/surge-smart-ingress.dconf']:
            lines = [r for r in examples[filename].splitlines() if r.startswith('RULE-SET,')]
            self.assertEqual([r.split(',')[1].rsplit('/', 1)[1].removesuffix('.list') for r in lines], [name for name, _ in order])
        self.assertNotIn('FINAL,', examples['examples/surge-shared.dconf'])
        self.assertNotIn('MATCH,', examples['examples/mihomo-shared.yaml'])

    def test_priority_regressions(self):
        def first_policy(host):
            for name, policy in B['load_manifest'](ROOT)['rules']:
                for rule in B['read_rules']((ROOT / (name + '.list')).read_text(), name):
                    kind, value = rule.split(',')[:2]
                    if ((kind == 'DOMAIN' and host == value) or
                        (kind == 'DOMAIN-SUFFIX' and (host == value or host.endswith('.' + value))) or
                        (kind == 'DOMAIN-KEYWORD' and value in host)):
                        return policy
        for host, policy in {
            'browser-intake-us5-datadoghq.com': 'AI-Claude',
            'http-intake.logs.us5.datadoghq.com': 'AI-Claude',
            'claude.ai': 'AI-Claude', 'clau.de': 'AI-Claude', 'chatgpt.com': 'AI-OpenAI', 'gemini.google.com': 'AI-Google', 'grok.com': 'AI', 'video.twimg.com': 'Proxy', 'pbs.twimg.com': 'Work-US', 'challenges.cloudflare.com': 'AI-Claude', 'cloudflare.com': 'Work-US', 'apple-relay.cloudflare.com': 'AI-Apple'
        }.items():
            with self.subTest(host=host):
                self.assertEqual(first_policy(host), policy)


if __name__ == '__main__':
    unittest.main()
