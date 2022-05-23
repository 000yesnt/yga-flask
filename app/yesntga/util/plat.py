import os.path
from sys import platform
def get_platform() -> str:
    """Platform identification. Tells whether we're on Docker, Linux or Windows."""
    # TODO: Add Windows check
    if platform.startswith('linux'):
        with open('/proc/1/cgroup') as proc:
            guh = proc.read()
            if 'docker' in guh:
                runtype = 'linux-docker'
            else:
                runtype = 'linux-standard'
    else:
        return platform
    return runtype
