# AskNehru Django Backend

## Backend Structure

The Django backend is now organized by feature app instead of a single large API module.

- `asknehru_django/`: Django project configuration, settings, and root URLs.
- `core/`: shared backend support code such as authentication, admin wiring, shared model exports, migrations, and common serializer/view utilities.
- `auth/`: login API.
- `users/`: user CRUD APIs.
- `medicines/`: medicine APIs, serializers, views, URLs, and models.
- `conversations/`: conversation APIs, serializers, views, URLs, and models.
- `roadmaps/`: roadmap APIs, serializers, views, URLs, and models.
- `yoga/`: yoga APIs, serializers, views, URLs, and models.
- `uploads/`: shared upload endpoints.
- `planning/`: epic/task planning APIs, serializers, views, URLs, and models.

Each feature app keeps its own `models.py`, `serializers.py`, `views.py`, `urls.py`, and `migrations/` package so related code stays together and easier to maintain.

The `core` app keeps the legacy Django app label `api` internally so existing migration history and database relations continue to work without schema churn.
