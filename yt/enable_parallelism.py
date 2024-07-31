from yt.utilities.logger import ytLogger as mylog


def turn_on_parallelism():
    parallel_capable = False
    try:
        # we import this to check if mpi4py is installed
        from mpi4py import MPI  # NOQA
    except ImportError as e:
        mylog.error(
            "Warning: Attempting to turn on parallelism, "
            "but mpi4py import failed. Try pip install mpi4py."
        )
        raise e
        # Now we have to turn on the parallelism from the perspective of the
    # parallel_analysis_interface
    from yt.utilities.parallel_tools.parallel_analysis_interface import (
        enable_parallelism,
    )

    parallel_capable = enable_parallelism()
    return parallel_capable
