# Implementation Plan for Pomodoro Web App

This plan breaks the project into incremental phases with concrete tasks, time estimates (rough), acceptance criteria, and testing notes. Use this as a roadmap for development and tracking progress.

---

## Phase 1 — Scaffold & App Factory (1-3 hours)

Goal
- Create a working Flask scaffold and static file structure so the app can be run and iterated on.

Tasks
- Create `app.py` with `create_app(config)` factory
- Add `config.py` with development defaults
- Create `requirements.txt` (Flask, SQLAlchemy, pytest)
- Create `templates/index.html` (placeholder UI)
- Create `static/js/` and `static/css/` directories and an empty `timer-core.js` and `style.css`

Acceptance criteria
- Running `flask run` (or `python -m flask run`) serves the index page.
- Project structure is present and imports do not error.

Testing
- Manual smoke test: load page in browser.

Estimated time: 1-3 hours

---

## Phase 2 — Timer Core & UI Integration (4-8 hours)

Goal
- Implement accurate timer logic and a working UI that can start/pause/reset and display remaining time. Backend API calls can be mocked.

Tasks
- Implement `static/js/timer-core.js` (pure functions for start/computeRemaining/pause/reset, visibility handling)
- Implement `static/js/timer-ui.js` (DOM bindings, controls)
- Implement basic circular timer UI in `index.html` and styles in `style.css`
- Mock `/api/session/start` and `/api/session/complete` endpoints on client (or implement basic test endpoints that log)

Acceptance criteria
- Timer Start/Pause/Reset works and UI updates smoothly.
- Timer recovers correctly after tab visibility changes and system sleep.

Testing
- Unit tests for `timer-core.js` functions (Jest) — basic cases for drift correction
- Manual test in browser

Estimated time: 4-8 hours

---

## Phase 3 — Persistence & API (4-6 hours)

Goal
- Implement backend persistence and real API endpoints, and connect the frontend to use them.

Tasks
- Create `models.py` with SQLAlchemy `Session` model
- Create `services.py` implementing `start_session` and `complete_session` logic
- Implement API endpoints (routes) for start/complete/cancel and stats
- Wire frontend to call real endpoints, handle responses and errors
- Add pytest tests for service functions and API (in-memory SQLite)

Acceptance criteria
- Starting/completing a session persists the record in the DB
- API tests pass in CI-local runs

Estimated time: 4-6 hours

---

## Phase 4 — History/Stats & Settings (3-6 hours)

Goal
- Add UI and API for session history, aggregated stats, and user settings for durations.

Tasks
- Implement `GET /api/sessions` and `GET /api/stats`
- Frontend: history view and stats panel (simple graphs or numeric summaries)
- Settings UI for custom durations, stored in localStorage and optionally server-side when authenticated

Acceptance criteria
- User can view recent sessions and stats
- User can change default durations and that affects newly started timers

Estimated time: 3-6 hours

---

## Phase 5 — Offline / Multi-tab / Notifications (6-12 hours)

Goal
- Improve UX for real-world use: offline resilience, single-tab leader, and notifications.

Tasks
- Implement offline queue and retry logic (localStorage/IndexedDB)
- Use BroadcastChannel/localStorage to elect a leader tab for timer control
- Add Notification API and sound playback for session transitions

Acceptance criteria
- App continues to function when offline and syncs events after reconnect
- Only one tab is actively controlling the timer, other tabs reflect state
- Notifications fire when session ends (with user permission)

Estimated time: 6-12 hours

---

## Phase 6 — Auth, CI, Deploy (6-12 hours)

Goal
- Prepare app for multi-user and production deployment.

Tasks
- Add simple auth (username/password or OAuth optional)
- Add CI (GitHub Actions) to run lint and tests
- Dockerfile and sample production config (gunicorn + nginx)
- E2E tests (Playwright) for critical flows

Acceptance criteria
- CI pipeline passes; Docker image builds and runs; tests cover critical flows

Estimated time: 6-12 hours

---

## Testing & QA Plan
- Unit tests: services, timer-core, utility functions
- Integration tests: Flask test client against in-memory DB
- E2E tests: Playwright for start->complete flow

## Deliverables per phase
- Source files added/updated (listed per phase)
- Tests for core logic
- README updates documenting how to run locally and run tests

---

If you want, I can implement Phase 1 now and create the scaffold files (`app.py`, `config.py`, `requirements.txt`, `templates/index.html`, `static/js/timer-core.js`, `static/css/style.css`). Which files should I create first?