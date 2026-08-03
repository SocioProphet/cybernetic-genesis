"""Minimal TritPack243 — vendored from SocioProphet/semantic-serdes (tools/tritpack.py).

Kept in lockstep by the shared contract: balanced-ternary digits {-1,0,+1} -> wire trits
{0,1,2}, little-endian, 5 wire-trits per byte (3**5 = 243), canonical hash = sha256 over the
packed bytes. This is the encoder Genesis uses to emit a TwinEventEnvelope AS a tritrpc_envelope,
so the same bytes ride the semantic-serdes / quantum-prophet ternary rail. Do not diverge from
the canonical source.
"""
from __future__ import annotations

import hashlib

TRIT_BASE = 3
TRITS_PER_BYTE = 5
BYTE_RADIX = TRIT_BASE ** TRITS_PER_BYTE  # 243


def bytes_to_wire_trits(data: bytes) -> list[int]:
    """A byte string -> wire trits {0,1,2}. Each byte (0..255) expands to 6 base-3 digits
    (3**6 = 729 > 255), little-endian, so any byte round-trips exactly."""
    trits: list[int] = []
    for b in data:
        v = b
        for _ in range(6):
            trits.append(v % TRIT_BASE)
            v //= TRIT_BASE
    return trits


def wire_trits_to_bytes(trits: list[int]) -> bytes:
    if len(trits) % 6:
        raise ValueError(f"trit count {len(trits)} not a multiple of 6")
    out = bytearray()
    for i in range(0, len(trits), 6):
        v = 0
        for j in range(6):
            v += trits[i + j] * (TRIT_BASE ** j)
        if v > 255:
            raise ValueError(f"decoded value {v} > 255")
        out.append(v)
    return bytes(out)


def pack_trits(trits: list[int]) -> bytes:
    for t in trits:
        if t not in (0, 1, 2):
            raise ValueError(f"wire trit {t!r} not in {{0,1,2}}")
    out = bytearray()
    for i in range(0, len(trits), TRITS_PER_BYTE):
        group = trits[i:i + TRITS_PER_BYTE]
        value = sum(t * (TRIT_BASE ** j) for j, t in enumerate(group))
        out.append(value)
    return bytes(out)


def unpack_trits(data: bytes, trit_len: int) -> list[int]:
    expected = (trit_len + TRITS_PER_BYTE - 1) // TRITS_PER_BYTE
    if len(data) != expected:
        raise ValueError(f"packed length {len(data)} != expected {expected} for {trit_len} trits")
    trits: list[int] = []
    for b in data:
        if b >= BYTE_RADIX:
            raise ValueError(f"byte {b} >= {BYTE_RADIX}; not a valid TritPack243 byte")
        v = b
        for _ in range(TRITS_PER_BYTE):
            trits.append(v % TRIT_BASE)
            v //= TRIT_BASE
    return trits[:trit_len]


def canonical_hash(data: bytes, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    h.update(data)
    return f"{algo}:{h.hexdigest()}"
