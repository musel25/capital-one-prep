"""A supplied IANA TZif loader for judge images without timezone files."""
from pathlib import Path

_DATA = (Path(__file__).parent / 'timezones.b85').read_text().strip()
TIMEZONE_SUPPORT = '''# Supplied offline IANA timezone data. Keep this support code.
import base64 as _tz_b64
import zlib as _tz_zlib
import json as _tz_json
from io import BytesIO as _TZBytesIO
from functools import lru_cache as _tz_cache
from zoneinfo import ZoneInfo as _SystemZoneInfo, ZoneInfoNotFoundError
_TZ_ARCHIVE = %r

@_tz_cache(maxsize=1)
def _timezone_data():
    return _tz_json.loads(_tz_zlib.decompress(_tz_b64.b85decode(_TZ_ARCHIVE)))

@_tz_cache(maxsize=None)
def ZoneInfo(key):
    """Load a standard ZoneInfo object from the supplied offline database."""
    if key not in _timezone_data():
        raise ZoneInfoNotFoundError(key)
    return _SystemZoneInfo.from_file(_TZBytesIO(_tz_b64.b64decode(_timezone_data()[key])), key=key)

''' % _DATA
