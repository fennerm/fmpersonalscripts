from fmpersonalscripts.save_i3_layout import reformat_json
import json
from plumbum import local
from pytest import fixture

@fixture(name="layout")
def gen_layout(testdir):
    return testdir / "resources" / "example_layout.json"

def test_save_i3_layout(layout, randstr, sandbox):
    name = randstr()
    outfile = local.path(sandbox / (name + '.json'))
    with open(layout, 'r') as f:
        reformat_json(f.read(), outfile)
    json.load(outfile)
