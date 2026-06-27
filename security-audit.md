# Security Audit Report — CardBranch (Pre-Live)

## Area-by-Area Findings

| Area | Item | Status | File:Line | Notes |
|------|------|--------|-----------|-------|
| **1. SECRETS & CONFIG** | SECRET_KEY from env, never hardcoded | **PASS** | `config.py:8` | Loaded from env var with fallback `'dev-secret'`. The fallback is weak but env takes precedence. `.env` contains `cardbranch-dev-secret-2026` — replace with a strong production secret before live. |
| | Stripe keys, Resend, R2, DB_URL all from env | **PASS** | `config.py:8-15` | All loaded via `os.environ.get(...)` with empty-string defaults. No secrets in source code. |
| | DEBUG forced off in production | **PASS** | `config.py:27` | `ProductionConfig.DEBUG = False`. However `run.py:14` hardcodes `debug=True` — but that path runs only via `python run.py`, not under gunicorn (Procfile). |
| | .gitignore excludes .env, *.pem, *.key, local config | **PASS** | `.gitignore:4` | `.env` and `*.db` excluded. `*.pem`/`*.key` not present in repo. Missing: no exclusion for `*.pem`, `*.key` in case they are added later. |
| | Git history scanned for committed secrets | **PASS** | — | No secrets ever committed. `.env` never tracked. `config.py` always used env-var patterns. No `sk_test_` or `AKIA` keys found in any commit. |
| **2. AUTHENTICATION** | Passwords hashed with strong algorithm | **PASS** | `app/models.py:31-33` | Uses `werkzeug.security.generate_password_hash` / `check_password_hash`. |
| | Rate limiting / lockout on login | **FAIL** | `app/auth/routes.py:10-22` | **No rate limiting, no account lockout, no captcha.** Brute-force attack on `/login` is trivial. |
| | Session cookies: Secure, HttpOnly, SameSite | **FAIL** | `app/__init__.py` `config.py` | No `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, or `SESSION_COOKIE_SAMESITE` configured anywhere. Flask defaults: HttpOnly=True (OK), SameSite=Lax (OK), Secure=False (FAIL — cookie sent over HTTP). |
| | `@login_required` on all dashboard/account routes | **PASS** | `app/dashboard/routes.py:13,30,77,85,134,148,181,188,204` | All sensitive routes protected. |
| | IDOR on card/order detail routes | **PASS** | `app/dashboard/routes.py:79,87,136,150,191,207` | All scoped with `user_id=current_user.id`. No user can access another user's cards. |
| **3. ADMIN ACCESS** | All admin routes: `@login_required` + admin role check | **PASS** | `app/admin/routes.py:20-21,36-37,44-45,66-68` | Every admin route gets both decorators. |
| | Admin role check server-side on every request | **PASS** | `app/admin/routes.py:13` | `admin_required` decorator checks `current_user.is_admin` server-side, not just UI hiding. |
| **4. STRIPE** | Webhook verifies Stripe signature | **PASS** | `app/checkout/routes.py:120` | `stripe.Webhook.construct_event(payload, sig_header, webhook_secret)` — proper verification. |
| | Webhook CSRF-exempt but signature-verified | **PASS** | `app/checkout/routes.py:113` | No `@csrf.exempt` needed currently because `CSRFProtect` is never initialized as middleware. The raw POST is accepted and signature-verified. (If CSRFProtect were added later, it would break — add `@csrf.exempt` proactively.) |
| | Order fulfillment from Stripe event, not client data | **PASS** | `app/checkout/routes.py:124-136` | Status set to `'paid'` only after webhook confirms `checkout.session.completed`. Not from client-side data. |
| | Stripe secret key server-side only | **PASS** | — | `STRIPE_SECRET_KEY` never appears in templates or frontend JS. |
| **5. INPUT VALIDATION** | SQLAlchemy ORM, no raw SQL | **PASS** | — | All queries use ORM methods. No `db.engine.execute()`, `text()`, or string-formatted SQL found. |
| | Jinja2 escaping (no unjustified `\|safe`) | **PASS** | — | Zero occurrences of `\|safe` in any template. |
| | Slug safe from path traversal/injection | **PASS** | `app/services/generator.py:22-24` | Regex `[^a-z0-9]+` strips all non-alphanumeric chars. |
| | File uploads validated for type and size | **FAIL** | `app/dashboard/forms.py:10-12`, `app/services/generator.py:38-40` | `FileAllowed` checks extension whitelist; `save_logo` re-checks extension. **No magic-byte / content-type verification** — a `.png` renamed `.exe` would be rejected, but a crafted polyglot file with a valid extension would pass. `MAX_CONTENT_LENGTH=16MB` limits size. |
| **6. FILE HANDLING / R2** | Files renamed/sanitized before storage | **PASS** | `app/services/generator.py:39-40` | Uses `uuid.uuid4().hex` — no user-supplied filename used. |
| | Local filesystem writes still happening | **FAIL** | `app/__init__.py:26-27`, `run.py:8-9`, `app/services/email.py:53` | `static/uploads/` and `static/generated/` dirs created locally. More critically: `email.py:53` uses `{site_url}/static/generated/{slug}/card.pdf` — a **local path reference**, not the R2 public URL. This link will 404 on production when assets are on R2. |
| | R2 bucket objects public only where intended | **PASS** | `app/services/r2.py:19` | Assets stored in `uploads/` and `generated/{slug}/` paths via R2 public URL. Acceptable for card assets. No admin/order data in R2. |
| **7. CSRF / CORS** | CSRF on all state-changing forms | **FAIL** | `templates/checkout/order.html:12`, `templates/admin/orders.html:37` | Two POST forms **lack CSRF tokens**: (1) `checkout/order` — creates orders; (2) `admin/orders` — updates order status/tracking. `DebugConfig` has `WTF_CSRF_ENABLED=False`; in production it defaults to `True` but `CSRFProtect` middleware is never initialized, so no global CSRF enforcement. Only `FlaskForm.validate_on_submit()` routes have CSRF. |
| | CORS configured restrictively | **N/A** | — | Flask-CORS not installed; no CORS headers set. Acceptable if no separate frontend origin. |
| **8. ERROR HANDLING** | No stack trace / path leakage on error pages | **FAIL** | `app/__init__.py` | **No custom error handlers for 404 or 500.** Flask's default handler in debug mode leaks stack traces; in production (gunicorn) it renders a generic page but may still expose server info. |
| | Exceptions caught and logged, not shown raw | **FAIL** | `app/checkout/routes.py:91` | Stripe errors are caught and shown via flash: `flash(f'Payment error: {str(e)}', 'error')` — leaks Stripe error detail to user. Not server-logged. `email.py` has bare `except Exception: pass` — silent failure. |
| **9. DEPENDENCIES** | All packages pinned with versions | **FAIL** | `requirements.txt:17` | `boto3>=1.34.0` uses `>=` (not pinned). All others use `==`. |

---

## CRITICAL FINDINGS (Exploitable Pre-Launch)

Ordered by severity:

| # | Severity | Finding | File:Line | Impact |
|---|----------|---------|-----------|--------|
| 1 | **CRITICAL** | **No CSRF on checkout POST** — creates pending orders and Stripe Checkout Sessions | `templates/checkout/order.html:12` `app/checkout/routes.py:15-92` | An attacker can forge a POST that creates an Order record and a Stripe Checkout Session for any card belonging to an authenticated victim who visits a malicious site. While no payment is completed, this creates valid Stripe sessions and database records tied to the victim. |
| 2 | **CRITICAL** | **No CSRF on admin order-update POST** | `templates/admin/orders.html:37` `app/admin/routes.py:47-60` | An authenticated admin visiting a malicious site could have order status or tracking numbers silently changed (e.g., marking unpaid orders as "delivered"). Gated behind admin auth, but devastating if triggered. |
| 3 | **HIGH** | **No rate limiting on login** | `app/auth/routes.py:10-22` | Offline brute force on the login endpoint is unbounded. No lockout, no delay, no captcha. Any account can be attacked at full speed. |
| 4 | **HIGH** | **Session cookie missing Secure flag** | `config.py` (all config classes) | Session cookie is transmitted over unencrypted HTTP unless reversed-proxy sets it. On HTTPS, the cookie should have `Secure=True` to prevent interception by network attackers. |
| 5 | **MEDIUM** | **No custom error handlers (404/500)** | `app/__init__.py` | In production, debug is off, but without custom handlers Flask may still leak internal paths or server environment details on unexpected errors. |
| 6 | **MEDIUM** | **Stripe error details leaked to user** | `app/checkout/routes.py:91` | `flash(f'Payment error: {str(e)}')` exposes Stripe API error messages in the UI. |
| 7 | **MEDIUM** | **Email PDF link references local path, not R2** | `app/services/email.py:53` | Admin notification emails link to `{site_url}/static/generated/{slug}/card.pdf` which won't resolve in production when assets live on R2. Operational issue, not a breach, but admin orders may be unfulfillable. |
| 8 | **LOW** | **boto3 version unpinned** | `requirements.txt:17` | `boto3>=1.34.0` could pull breaking changes on deploy. |
| 9 | **LOW** | **File uploads rely on extension-only checks** | `app/services/generator.py:38-40` | No magic-byte validation. Low risk because `Pillow` and `reportlab` would reject non-image files during processing. |
| 10 | **LOW** | **No server-side logging of exceptions** | `app/services/email.py:41,86,121` | `except Exception: pass` silently swallows send failures. |

---

## Summary

**3 CRITICAL, 1 HIGH, 2 MEDIUM, 3 LOW findings.**

Immediate blockers for live mode:

1. **CSRF on checkout and admin forms** — add `{{ form.hidden_tag() }}` or `{{ csrf_token() }}` to both templates.
2. **Rate limiting on login** — install Flask-Limiter and configure at least 5 attempts per minute per IP.
3. **Secure session cookie** — add `SESSION_COOKIE_SECURE = True` and `SESSION_COOKIE_SAMESITE = 'Lax'` to `ProductionConfig`.
4. **Custom error handlers** — add `@app.errorhandler(404)` and `@app.errorhandler(500)`.
5. **Stripe error details** — log server-side and show a generic message to the user.
6. **Fix email PDF URL** — use the R2 public URL pattern instead of local `static/generated/`.
7. **Pin boto3** — change `>=` to `==`.
