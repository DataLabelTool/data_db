import os
from pathlib import Path


def project_root() -> Path:
    """return project dir path"""
    return Path(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..')
        )
    )


def base_url() -> str:
    """

    :return: Path object with base url
    """
    base = os.getenv('API_BASE_URL', "")
    return base

