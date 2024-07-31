from yt.config import ytcfg


def is_sequence(obj):
    """
    Grabbed from Python Cookbook / matplotlib.cbook.  Returns true/false for

    Parameters
    ----------
    obj : iterable
    """
    try:
        len(obj)
        return True
    except TypeError:
        return False


def is_root():
    """
    This function returns True if it is on the root processor of the
    topcomm and False otherwise.
    """
    if not ytcfg.get("yt", "internals", "parallel"):
        return True
    return ytcfg.get("yt", "internals", "topcomm_parallel_rank") == 0
