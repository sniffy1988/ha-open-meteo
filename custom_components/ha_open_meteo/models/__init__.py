"""Variable catalogs for Open-Meteo APIs."""

from ..const import DEFAULT_GROUPS, GROUP_LABELS, group_options
from .variables import MODULE_GROUPS, VariableDef, expand_variables

__all__ = [
    "DEFAULT_GROUPS",
    "GROUP_LABELS",
    "MODULE_GROUPS",
    "VariableDef",
    "expand_variables",
    "group_options",
]
