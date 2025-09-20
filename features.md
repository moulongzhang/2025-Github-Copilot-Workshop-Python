# Features for Pomodoro Web App

This file lists the features to implement for the Pomodoro web application. Features are grouped into MVP (must-have), Near-term (should-have), and Optional (nice-to-have). Each feature includes a short description, acceptance criteria, priority, and primary components involved.

---

## MVP (Must-have)

1. Core Timer UI
   - Description: A responsive, accessible UI that shows a circular/linear countdown and Start/Pause/Reset controls.
   - Acceptance criteria:
     - User can start a pomodoro, pause/resume, and reset.
     - Remaining time updates smoothly.
   - Priority: High
   - Components: `templates/index.html`, `static/js/timer-ui.js`, `static/css/style.css`

2. Accurate Client-side Timer Logic (timer-core.js)
   - Description: High-resolution timing and drift compensation logic.
   - Acceptance criteria:
     - Uses performance.now() when available.
     - Compensates for tab visibility changes and system sleep.
     - Exposes pure functions that can be unit tested.
   - Priority: High
   - Components: `static/js/timer-core.js` (pure functions), tests (Jest)

3. Session Start / Complete API
   - Description: Minimal REST API to record a session start and completion.
   - Acceptance criteria:
     - POST `/api/session/start` returns session_id.
     - POST `/api/session/complete` records completion and duration.
   - Priority: High
   - Components: `api.py`/`routes.py`, `services.py`, `models.py`

4. Persist Sessions (SQLite)
   - Description: Save session records to SQLite via SQLAlchemy.
   - Acceptance criteria:
     - Sessions saved with start_ts, end_ts, duration, type, completed flag.
     - In-memory DB support for tests.
   - Priority: High
   - Components: `models.py`, DB config, `tests` fixtures

5. Application Factory and DI
   - Description: `create_app(config)` factory to allow injecting test dependencies (time provider, DB URI).
   - Acceptance criteria:
     - Tests can create app with in-memory DB and mocked time provider.
   - Priority: High
   - Components: `app.py`, `config.py`, `tests/conftest.py`

6. Minimal Frontend-Backend Integration
   - Description: Timer UI starts a session (POST start) and completes session (POST complete).
   - Acceptance criteria:
     - Starting and completing a session results in DB records.
   - Priority: High
   - Components: `timer-ui.js`, api routes, `services.py`

---

## Near-term (Should-have)

7. Session History UI
   - Description: Show recent sessions and status (completed/cancelled) with timestamps.
   - Acceptance criteria:
     - Endpoint GET `/api/sessions` returns recent sessions.
     - Frontend displays paginated list.
   - Priority: Medium
   - Components: `api.py`, `templates/history.html`, `timer-ui.js`

8. Statistics API & UI
   - Description: Daily/weekly stats and totals.
   - Acceptance criteria:
     - GET `/api/stats` returns aggregated metrics (pomodoros completed, focus minutes).
     - Frontend renders graphs or simple numeric summaries.
   - Priority: Medium
   - Components: `services.py`, `api.py`, frontend charts (Chart.js optional)

9. Custom Durations & Settings
   - Description: Allow customizing pomodoro/short/long break durations and persist preferences.
   - Acceptance criteria:
     - User can change durations in UI; preferences saved to localStorage (or DB when auth exists).
   - Priority: Medium
   - Components: `timer-ui.js`, localStorage, optional User model

10. Offline queueing & retry
    - Description: Queue start/complete requests when offline and sync when back online.
    - Acceptance criteria:
      - If network is down, operations are stored locally and sent when online.
    - Priority: Medium
    - Components: `timer-ui.js`, background sync logic, optional IndexedDB

11. Multi-tab coordination
    - Description: Prevent multiple tabs from running independent timers; elect leader tab.
    - Acceptance criteria:
      - Only one tab acts as primary timer; other tabs show synced state.
    - Priority: Medium
    - Components: `timer-ui.js`, BroadcastChannel/localStorage lock

12. Notifications & Sound
    - Description: Desktop notifications and sound on session end; permission handling.
    - Acceptance criteria:
      - Browser asks permission; notifications and sound fire on transitions.
    - Priority: Medium
    - Components: `timer-ui.js`, Notification API, static/sound files

---

## Optional / Advanced (Nice-to-have)

13. Authentication / Multi-user
    - Description: Optional user accounts to keep persistent history across devices.
    - Acceptance criteria:
      - Login/logout, sessions associated with user_id, protected API.
    - Priority: Low
    - Components: `auth.py`, `models.py`, login templates

14. Export / Import sessions
    - Description: CSV export of sessions or JSON backup.
    - Acceptance criteria:
      - User can download CSV of sessions for selected range.
    - Priority: Low
    - Components: `api.py` export endpoint, frontend UI

15. E2E Tests (Playwright)
    - Description: End-to-end tests covering critical flows.
    - Acceptance criteria:
      - Playwright script runs start -> complete flow and verifies DB state.
    - Priority: Low
    - Components: `tests/e2e` suite

16. Docker + Production config
    - Description: Dockerfile, gunicorn config, nginx reverse proxy sample.
    - Acceptance criteria:
      - App can be run via Docker and served with gunicorn; static files served through nginx recommended in prod.
    - Priority: Low

---

## Acceptance criteria and test mapping

- Unit tests:
  - `services.SessionService.start_session` and `complete_session` with mocked time provider and DB session
  - `timer-core.js` functions for remaining time computation and drift correction

- Integration tests:
  - Flask test client for API endpoints using in-memory DB

- E2E tests (optional):
  - Start, complete, and verify UI and DB state

---

## Next steps
1. Create project scaffold (app factory, DB models, services, templates, static JS/CSS)
2. Implement `timer-core.js` and unit tests (Jest)
3. Implement API endpoints and backend unit/integration tests (pytest)
4. Connect frontend to backend and implement history/stats UI

If you want, I can now generate the scaffold files for the MVP (app.py, models.py, services.py, templates/index.html, static/js/timer-core.js, static/js/timer-ui.js, static/css/style.css, requirements.txt) and a minimal pytest setup. Which files do you want me to create first?