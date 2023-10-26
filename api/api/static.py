# flake8: noqa WPS432, S105
import datetime
from zoneinfo import ZoneInfo


class Static:
    """Set the Static variables here."""

    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
    GITHUB_EMAIL_LIST_URL = "https://api.github.com/user/emails"
    GITHUB_USER_INFO_URL = "https://api.github.com/user"
    GITHUB_DEFAULT_HEADER = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    TOKEN_CODE_EXPIRE_TIME = datetime.timedelta(minutes=15)
    ACCESS_TOKEN_EXPIRE_TIME = datetime.timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE_TIME = datetime.timedelta(days=90)
    TIME_ZONE = ZoneInfo("Asia/Tokyo")


static = Static()
