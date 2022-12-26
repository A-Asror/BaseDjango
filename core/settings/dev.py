from core.settings.base import INSTALLED_APPS, MIDDLEWARE, env

"""
START SITE APPS
"""

APPS = [
    "debug_toolbar",
    "querycount",
]

INSTALLED_APPS += APPS

"""
END SITE APPS

START DJANGO DEBUG TOOLBAR
"""

INTERNAL_IPS = [
    "127.0.0.1",
]  # for debug toolbar

"""
END DJANGO DEBUG TOOLBAR

START QUERY COUNTER
"""

QUERYCOUNT = {
    "THRESHOLDS": {"MEDIUM": 50, "HIGH": 200, "MIN_TIME_TO_LOG": 0, "MIN_QUERY_COUNT_TO_LOG": 0},
    "IGNORE_REQUEST_PATTERNS": [],
    "IGNORE_SQL_PATTERNS": [],
    "DISPLAY_DUPLICATES": None,
    "RESPONSE_HEADER": "X-DjangoQueryCount-Count",
}

"""
END QUERY COUNTER

START MIDDLEWARE
"""

MIDDLEWARE += [
    "querycount.middleware.QueryCountMiddleware",  # remove production
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # remove production
]

"""
END MIDDLEWARE
"""
