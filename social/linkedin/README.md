# LinkedIn direct publishing through GitHub Actions — manual only

**Status:** Publishing integration staged; LinkedIn OAuth app and user consent still required. **No post has been published.**

This replaces the need for Metricool for personal-profile research updates. Only the authorized LinkedIn member can authorize posting to their own profile. LinkedIn's **Share on LinkedIn** self-service product grants `w_member_social`. Use **Sign in with LinkedIn using OpenID Connect** (`openid profile`) to obtain the correct profile ID; never substitute a guessed person URN. The five-panel carousel is a **single PDF document post**, not a sponsored LinkedIn carousel.

## 1. One-time LinkedIn Developer App setup (user action)

1. Open https://www.linkedin.com/developers/apps and create an app such as **Cooperative Traffic Research Publisher**. LinkedIn currently requires a linked **LinkedIn Page** for new developer apps, plus an app logo and privacy-policy URL. Use your own Page (or create one); you may have to verify the Page association. This **does not mean publishing to that Page**: the integration targets your personal member profile.
2. In **Products**, enable both:
   - **Share on LinkedIn** — provides `w_member_social`;
   - **Sign In with LinkedIn using OpenID Connect** — provides `openid` and `profile`.
   Check the app's **Auth** tab to confirm all three scopes are available.
3. Under **Auth > OAuth 2.0 settings**, register this exact authorized redirect URL:
   `https://oauth.pstmn.io/v1/callback`.
   This is the official Postman OAuth callback, not a server managed by this repository. Alternatively, use your own trusted HTTPS callback and adapt the local helper to match exactly. Never paste an access token, client secret or authorization code into ChatGPT.
4. The **Client ID** and **Client Secret** are needed **only on your own computer** to complete the standard 3-legged authorization. The secret is never committed to the public repository.

Official references: [LinkedIn Developer app](https://www.linkedin.com/developers/apps), [API product access](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access), [authorization-code OAuth](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow), [OpenID Connect](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin-v2).

## 2. Authorize on your own Mac; store credentials directly as encrypted GitHub Actions Secrets

Install and authorize the [GitHub CLI](https://cli.github.com/) on your Mac if needed:

```bash
brew install gh
gh auth login
```

Clone the repository if it is not already available locally, or pull the latest `main`. From its root run:

```bash
python3 social/linkedin/authorize_local.py
```

The helper prompts securely for your app's Client ID and Client Secret, opens LinkedIn's consent page in your browser, verifies the OAuth `state` against the redirected Postman callback URL, exchanges the short-lived authorization code **locally**, and fetches your account identifier using the OIDC `userinfo` endpoint. You paste the **full redirected URL into your own local terminal only** (never into this chat, an issue, Actions logs, or a public comment).

It writes **only** these two values directly to GitHub encrypted Actions Secrets with `gh secret set`, without printing or saving them to a file:

- `LINKEDIN_ACCESS_TOKEN`
- `LINKEDIN_PERSON_URN`

You must have rights to manage GitHub repository Actions Secrets. Check their *names*, not their contents, at https://github.com/yonnastgetahun/cooperative_traffic_research/settings/secrets/actions.

**Security:** Do not put secrets in a README, an issue, pull-request diff, public workflow input, copied shell command, or chat. Authorization codes expire rapidly and can be used only once. LinkedIn access tokens generally last **60 days**; rerun the user-owned local authorization when needed. Programmatic refresh is not automatically available to self-service applications. If Postman callback consent or a product permission is unavailable, stop and inspect the app's Auth tab rather than using workarounds.

## 3. The approved visual carousel

The approved five-page LinkedIn document is `cooperative_traffic_pivot_linkedin_carousel.pdf`, with **exact SHA256**:

```
60df1741d718cccb8dabf2f4052ac4dabfb237daa04887a207226deaacbc05df
```

After downloading that PDF from this conversation, upload it in the GitHub website to **exactly** `social/linkedin/traffic_pivot_carousel.pdf`, preserving the original bytes. GitHub Actions verifies the hash and **refuses to publish a different or missing PDF**. The approved caption is versioned separately at `social/linkedin/traffic_pivot_announcement.txt`.

LinkedIn's personal-profile Posts API supports a document attachment for organic posts. This is **not** a native sponsored carousel; it is one five-page document asset. Reference: [Documents API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/documents-api?view=li-lms-2026-08), [Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?view=li-lms-2026-08).

## 4. Verify OAuth before any publication

Open https://github.com/yonnastgetahun/cooperative_traffic_research/actions/workflows/linkedin-manual-personal-document.yml and choose **Run workflow**:

- `action=validate`: offline checks; **no credentials and no LinkedIn API requests**.
- `action=verify`: read-only OIDC identity verification against the stored GitHub Secrets; **NO POST**.
- `action=publish`: **only after explicit approval of the final caption and PDF**; requires the exact confirmation phrase `YES_PUBLISH_APPROVED_LINKEDIN_DOCUMENT`. Uploads the approved SHA-verified PDF, waits for document `AVAILABLE` status, then attempts **one** Posts API creation. Never automatically retries an ambiguous publication.

The workflow has **only `workflow_dispatch`**. It will not post as a result of a git push, a merged pull request, a scheduled timer, or a PR. `github.run_attempt == 1` blocks rerunning a published job. If post creation is ambiguous, inspect your LinkedIn profile before considering any future attempt; duplicate publication must not be automated.

The underlying publisher is `social/linkedin/publish_linkedin.py` (Python standard library only). It uses Posts API version **202609** and `X-Restli-Protocol-Version: 2.0.0` in REST calls. Update the pinned marketing API version prospectively if LinkedIn sunsets it; do not silently change it during an approved publication.

## 5. Status and editorial boundaries

- **GitHub setup does not authorize a post by itself.** Publishing requires a manual workflow invocation and exact confirmation string after the media and copy have been reviewed.
- LinkedIn profile posting is independent of Metricool. X stays on the separate existing GitHub-to-X workflow.
- Do not present T1 as a demonstration of positive cooperative traffic benefits or assert SUMO is invalid. The experimental findings show confounding and a source-supported random-stream coupling mechanism, but not its proven numerical causal share.
- The next research direction is a **feasibility assessment of independent simulation frameworks**, not an independently validated cross-model result already achieved.
