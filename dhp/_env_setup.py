"""
All default options are for local development using the docker-compose file included
in the repository.
"""

import os
from urllib.parse import quote_plus

# ############################################# #
# Database Setup
# https://docs.sqlalchemy.org/en/14/core/engines.html#engine-configuration
# ############################################# #

# If DB_URL is defined it won't be built using any of the component parameters.
DB_URL = os.environ.get("DB_URL", False)

if not DB_URL:
    DB_HOST = os.environ.get("DB_HOST", "db")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASS = os.environ.get("DB_PASS", "")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "playground")
    DB_DIALECT = os.environ.get("DB_DIALECT", "postgresql")

    DB_DRIVER = os.environ.get("DB_DRIVER", "+psycopg2")

    if DB_DRIVER and not DB_DRIVER.startswith("+"):
        # If a Driver is specified the URL expects it to be prepended with `+` otherwise
        # a blank string.
        DB_DRIVER = "+" + DB_DRIVER

    # Build the URL.
    DB_URL = (
        f"{DB_DIALECT}{DB_DRIVER}://"
        f"{DB_USER}:{quote_plus(DB_PASS)}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


CELERY_BROKER = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_BACKEND = os.environ.get("CELERY_BACKEND", "redis://redis:6379/0")
