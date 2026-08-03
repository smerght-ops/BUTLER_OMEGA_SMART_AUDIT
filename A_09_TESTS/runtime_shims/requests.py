class Session:
    pass


def get(*args, **kwargs):
    raise RuntimeError("NETWORK_DISABLED_DURING_OFFICIAL_WORD_ACCEPTANCE")


def post(*args, **kwargs):
    raise RuntimeError("NETWORK_DISABLED_DURING_OFFICIAL_WORD_ACCEPTANCE")
