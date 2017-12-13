from plumbum import local
from plumbum.cmd import sysmaint

def test_sysmaint():
    sysmaint()
    assert (local.env.home / 'data/logs/arch/arch.log').exists()
