from __future__ import annotations

import os
import platform
import sys

def capture_environment() -> dict[str, str]:
    return {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "machine": platform.machine(),
        "pid": str(os.getpid()),
    }
