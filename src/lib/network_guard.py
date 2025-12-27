import urllib.parse


LOCAL_HOSTS = {"localhost", "127.0.0.1"}


def enforce_local_only(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    if host and host not in LOCAL_HOSTS:
        raise ValueError(f"External network calls are forbidden: {host}")
