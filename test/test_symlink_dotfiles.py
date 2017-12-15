from warnings import filterwarnings

from pytest import fixture

from fmpersonalscripts.symlink_dotfiles import symlink_all_dotfiles

filterwarnings("ignore")

@fixture(name="mock_home")
def gen_mock_home(sandbox):
    mock_home = {}
    mock_home['home'] = sandbox / 'home'
    mock_home['home'].mkdir()
    mock_home['xdg_home'] = mock_home['home'] / '.config'
    mock_home['xdg_home'].mkdir()
    mock_home['config_file'] = mock_home['xdg_home'] / 'a_file'
    with mock_home['config_file'].open('w') as f:
        f.write('foo')
    mock_home['config_file'].touch()
    mock_home['broken_link'] = mock_home['home'] / 'broken_link'
    doesnt_exist = mock_home['home'] / 'doesnt_exist'
    doesnt_exist.touch()
    doesnt_exist.symlink(mock_home['broken_link'])
    doesnt_exist.delete()

    yield mock_home
    mock_home['home'].delete()


@fixture(name="mock_dots")
def gen_mock_dots(sandbox):
    mock_dots = {}
    mock_dots['dots'] = sandbox / 'dots'
    mock_dots['dots'].mkdir()
    mock_dots['xdg_home'] = mock_dots['dots'] / '.config'
    mock_dots['xdg_home'].mkdir()
    mock_dots['conflict'] = mock_dots['xdg_home'] / 'a_file'
    mock_dots['conflict'].touch()
    mock_dots['other_dir'] = mock_dots['dots'] / 'dir2'
    mock_dots['other_dir'].mkdir()
    mock_dots['contained_file'] = mock_dots['other_dir'] / 'con_file'
    mock_dots['contained_file'].touch()
    mock_dots['no_conflict'] = mock_dots['dots'] / '.another_file'
    mock_dots['no_conflict'].touch()
    mock_dots['not_broken_here'] = mock_dots['dots'] / 'broken_link'
    mock_dots['not_broken_here'].touch()
    mock_dots['two_dots'] = mock_dots['dots'] / '.foo.bar'
    mock_dots['two_dots'].touch()
    yield mock_dots
    mock_dots['dots'].delete()

@fixture(name="resultant_dirs")
def gen_resultant_dirs(mock_home, mock_dots):
    symlink_all_dotfiles(
        dots=mock_dots['dots'], home=mock_home['home'])

def test_conflicts_not_overwritten(resultant_dirs, mock_home, mock_dots):
    assert mock_home['config_file'].read() == 'foo'

def test_no_conflicts_linked(resultant_dirs, mock_home, mock_dots):
    assert (mock_home['home'] / '.another_file').exists()

def test_config_dir_not_linked(resultant_dirs, mock_home, mock_dots):
    assert not mock_home['xdg_home'].is_symlink()

def test_contained_file_linked(resultant_dirs, mock_home, mock_dots):
    assert (mock_home['home'] / 'dir2' / 'con_file').exists()

def test_two_dots(resultant_dirs, mock_home, mock_dots):
    assert (mock_home['home'] / '.foo.bar').exists()
