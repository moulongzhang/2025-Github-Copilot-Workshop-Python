# Pomodoro Web App - Architecture

This document summarizes the proposed architecture for the Pomodoro timer web application (Flask + HTML/CSS/JS). It consolidates the decisions and recommendations made during the design discussion, and includes implementation notes and guidance for testing and future improvements.

## Goals
- Responsive, user-friendly Pomodoro timer with accurate client-side timing
- Lightweight backend to record sessions, provide history and statistics
- Testable, maintainable, and easy to extend

## High-level architecture

- Frontend (browser):
  - Responsible for the real-time timer UI and user interaction.
  - Implemented with HTML/CSS and modular JavaScript.
  - Uses high-resolution timing APIs (performance.now, requestAnimationFrame) and localStorage for recovery.
  - Communicates with the backend via a small REST API to record session start/complete/cancel.

- Backend (Flask):
  - Serves the static frontend and provides API endpoints for sessions and stats.
  - Holds minimal business logic; core logic placed in a `services` layer for testability.
  - Uses SQLite (development) with SQLAlchemy and an easy path to PostgreSQL for production.

- Persistence:
  - Sessions persisted in a `sessions` table (id, user_id, type, start_ts, end_ts, duration, completed, created_at).

## Components and files (suggested)

- app.py
  - Application factory `create_app(config)`
  - Registers blueprints, error handlers, logging

- models.py
  - SQLAlchemy models (Session, User optional)
  - DB initialization helpers

- services.py
  - `SessionService` with pure methods: `start_session`, `complete_session`, `cancel_session`, `get_stats`
  - Uses dependency injection for DB session and time provider

- api.py (or routes.py)
  - Flask routes /blueprints implementing the HTTP layer
  - Validate requests (using pydantic or marshmallow) then call services

- templates/
  - index.html (main UI)

- static/
  - css/style.css
  - js/timer-core.js (pure timer logic, testable)
  - js/timer-ui.js (DOM binding, uses timer-core)
  - img/

- tests/
  - pytest tests for services, routes (Flask test client), and JS unit tests (optional)

- requirements.txt / pyproject.toml

## API Design (minimal)

- POST /api/session/start
  - body: {type: "pomodoro"|"short_break"|"long_break", planned_duration: number}
  - response: {session_id}

- POST /api/session/complete
  - body: {session_id, actual_duration}
  - response: 200

- POST /api/session/cancel
  - body: {session_id}

- GET /api/stats?range=7d
  - response: aggregated statistics (pomodoros completed, focus time, etc.)

- GET /api/sessions?limit=50
  - response: recent session list

Security: CSRF protection for cookie auth; validate inputs strictly; rate limits optional.

## Frontend timer design

- Keep core timing logic in `timer-core.js` as pure functions:
  - `startTimer(plannedMs, nowProvider)` returns a timer state and helpers
  - `computeRemaining(state, now)` computes remaining ms using monotonic timestamps
  - `adjustForVisibility(state, now)` compensates for visibilitychange/suspend

- UI module (`timer-ui.js`) should be thin: render DOM, bind buttons, call core functions.

- Persistence & multi-tab:
  - Persist session state in localStorage and/or BroadcastChannel for leader election across tabs.

- Offline handling:
  - Queue server calls (start/complete) in IndexedDB or localStorage and sync when online.

## Testing strategy

- Backend
  - Use pytest and a create_app factory.
  - Use SQLAlchemy with an in-memory SQLite database for unit tests.
  - Provide fixtures: `app`, `client`, `db_session`, `time_provider`.
  - Test services in isolation by injecting a fake time provider and a transactional DB session.

- Frontend
  - Split timer-core.js so it can be tested with Jest (Node) or run in browser using karma.
  - Use jsdom for DOM-related tests (optional); prefer testing core logic in isolation.

- Integration/E2E
  - Optional Playwright tests for critical flows: start -> complete, offline -> sync, multi-tab.

## Testability-focused design decisions

- Application factory pattern to make the Flask app configurable for tests
- Services layer to keep business logic independent from HTTP
- Dependency injection for time provider, RNG, DB session, and external notifiers
- Pure timer-core module for easy JS unit tests
- Use parameterized queries / ORM to simplify DB mocking
- Provide fixtures (pytest) to create and tear down test DB per test

## Development & deployment notes

- Use a virtual environment and pin dependencies in `requirements.txt`.
- For production: run behind gunicorn with recommended worker count; serve static files via nginx.
- Optional Dockerfile for consistent deploys.

## Next steps (recommended immediate tasks)

1. Create project scaffold: `create_app`, `models.py`, `services.py`, basic `index.html`, `timer-core.js`.
2. Add pytest fixtures and one or two unit tests for `SessionService` and timer-core functions.
3. Implement client Start/Complete flow and connect to the backend API.

---

This `architecture.md` is a living document: we can extend it with sequence diagrams, DB schema DDL, or wireframes as we implement the scaffold. If you want, I can now create the scaffold files (`app.py`, `models.py`, `services.py`, templates and static JS/CSS) and a minimal `requirements.txt`.