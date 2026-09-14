"""Bounded parser and canonical encoder for the proprietary PIXL wire formats."""

import hashlib
import re
from dataclasses import dataclass, field
from typing import Never


class PixlError(ValueError):
    def __init__(self, code, detail=""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


@dataclass(frozen=True)
class Ref:
    id: str


@dataclass(frozen=True)
class Symbol:
    value: str


@dataclass
class Record:
    id: str
    kind: str
    fields: dict = field(default_factory=dict)


@dataclass
class Document:
    revision: int = 0
    records: dict[str, Record] = field(default_factory=dict)
    format: int = 1


IDENT = re.compile(rb"[A-Za-z][A-Za-z0-9_.-]{0,95}")
MAX_BYTES = 16 * 1024 * 1024
MAX_INT = 2**63 - 1
WS = b" \t\r\n"


class Parser:
    def __init__(self, data):
        if not isinstance(data, bytes) or len(data) > MAX_BYTES:
            raise PixlError("input_size", "expected bytes, at most 16 MiB")
        self.data, self.i = data, 0

    def error(self, detail) -> Never:
        raise PixlError("syntax", f"byte {self.i}: {detail}")

    def skip(self):
        while self.i < len(self.data) and self.data[self.i] in WS:
            self.i += 1

    def take(self, token):
        self.skip()
        if not self.data.startswith(token, self.i):
            self.error(f"expected {token!r}")
        self.i += len(token)

    def ident(self):
        self.skip()
        match = IDENT.match(self.data, self.i)
        if match is None:
            self.error("expected identifier")
        self.i = match.end()
        return match[0].decode("ascii")

    def unsigned(self):
        start = self.i
        while self.i < len(self.data) and 48 <= self.data[self.i] <= 57:
            self.i += 1
        if start == self.i or self.i - start > 19:
            self.error("invalid integer")
        value = int(self.data[start : self.i])
        if value > MAX_INT:
            self.error("integer exceeds signed 64-bit range")
        return value

    def value(self, depth=0):
        if depth > 64:
            self.error("value nesting exceeds 64")
        self.skip()
        if self.i >= len(self.data):
            self.error("missing value")
        ch = self.data[self.i : self.i + 1]
        self.i += 1
        if ch == b"~":
            count = self.unsigned()
            if self.data[self.i : self.i + 1] != b":":
                self.error("missing literal length separator")
            self.i += 1
            end = self.i + count
            if end > len(self.data):
                self.error("truncated literal")
            value = ""
            try:
                value = self.data[self.i : end].decode("utf-8", errors="strict")
            except UnicodeError:
                self.error("literal length splits UTF-8 or invalid UTF-8")
            self.i = end
            return value
        if ch == b"@":
            return Ref(self.ident())
        if ch in (b"+", b"?"):
            return True if ch == b"+" else None
        if ch == b"-" and (
            self.i == len(self.data) or not 48 <= self.data[self.i] <= 57
        ):
            return False
        if ch == b"[":
            result = []
            self.skip()
            if self.data[self.i : self.i + 1] == b"]":
                self.i += 1
                return result
            while True:
                result.append(self.value(depth + 1))
                self.skip()
                if self.data[self.i : self.i + 1] == b"]":
                    self.i += 1
                    return result
                self.take(b",")
        elif ch == b"{":
            result = {}
            self.skip()
            if self.data[self.i : self.i + 1] == b"}":
                self.i += 1
                return result
            while True:
                key = self.ident()
                if key in result:
                    self.error(f"duplicate field {key}")
                self.take(b"=")
                result[key] = self.value(depth + 1)
                self.skip()
                if self.data[self.i : self.i + 1] == b"}":
                    self.i += 1
                    return result
                self.take(b";")
        if ch == b"-" or b"0" <= ch <= b"9":
            if ch != b"-":
                self.i -= 1
            # Permit -2**63 while keeping all other limits strict.
            start = self.i
            while self.i < len(self.data) and 48 <= self.data[self.i] <= 57:
                self.i += 1
            if self.i - start > 19:
                self.error("integer exceeds signed 64-bit range")
            number = int(self.data[start : self.i]) * (-1 if ch == b"-" else 1)
            if not -(2**63) <= number <= MAX_INT:
                self.error("integer exceeds signed 64-bit range")
            return number
        self.i -= 1
        return Symbol(self.ident())

    def document(self):
        if self.data[:3] not in (b"PX1", b"PX2") or self.data[3:4] not in [
            bytes([w]) for w in WS
        ]:
            self.error("expected PX1 or PX2 header and whitespace")
        self.i = 3
        self.skip()
        revision = self.unsigned()
        if self.i == len(self.data) or self.data[self.i] not in WS:
            self.error("revision must be followed by whitespace")
        doc = Document(revision, format=int(self.data[2:3]))
        self.skip()
        while self.i < len(self.data):
            self.take(b"@")
            id_ = self.ident()
            if id_ in doc.records:
                self.error(f"duplicate record {id_}")
            self.take(b":")
            kind = self.ident()
            if len(kind) != 1 or not "A" <= kind <= "Z":
                self.error("kind must be one uppercase ASCII letter")
            fields = self.value()
            if not isinstance(fields, dict):
                self.error("record body must be a map")
            doc.records[id_] = Record(id_, kind, fields)
            if len(doc.records) > 100_000:
                self.error("too many records")
            self.skip()
        return doc


def parse(data: bytes | str) -> Document:
    if isinstance(data, str):
        try:
            data = data.encode("utf-8")
        except UnicodeError as error:
            raise PixlError("utf8", str(error)) from error
    return Parser(data).document()


def identifier(value):
    if not isinstance(value, str) or not IDENT.fullmatch(value.encode("utf-8")):
        raise PixlError("identifier", repr(value))
    return value.encode("ascii")


def encode_value(value, depth=0):
    if depth > 64:
        raise PixlError("depth", "value nesting exceeds 64")
    if isinstance(value, Ref):
        return b"@" + identifier(value.id)
    if isinstance(value, Symbol):
        return identifier(value.value)
    if isinstance(value, str):
        raw = value.encode("utf-8")
        return b"~" + str(len(raw)).encode() + b":" + raw
    if value is True:
        return b"+"
    if value is False:
        return b"-"
    if value is None:
        return b"?"
    if type(value) is int and -(2**63) <= value <= MAX_INT:
        return str(value).encode()
    if isinstance(value, list):
        return b"[" + b",".join(encode_value(v, depth + 1) for v in value) + b"]"
    if isinstance(value, dict):
        return (
            b"{"
            + b";".join(
                identifier(k) + b"=" + encode_value(value[k], depth + 1)
                for k in sorted(value)
            )
            + b"}"
        )
    raise PixlError("value_type", repr(type(value)))


def encode_record(record):
    if not isinstance(record.kind, str) or not re.fullmatch("[A-Z]", record.kind):
        raise PixlError("kind", repr(record.kind))
    return (
        b"@"
        + identifier(record.id)
        + b":"
        + record.kind.encode()
        + encode_value(record.fields)
    )


def encode(doc):
    if type(doc.revision) is not int or not 0 <= doc.revision <= MAX_INT:
        raise PixlError("revision", str(doc.revision))
    if type(doc.format) is not int or doc.format not in (1, 2):
        raise PixlError("format", "expected integer 1 or 2")
    if any(id_ != rec.id for id_, rec in doc.records.items()):
        raise PixlError("record_id", "map key differs from record ID")
    data = (
        b"PX"
        + str(doc.format).encode()
        + b" "
        + str(doc.revision).encode()
        + b"\n"
        + b"".join(encode_record(doc.records[k]) + b"\n" for k in sorted(doc.records))
    )
    if len(data) > MAX_BYTES or len(doc.records) > 100_000:
        raise PixlError("input_size", "document exceeds limits")
    return data


def digest(doc):
    return hashlib.sha256(encode(doc)).hexdigest()


def record_hash(record):
    return hashlib.sha256(encode_record(record)).hexdigest()


def to_data(value):
    """Lossless host-JSON representation; this is not the UDL wire syntax."""
    if isinstance(value, Ref):
        return {"$ref": value.id}
    if isinstance(value, Symbol):
        return {"$symbol": value.value}
    if isinstance(value, list):
        return [to_data(v) for v in value]
    if isinstance(value, dict):
        return {k: to_data(v) for k, v in value.items()}
    return value
