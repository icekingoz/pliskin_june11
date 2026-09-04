# AGENTS.md

This repo is a **pytest + Playwright + requests** test framework for two systems:

| Suite | Target | HTTP / browser |
|---|---|---|
| UI | [Swag Labs](https://www.saucedemo.com/) | Playwright (sync) + Chromium |
| API | [restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html) | `requests` only |

Python 3.12. Run everything from the **project root** with `python -m pytest` so `pythonpath = .` in `pytest.ini` resolves `pages` and `api`.

Credentials: `SAUCE_USERNAME` and `SAUCE_PASSWORD` from `.env` locally, GitHub Actions secrets in CI. Never commit secrets.

---

## Layout

```
pages/                    One class per Swag Labs screen (locators + actions, no asserts)
api/
  booking_client.py       One method per restful-booker endpoint (returns Response, no asserts)
  builders.py             make_booking(**overrides) — unique valid payloads
tests/ui/                 Browser tests
tests/api/                HTTP tests + tests/api/conftest.py
conftest.py               UI fixtures, session login (storage_state), Allure plugin hook
support/allure_hooks.py   Failure attachments; attach_exchange() for API
pytest.ini                base_url, chromium, html + Allure, --strict-markers
.github/workflows/tests.yml   UI job, API job, Allure site on master
```

`pytest-playwright` supplies `browser`, `context`, `page`, and `new_context`. Root `conftest.py` layers login and journey fixtures on top.

---

## Architecture

```
UI:  pytest-playwright page
       → LoginPage / InventoryPage / CartPage / CheckoutPage
       → tests/ui assert on locators or getter return values

API: ApiSession (base URL + timeout)
       → BookingAPIClient (endpoints)
       → make_booking() / created_booking fixture
       → tests/api assert on status_code and JSON
```

**Page objects and the API client never decide pass/fail.** They click, fill, GET/POST, and return locators, data, or `requests.Response`. Tests own every `assert`.

**Page objects are stateless.** They keep `page` and locators only. No cached totals, usernames, or step counters. Read live DOM (or getter methods that read it now).

**Navigation returns the next screen; staying put returns `self`.**

```python
inventory = login_page.login_user(user, pw)          # → InventoryPage
cart = inventory.add_item_to_cart("sauce-labs-backpack").open_cart()  # self, then CartPage
```

Local imports inside methods (e.g. `CartPage.logout`) break circular imports between page modules. Keep that pattern.

**Checkout is one class** covering information → overview → complete (`CheckoutPage`). Same `fill_information()` for happy and sad paths; the test asserts title vs error.

**Fixtures hold setup that is not the thing under test.** Prefer an existing fixture over repeating login or cart-seeding in the test body.

| Fixture | What you get |
|---|---|
| `login_page` | Open login screen (`page`, not logged in) |
| `auth_state` (session) | Saved `playwright/.auth/state.json` after a real login |
| `logged_in_page` | Fresh page with that storage state |
| `inventory_page` | Logged in, on `/inventory.html` |
| `cart_with` | Factory: `cart_with("sauce-labs-backpack", ...)` → `CartPage` |
| `checkout_started` | Backpack in cart, on checkout information |
| `completed_order` | Finished checkout |
| `booking_client` | Authenticated `BookingAPIClient` |
| `created_booking` | `(booking_id, payload)`; **deletes after the test** (even on failure) |

`inventory_page` uses session auth, not a full UI login per test. Use `login_page` when the test **is** about login.

**API data:** `make_booking()` builds a valid body with unique `firstname`/`lastname` (`Solid{uuid}` / `Snake{uuid}`). Override fields with kwargs. `created_booking` yields then deletes; no asserts after `yield`. Treat “already gone” as success in teardown.

---

## Hard rules (do not violate)

1. **Assertions live only in tests** — never in `pages/` or `api/`.
2. **UI: pytest `assert` only.** Do not import or use `from playwright.sync_api import expect`. Do not use `time.sleep()`.
3. **API: `requests` only** (including `ApiSession` / `BookingAPIClient`). No Playwright `APIRequestContext`, no `httpx`.
4. **Do not weaken assertions to make a test pass.** Fix locators, waits, product, or data. Do not comment out, broaden, or replace a specific check with a truthy check.
5. **Each test stands alone** — own data, any order. No dependence on another test’s leftovers.
6. **Secrets stay out of git** — env / CI secrets only.

README still shows `expect()` in a few examples. That is outdated. Follow this file and `.cursor/rules/automated-tests.mdc`.

```python
# ❌ BAD — Playwright expect
from playwright.sync_api import expect
expect(cart_page.cart_items).to_have_count(1)

# ✅ GOOD
assert cart_page.get_item_count() == 1
assert "Sauce Labs Backpack" in cart_page.get_item_names()

# ❌ BAD — assert in the page object
def login_standard_user(self):
    self.login_button.click()
    assert self.page.locator("[data-test='title']").text_content() == "Products"

# ✅ GOOD — page acts; test asserts
def login_standard_user(self) -> InventoryPage:
    self.username.fill("standard_user")
    self.password.fill("secret_sauce")
    self.login_button.click()
    return InventoryPage(self.page)
```

For visibility/text on a locator returned by a getter:

```python
error = login_page.get_error_message()
assert error.is_visible()
assert "locked out" in (error.text_content() or "")
```

---

## Adding a UI test

1. Put it in `tests/ui/test_<area>.py`.
2. Request the **shallowest** fixture that puts you where the scenario starts (`login_page`, `inventory_page`, `cart_with`, `checkout_started`, …).
3. Drive the UI through page objects. Add locators/actions on the page class if missing; do not dump raw `page.locator(...)` in new tests unless you are teaching a locator lesson.
4. Assert with pytest `assert` on getters (`get_title().text_content()`, `get_item_names()`, `count()`, `is_visible()`, …).
5. Prefer `[data-test="..."]` locators, matching existing pages.
6. Mark with `@pytest.mark.ui` if you add a marker (markers are strict: only `ui` and `api` in `pytest.ini`).

`cart_with` example:

```python
def test_remove_one_item_from_cart(cart_with):
    cart_page = cart_with("sauce-labs-backpack", "sauce-labs-bike-light")
    cart_page.remove_item("sauce-labs-backpack")
    assert cart_page.get_item_count() == 1
    assert cart_page.get_item_names() == ["Sauce Labs Bike Light"]
```

---

## Adding an API test

1. Put it in `tests/api/test_<resource>.py`. Set `pytestmark = pytest.mark.api` on the module when the file is API-only.
2. Use `booking_client` for authenticated calls; construct `BookingAPIClient(api_session)` with no token for 403/unauth cases.
3. Use `make_booking()` / `created_booking` instead of hardcoded names.
4. Add a method on `BookingAPIClient` for a new endpoint — return the raw `Response`.
5. Assert `status_code` and body. Optional: wrap the call with `attach_exchange()` from `support.allure_hooks` so Allure stores request/response.

```python
def test_put_replaces_the_whole_booking(booking_client, created_booking):
    booking_id, _ = created_booking
    new_payload = make_booking(firstname="Big", lastname="Boss", totalprice=222)
    r = booking_client.update_booking(booking_id, new_payload)
    assert r.status_code == 200
    assert booking_client.get_booking(booking_id).json() == new_payload
```

restful-booker is a **shared public API**: it can sleep when idle and reset data. Prefer unique payloads and the cleanup fixture; do not assume leftover IDs from a previous run.

---

## Commands

```bash
pip install -r requirements.txt
playwright install chromium

python -m pytest                      # full suite
python -m pytest --headed             # watch the browser
python -m pytest tests/api            # API only
python -m pytest --ignore=tests/api   # UI only (matches CI ui-tests job)
python -m pytest -k checkout
python -m pytest --setup-show         # fixture setup/teardown
```

Outputs: `report.html` always; screenshots, video, traces on failure under `test-results/`; Allure raw results in `allure-results/`. Open traces at https://trace.playwright.dev.

CI: `.github/workflows/tests.yml` — parallel `ui-tests` and `api-tests`, then Allure; Pages publish **only from `master`**.

---

## Do not

- Put `assert` or `expect()` in page objects or `BookingAPIClient`.
- Add `time.sleep()`; use Playwright auto-wait (`click`, `fill`, `is_visible`, `wait_for_url` as in `auth_state`).
- Share mutable booking IDs or cart state across tests.
- Skip or soften failing asserts to go green.
- Change `pytest.ini` `addopts` unless the task is about reporting/CI.
- Treat `tests/ui/test_login.py` / `test_first.py` / `test_internet.py` / `test_demoqa.py` as the pattern for **new** product tests — several are early locator exercises. Prefer `test_inventory.py`, `test_cart.py`, `test_checkout.py`, and `tests/api/test_*.py`.
