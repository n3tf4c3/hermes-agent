"""Security and compatibility checks for the bundled authentication dependencies.

The options reuse regression is GHSA-gvp8-978c-rx2q. Google auth's real
client API also exercises the OAuthlib 4 transition without contacting a provider.
"""

import base64
import hashlib
from urllib.parse import parse_qs, urlparse

import jwt
import pytest


def test_unverified_jwt_peek_does_not_disable_later_expiration_checks():
    secret = "dependency-security-test-key-32bytes"
    expired = jwt.encode({"exp": 1, "sub": "fixture"}, secret, algorithm="HS256")
    options = {"verify_signature": False}

    jwt.decode(expired, options=options)

    assert options == {"verify_signature": False}
    options["verify_signature"] = True
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(expired, secret, algorithms=["HS256"], options=options)


def test_google_authorization_flow_keeps_s256_pkce():
    flow_module = pytest.importorskip("google_auth_oauthlib.flow")
    flow = flow_module.Flow.from_client_config(
        {
            "installed": {
                "client_id": "fixture.apps.googleusercontent.com",
                "client_secret": "fixture-client-secret",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["openid"],
        autogenerate_code_verifier=True,
    )
    flow.redirect_uri = "http://127.0.0.1:8765/callback"

    url, state = flow.authorization_url()

    query = parse_qs(urlparse(url).query)
    expected = (
        base64
        .urlsafe_b64encode(hashlib.sha256(flow.code_verifier.encode("ascii")).digest())
        .rstrip(b"=")
        .decode("ascii")
    )
    assert query["code_challenge"] == [expected]
    assert query["code_challenge_method"] == ["S256"]
    assert query["state"] == [state]
    assert query["redirect_uri"] == [flow.redirect_uri]
