"""Shared result envelopes; runtime validation and saved formats remain authoritative."""

from os import PathLike
from typing import TypeAlias, TypedDict

PathInput: TypeAlias = str | PathLike[str]


class PublicationResult(TypedDict):
    revision: int
    hash: str
    state: str


class FileIdentity(TypedDict):
    path: str
    sha256: str


class HandoffReceipt(FileIdentity):
    asset_id: str
    requirements_hash: str
    state_hash: str
    next: str
    scope: str


class SectionLocator(FileIdentity):
    start: int
    end: int
    bytes: int
    json_pointer: str
