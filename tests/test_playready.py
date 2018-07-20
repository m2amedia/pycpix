import pytest
from cpix.drm import playready


PLAYREADY_TEST_KEY_SEED = b"XVBovsmzhP9gRIZxWfFta3VVRPzVEWmJsazEJ46I"
PLAYREADY_TEST_URL = "https://test.playready.microsoft.com/service/rightsmanager.asmx"


def test_generate_key():
    kid = b"8ba94ade-6eb9-449d-b44f-a5beefaf43b0"

    cek = playready.generate_content_key(kid, PLAYREADY_TEST_KEY_SEED)

    assert cek == b"DBFD6922C321C4BB486F4A1C44097ED6"


def test_checksum():
    kid = b"8ba94ade-6eb9-449d-b44f-a5beefaf43b0"
    cek = b"DBFD6922C321C4BB486F4A1C44097ED6"

    checksum = playready.checksum(kid, cek)

    assert checksum == b"Me48z71nuqY="


def test_generate_wrmheader():
    keys = [{
        "key_id": b"8ba94ade-6eb9-449d-b44f-a5beefaf43b0",
        "key": b"DBFD6922C321C4BB486F4A1C44097ED6"
    }]

    wrmheader = playready.generate_wrmheader(keys, PLAYREADY_TEST_URL)

    assert wrmheader == b'<\x00W\x00R\x00M\x00H\x00E\x00A\x00D\x00E\x00R\x00 \x00x\x00m\x00l\x00n\x00s\x00=\x00"\x00h\x00t\x00t\x00p\x00:\x00/\x00/\x00s\x00c\x00h\x00e\x00m\x00a\x00s\x00.\x00m\x00i\x00c\x00r\x00o\x00s\x00o\x00f\x00t\x00.\x00c\x00o\x00m\x00/\x00D\x00R\x00M\x00/\x002\x000\x000\x007\x00/\x000\x003\x00/\x00P\x00l\x00a\x00y\x00R\x00e\x00a\x00d\x00y\x00H\x00e\x00a\x00d\x00e\x00r\x00"\x00 \x00v\x00e\x00r\x00s\x00i\x00o\x00n\x00=\x00"\x004\x00.\x002\x00.\x000\x00.\x000\x00"\x00>\x00<\x00D\x00A\x00T\x00A\x00>\x00<\x00P\x00R\x00O\x00T\x00E\x00C\x00T\x00I\x00N\x00F\x00O\x00>\x00<\x00K\x00I\x00D\x00S\x00>\x00<\x00K\x00I\x00D\x00 \x00A\x00L\x00G\x00I\x00D\x00=\x00"\x00A\x00E\x00S\x00C\x00T\x00R\x00"\x00 \x00C\x00H\x00E\x00C\x00K\x00S\x00U\x00M\x00=\x00"\x00M\x00e\x004\x008\x00z\x007\x001\x00n\x00u\x00q\x00Y\x00=\x00"\x00 \x00V\x00A\x00L\x00U\x00E\x00=\x00"\x003\x00k\x00q\x00p\x00i\x007\x00l\x00u\x00n\x00U\x00S\x000\x00T\x006\x00W\x00+\x007\x006\x009\x00D\x00s\x00A\x00=\x00=\x00"\x00>\x00<\x00/\x00K\x00I\x00D\x00>\x00<\x00/\x00K\x00I\x00D\x00S\x00>\x00<\x00/\x00P\x00R\x00O\x00T\x00E\x00C\x00T\x00I\x00N\x00F\x00O\x00>\x00<\x00L\x00A\x00_\x00U\x00R\x00L\x00>\x00h\x00t\x00t\x00p\x00s\x00:\x00/\x00/\x00t\x00e\x00s\x00t\x00.\x00p\x00l\x00a\x00y\x00r\x00e\x00a\x00d\x00y\x00.\x00m\x00i\x00c\x00r\x00o\x00s\x00o\x00f\x00t\x00.\x00c\x00o\x00m\x00/\x00s\x00e\x00r\x00v\x00i\x00c\x00e\x00/\x00r\x00i\x00g\x00h\x00t\x00s\x00m\x00a\x00n\x00a\x00g\x00e\x00r\x00.\x00a\x00s\x00m\x00x\x00<\x00/\x00L\x00A\x00_\x00U\x00R\x00L\x00>\x00<\x00/\x00D\x00A\x00T\x00A\x00>\x00<\x00/\x00W\x00R\x00M\x00H\x00E\x00A\x00D\x00E\x00R\x00>\x00'


def test_generate_playready_object():
    keys = [{
        "key_id": b"8ba94ade-6eb9-449d-b44f-a5beefaf43b0",
        "key": b"DBFD6922C321C4BB486F4A1C44097ED6"
    }]

    wrmheader = playready.generate_wrmheader(keys, PLAYREADY_TEST_URL)

    pro = playready.generate_playready_object(wrmheader)

    assert pro == b'\x8e\x02\x00\x00\x01\x00\x01\x00\x84\x02<\x00W\x00R\x00M\x00H\x00E\x00A\x00D\x00E\x00R\x00 \x00x\x00m\x00l\x00n\x00s\x00=\x00"\x00h\x00t\x00t\x00p\x00:\x00/\x00/\x00s\x00c\x00h\x00e\x00m\x00a\x00s\x00.\x00m\x00i\x00c\x00r\x00o\x00s\x00o\x00f\x00t\x00.\x00c\x00o\x00m\x00/\x00D\x00R\x00M\x00/\x002\x000\x000\x007\x00/\x000\x003\x00/\x00P\x00l\x00a\x00y\x00R\x00e\x00a\x00d\x00y\x00H\x00e\x00a\x00d\x00e\x00r\x00"\x00 \x00v\x00e\x00r\x00s\x00i\x00o\x00n\x00=\x00"\x004\x00.\x002\x00.\x000\x00.\x000\x00"\x00>\x00<\x00D\x00A\x00T\x00A\x00>\x00<\x00P\x00R\x00O\x00T\x00E\x00C\x00T\x00I\x00N\x00F\x00O\x00>\x00<\x00K\x00I\x00D\x00S\x00>\x00<\x00K\x00I\x00D\x00 \x00A\x00L\x00G\x00I\x00D\x00=\x00"\x00A\x00E\x00S\x00C\x00T\x00R\x00"\x00 \x00C\x00H\x00E\x00C\x00K\x00S\x00U\x00M\x00=\x00"\x00M\x00e\x004\x008\x00z\x007\x001\x00n\x00u\x00q\x00Y\x00=\x00"\x00 \x00V\x00A\x00L\x00U\x00E\x00=\x00"\x003\x00k\x00q\x00p\x00i\x007\x00l\x00u\x00n\x00U\x00S\x000\x00T\x006\x00W\x00+\x007\x006\x009\x00D\x00s\x00A\x00=\x00=\x00"\x00>\x00<\x00/\x00K\x00I\x00D\x00>\x00<\x00/\x00K\x00I\x00D\x00S\x00>\x00<\x00/\x00P\x00R\x00O\x00T\x00E\x00C\x00T\x00I\x00N\x00F\x00O\x00>\x00<\x00L\x00A\x00_\x00U\x00R\x00L\x00>\x00h\x00t\x00t\x00p\x00s\x00:\x00/\x00/\x00t\x00e\x00s\x00t\x00.\x00p\x00l\x00a\x00y\x00r\x00e\x00a\x00d\x00y\x00.\x00m\x00i\x00c\x00r\x00o\x00s\x00o\x00f\x00t\x00.\x00c\x00o\x00m\x00/\x00s\x00e\x00r\x00v\x00i\x00c\x00e\x00/\x00r\x00i\x00g\x00h\x00t\x00s\x00m\x00a\x00n\x00a\x00g\x00e\x00r\x00.\x00a\x00s\x00m\x00x\x00<\x00/\x00L\x00A\x00_\x00U\x00R\x00L\x00>\x00<\x00/\x00D\x00A\x00T\x00A\x00>\x00<\x00/\x00W\x00R\x00M\x00H\x00E\x00A\x00D\x00E\x00R\x00>\x00'


def test_generate_pssh():
    keys = [{
        "key_id": b"8ba94ade-6eb9-449d-b44f-a5beefaf43b0",
        "key": b"DBFD6922C321C4BB486F4A1C44097ED6"
    }]

    pssh = playready.generate_pssh(keys, PLAYREADY_TEST_URL)

    assert pssh == b'\x00\x00\x02\xc2pssh\x01\x00\x00\x00\x9a\x04\xf0y\x98@B\x86\xab\x92\xe6[\xe0\x88_\x95\x00\x00\x00\x01\x8b\xa9J\xden\xb9D\x9d\xb4O\xa5\xbe\xef\xafC\xb0\x00\x00\x02\x8e\x8e\x02\x00\x00\x01\x00\x01\x00\x84\x02<\x00W\x00R\x00M\x00H\x00E\x00A\x00D\x00E\x00R\x00 \x00x\x00m\x00l\x00n\x00s\x00=\x00"\x00h\x00t\x00t\x00p\x00:\x00/\x00/\x00s\x00c\x00h\x00e\x00m\x00a\x00s\x00.\x00m\x00i\x00c\x00r\x00o\x00s\x00o\x00f\x00t\x00.\x00c\x00o\x00m\x00/\x00D\x00R\x00M\x00/\x002\x000\x000\x007\x00/\x000\x003\x00/\x00P\x00l\x00a\x00y\x00R\x00e\x00a\x00d\x00y\x00H\x00e\x00a\x00d\x00e\x00r\x00"\x00 \x00v\x00e\x00r\x00s\x00i\x00o\x00n\x00=\x00"\x004\x00.\x002\x00.\x000\x00.\x000\x00"\x00>\x00<\x00D\x00A\x00T\x00A\x00>\x00<\x00P\x00R\x00O\x00T\x00E\x00C\x00T\x00I\x00N\x00F\x00O\x00>\x00<\x00K\x00I\x00D\x00S\x00>\x00<\x00K\x00I\x00D\x00 \x00A\x00L\x00G\x00I\x00D\x00=\x00"\x00A\x00E\x00S\x00C\x00T\x00R\x00"\x00 \x00C\x00H\x00E\x00C\x00K\x00S\x00U\x00M\x00=\x00"\x00M\x00e\x004\x008\x00z\x007\x001\x00n\x00u\x00q\x00Y\x00=\x00"\x00 \x00V\x00A\x00L\x00U\x00E\x00=\x00"\x003\x00k\x00q\x00p\x00i\x007\x00l\x00u\x00n\x00U\x00S\x000\x00T\x006\x00W\x00+\x007\x006\x009\x00D\x00s\x00A\x00=\x00=\x00"\x00>\x00<\x00/\x00K\x00I\x00D\x00>\x00<\x00/\x00K\x00I\x00D\x00S\x00>\x00<\x00/\x00P\x00R\x00O\x00T\x00E\x00C\x00T\x00I\x00N\x00F\x00O\x00>\x00<\x00L\x00A\x00_\x00U\x00R\x00L\x00>\x00h\x00t\x00t\x00p\x00s\x00:\x00/\x00/\x00t\x00e\x00s\x00t\x00.\x00p\x00l\x00a\x00y\x00r\x00e\x00a\x00d\x00y\x00.\x00m\x00i\x00c\x00r\x00o\x00s\x00o\x00f\x00t\x00.\x00c\x00o\x00m\x00/\x00s\x00e\x00r\x00v\x00i\x00c\x00e\x00/\x00r\x00i\x00g\x00h\x00t\x00s\x00m\x00a\x00n\x00a\x00g\x00e\x00r\x00.\x00a\x00s\x00m\x00x\x00<\x00/\x00L\x00A\x00_\x00U\x00R\x00L\x00>\x00<\x00/\x00D\x00A\x00T\x00A\x00>\x00<\x00/\x00W\x00R\x00M\x00H\x00E\x00A\x00D\x00E\x00R\x00>\x00'