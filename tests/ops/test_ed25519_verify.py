"""Pure-Python Ed25519 verification pinned to RFC 8032 vectors and a library cross-check."""
import os

import pytest

from ed25519_verify import verify

# RFC 8032 section 7.1: (public key, message, signature)
VECTORS = [
    ("d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a", "",
     "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"),
    ("3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c", "72",
     "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00"),
    ("fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025", "af82",
     "6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac18ff9b538d16f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a"),
]


@pytest.mark.parametrize("pk,msg,sig", VECTORS)
def test_rfc8032_vectors_verify(pk, msg, sig):
    """The RFC reference vectors verify exactly; no library is involved."""
    assert verify(bytes.fromhex(pk), bytes.fromhex(msg), bytes.fromhex(sig))


@pytest.mark.parametrize("pk,msg,sig", VECTORS)
def test_tampered_message_signature_or_key_fails(pk, msg, sig):
    """Any single flipped bit in message, signature or key is rejected."""
    key, message, signature = bytes.fromhex(pk), bytes.fromhex(msg), bytes.fromhex(sig)
    assert not verify(key, message + b"x", signature)
    flipped = bytearray(signature)
    flipped[0] ^= 1
    assert not verify(key, message, bytes(flipped))
    flipped = bytearray(signature)
    flipped[63] ^= 0x10
    assert not verify(key, message, bytes(flipped))
    other = bytearray(key)
    other[5] ^= 1
    assert not verify(bytes(other), message, signature)


def test_malformed_inputs_are_false_not_exceptions():
    """Wrong lengths, non-canonical S and undecodable points return False."""
    pk, msg, sig = (bytes.fromhex(v) for v in VECTORS[0])
    assert not verify(pk[:31], msg, sig)
    assert not verify(pk, msg, sig[:63])
    assert not verify(b"", msg, sig)
    high_s = sig[:32] + (2 ** 252 + 27742317777372353535851937790883648493).to_bytes(32, "little")
    assert not verify(pk, msg, high_s)
    assert not verify(b"\xff" * 32, msg, sig)
    assert not verify("not bytes", msg, sig)  # type: ignore[arg-type]


def test_cross_check_against_operator_side_library():
    """Signatures from the library the operator uses verify here; a wrong key does not."""
    cryptography = pytest.importorskip("cryptography")
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519
    for _ in range(3):
        key = ed25519.Ed25519PrivateKey.generate()
        pub = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        message = os.urandom(200)
        signature = key.sign(message)
        assert verify(pub, message, signature)
        assert not verify(pub, message[:-1], signature)
        other = ed25519.Ed25519PrivateKey.generate().public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        assert not verify(other, message, signature)


def test_small_order_keys_and_points_are_rejected():
    """The identity key with R = identity and S = 0 satisfies the raw equation; it must be refused."""
    from ed25519_verify import is_strong_public_key
    identity = (1).to_bytes(32, "little")            # y = 1, x = 0: the neutral element
    assert not is_strong_public_key(identity)
    assert not verify(identity, b"any envelope", identity + bytes(32))
    order_two = (2 ** 255 - 19 - 1).to_bytes(32, "little")   # y = -1: the point of order two
    assert not is_strong_public_key(order_two)
    pk, msg, sig = (bytes.fromhex(v) for v in VECTORS[0])
    assert is_strong_public_key(pk)
    assert not verify(pk, msg, identity + sig[32:])
