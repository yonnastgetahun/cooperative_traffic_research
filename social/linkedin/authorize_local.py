#!/usr/bin/env python3
"""Interactive local LinkedIn authorization.

This runs on the user's machine, never in public GitHub Actions. It obtains a
member access token via LinkedIn's authorization-code flow and writes it
directly to GitHub Actions Secrets with the user's locally authenticated gh CLI.
Neither client secret nor access token is printed, committed or stored to disk.
"""
import getpass
import json
import secrets
import shutil
import subprocess
import sys
from urllib.parse import urlencode, urlsplit, parse_qs
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import webbrowser

REPOSITORY = "yonnastgetahun/cooperative_traffic_research"
REDIRECT = "https://oauth.pstmn.io/v1/callback"
SCOPES = "openid profile w_member_social"


def stop(message):
    raise RuntimeError(message)


def check_gh():
    if not shutil.which("gh"):
        stop("GitHub CLI not found. Install gh, then run gh auth login on this computer.")
    proc = subprocess.run(["gh", "auth", "status"], stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL, check=False)
    if proc.returncode != 0:
        stop("Run gh auth login before authorizing LinkedIn")


def set_github_secret(key, value):
    proc = subprocess.run(["gh", "secret", "set", key, "--repo", REPOSITORY],
                          input=value, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    if proc.returncode != 0:
        stop("Could not save GitHub secret " + key +
             ". Verify your GitHub repository permissions; do not paste secrets into chat.")


def main():
    check_gh()
    print("LinkedIn OAuth - credential exchange happens locally; tokens are not printed.")
    client_id = input("LinkedIn Developer App Client ID: ").strip()
    client_secret = getpass.getpass("LinkedIn Developer App Client Secret (hidden): ")
    if not client_id or not client_secret:
        stop("Client ID and client secret are required")
    state = secrets.token_urlsafe(36)
    query = urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT,
        "state": state,
        "scope": SCOPES,
    })
    url = "https://www.linkedin.com/oauth/v2/authorization?" + query
    print("Open the LinkedIn authorization page in your browser.")
    webbrowser.open(url)
    print("After LinkedIn redirects to the registered Postman callback, copy the")
    print("entire address-bar URL and paste it into THIS TERMINAL ONLY.")
    callback = input("Redirected callback URL (hidden neither here nor remotely): ").strip()
    parsed = urlsplit(callback)
    if parsed.scheme != "https" or parsed.netloc != "oauth.pstmn.io" or parsed.path != "/v1/callback":
        stop("Redirect is not the registered LinkedIn OAuth callback")
    q = parse_qs(parsed.query)
    if q.get("error"):
        stop("LinkedIn declined or rejected the authorization")
    if not secrets.compare_digest(q.get("state", [""])[0], state):
        stop("LinkedIn OAuth state did not match; no secret was stored")
    code = q.get("code", [""])[0]
    if not code:
        stop("No authorization code in callback URL")
    payload = urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode("utf-8")
    req = Request("https://www.linkedin.com/oauth/v2/accessToken",
                  data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"},
                  method="POST")
    try:
        with urlopen(req, timeout=30) as response:
            token_response = json.loads(response.read(50000))
    except HTTPError as exc:
        stop("LinkedIn rejected token exchange (HTTP %s). Check redirect, app, scopes." % exc.code)
    except URLError:
        stop("LinkedIn token exchange network error")
    token = token_response.get("access_token")
    if not token:
        stop("LinkedIn token endpoint returned no access token")
    granted = set(token_response.get("scope", "").split())
    if granted and not set(SCOPES.split()).issubset(granted):
        stop("LinkedIn token lacks required permissions; no secret stored")
    info_request = Request("https://api.linkedin.com/v2/userinfo",
                           headers={"Authorization": "Bearer " + token}, method="GET")
    try:
        with urlopen(info_request, timeout=30) as response:
            info = json.loads(response.read(50000))
    except HTTPError as exc:
        stop("LinkedIn userinfo check failed HTTP " + str(exc.code))
    except URLError:
        stop("LinkedIn userinfo network error")
    member_id = str(info.get("sub", ""))
    if not member_id or len(member_id) > 120:
        stop("No LinkedIn OIDC member ID returned")
    urn = "urn:li:person:" + member_id
    set_github_secret("LINKEDIN_ACCESS_TOKEN", token)
    set_github_secret("LINKEDIN_PERSON_URN", urn)
    print("Success: LinkedIn personal author and OAuth token saved in GitHub Secrets.")
    print("No post has been published.")
    print("Token lifetime from LinkedIn (days):", int(token_response.get("expires_in", 0))//86400)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("STOP: " + str(e), file=sys.stderr)
        raise SystemExit(1)
