from .binary import BinaryInspector
from .configuration import ConfigurationInspector
from .git import GitInspector
from .policy import PolicyInspector
from .privacy import PrivacyInspector
from .secrets import SecretsInspector
from .whitelist import WhitelistInspector

DEFAULT_INSPECTORS = (
    ConfigurationInspector,
    SecretsInspector,
    PrivacyInspector,
    BinaryInspector,
    GitInspector,
    WhitelistInspector,
    PolicyInspector,
)

__all__ = ["DEFAULT_INSPECTORS"]
