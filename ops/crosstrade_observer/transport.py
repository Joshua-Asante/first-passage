"""Fixed-origin, bounded CrossTrade GET transport. Never follows redirects."""
import json
import math
import re
import urllib.error
import urllib.parse
import urllib.request


class ReadError(Exception):
    """A public diagnostic code, never a provider message or URL."""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def _invalid_constant(_value):
    raise ValueError('nonfinite JSON')


def _finite_float(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError('overflow JSON number')
    return result


def _redact(value, secret):
    if isinstance(value, str):
        return value.replace(secret, '[REDACTED]')
    if isinstance(value, list):
        return [_redact(item, secret) for item in value]
    if isinstance(value, dict):
        return {_redact(key, secret): _redact(item, secret) for key, item in value.items()}
    return value


def _allowed(path):
    if not isinstance(path, str) or any(ord(c) < 32 for c in path):
        return False
    url = urllib.parse.urlsplit(path)
    if url.scheme or url.netloc or url.fragment:
        return False
    if url.path == '/v1/api/tv/fills/history':
        query = urllib.parse.parse_qs(url.query, keep_blank_values=True)
        return (set(query) <= {'account', 'limit', 'cursor', 'from', 'to'}
                and all(len(v) == 1 and v[0] for v in query.values()))
    if url.query:
        return False
    if url.path == '/v1/api/tv/accounts/snapshot':
        return True
    match = re.fullmatch(r'/v1/api/tv/accounts/([^/]+)/(positions|orders|fills)', url.path)
    if not match:
        return False
    account = urllib.parse.unquote(match[1])
    return bool(account and account not in ('.', '..')
                and not any(c in account for c in '/\\?#')
                and not any(ord(c) < 32 for c in account))


class ReadClient:
    """No configurable host, method, redirect policy or trade endpoint."""

    def __init__(self, secret):
        if not isinstance(secret, str) or not secret.strip() or any(c in secret for c in '\r\n'):
            raise ValueError('invalid credential')
        self._secret = secret
        self.opener = urllib.request.build_opener(_NoRedirect())

    def get(self, path):
        if not _allowed(path):
            raise ValueError('endpoint not allowed')
        req = urllib.request.Request('https://app.crosstrade.io' + path,
                                     headers={'Authorization': 'Bearer ' + self._secret,
                                              'Accept': 'application/json'}, method='GET')
        try:
            try:
                response = self.opener.open(req, timeout=15)
            except urllib.error.HTTPError as exc:
                response = exc
            with response:
                status = response.status
                raw = response.read(2_000_001)
            if 300 <= status < 400:
                raise ReadError('redirect_refused')
            if len(raw) > 2_000_000:
                raise ReadError('response_too_large')
            try:
                body = json.loads(raw, object_pairs_hook=_unique_pairs,
                                  parse_constant=_invalid_constant, parse_float=_finite_float)
                body = _redact(body, self._secret)
            except (ValueError, UnicodeError, RecursionError) as exc:
                raise ReadError('invalid_json') from exc
            return status, body
        except TimeoutError as exc:
            raise ReadError('timeout') from exc
        except (urllib.error.URLError, OSError) as exc:
            raise ReadError('transport_error') from exc
