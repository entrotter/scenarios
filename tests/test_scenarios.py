import json
from pathlib import Path
import unittest
from entrotter_engine.models import validate
try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator=None
ROOT=Path(__file__).resolve().parents[1]
class ScenarioTests(unittest.TestCase):
    def test_manifest_paths(self):
        manifest=json.loads((ROOT/'manifest.json').read_text())
        for key in ['fixtures','evm_local','historical_templates']:
            for name in manifest[key]:self.assertTrue((ROOT/name).is_file())
    def test_all_runtime_validate(self):
        for p in list((ROOT/'fixtures').glob('*.json'))+list((ROOT/'evm').glob('*.json')):
            with self.subTest(path=p.name):validate(json.loads(p.read_text()))
    def test_no_real_claims_in_synthetic(self):
        for p in (ROOT/'fixtures').glob('*.json'):
            data=json.loads(p.read_text());self.assertEqual(data['provenance']['kind'],'synthetic')
    @unittest.skipUnless(Draft202012Validator,'Development-only jsonschema dependency not installed')
    def test_json_schema(self):
        schema=json.loads((ROOT/'schemas/scenario.v0.1.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        validator=Draft202012Validator(schema)
        for p in list((ROOT/'fixtures').glob('*.json'))+list((ROOT/'evm').glob('*.json')):
            with self.subTest(path=p.name):validator.validate(json.loads(p.read_text()))

if __name__=='__main__':unittest.main()
