"""Version gates for saved adapter data, independent of PIXL wire versions."""

from .codec import PixlError


def require_version(value, format_name, *, optional=False, exact_int=False):
    """Return the unchanged object after checking its declared supported version.

    JSON Schema integer semantics include 1.0. Adapters that historically used
    exact Python integers can retain that narrower rule with ``exact_int``.
    ``optional`` supports legacy objects without a version, never explicit null.
    """
    if not isinstance(value, dict):
        raise PixlError("adapter_version", f"{format_name} must be a JSON object")
    if "version" not in value and optional:
        return value
    version = value.get("version")
    supported = (
        type(version) is int if exact_int else type(version) in (int, float)
    ) and version == 1
    if not supported:
        declared = repr(version) if type(version) in (str, int, float, bool, type(None)) else type(version).__name__
        if "version" not in value:
            declared = "missing"
        raise PixlError(
            "adapter_version",
            f"{format_name}: unsupported version {declared}; this kit supports version 1. "
            "Preserve the saved file and use a compatible kit or an explicit tested migration; do not relabel its version.",
        )
    return value


def is_binding(value, namespace):
    """Recognize our namespace, including unsupported or malformed revisions."""
    return isinstance(value, str) and (value == namespace or value.startswith(namespace + "/"))


def require_binding(value, namespace):
    """Reject interpreting a saved binding with unknown adapter semantics."""
    if value != namespace + "/1":
        raise PixlError(
            "adapter_version",
            f"{namespace}: unsupported binding {value!r}; this kit supports {namespace}/1. "
            "Preserve the saved state and use a compatible kit or an explicit tested migration; do not relabel its binding.",
        )
    return value
