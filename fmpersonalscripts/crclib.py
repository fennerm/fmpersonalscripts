"""Library code for operations involving CRC IBEST <-> Local communication"""

from plumbum import local

def check_valid_location(local_path):
    """Check that a given path is inside the shared 'fmacrae' directory

    Parameters
    ----------
    local_path: plumbum.local.path
        A directory

    Raises
    ------
    ValueError
        If `local_path` is not in shared fmacrae directory
    """
    if 'fmacrae' not in local_path.parts:
        raise ValueError('Push should only be called inside the shared dir')

def map_local_to_remote(local_path):
    """Given a local path, return the equivalent path on IBEST

    Parameters
    ----------
    local_path: plumbum.local.path
        A directory

    Returns
    -------
    plumbum.local.path
        Matched directory on IBEST
    """
    remote = local_path.relative_to(local.path('/') / 'home' / 'data')
    remote_address = 'schaack@ford.ibest.uidaho.edu:' + str(remote)
    return remote_address
