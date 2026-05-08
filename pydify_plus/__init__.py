from .async_client import AsyncClient
from .sync_client import Client

try:
    from ._version import __version__
except Exception:
    try:
        from importlib.metadata import version

        __version__ = version("pydify_plus")
    except Exception:
        __version__ = "0.0.0"
__all__ = ["AsyncClient", "Client", "__version__"]
