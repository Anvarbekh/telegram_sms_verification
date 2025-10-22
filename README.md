# Telegram Gateway SMS Verification

FastAPI service that uses Telegram Gateway API to send verification codes and verify them.

Setup:

1. Copy `env.dev.example` to `env.dev` and fill values
2. Start with Docker Compose: `docker-compose up --build`.
3. Create DB tables (app will auto-create on startup).

Local testing with ngrok (for webhook):
1. `ngrok http 8000`
2. Set `WEBHOOK_HOST` in `env.dev` to the ngrok URL (e.g. `https://abcd1234.ngrok.io`) so Telegram Gateway can call the webhook URL.

Endpoints:
- `POST /api/v1/verification/start` — start verification
- `POST /api/v1/verification/verify` — verify code
- `POST /api/v1/webhook/report` — (optional) webhook for delivery reports


See `app/` for implementation details.

Environment (`env.dev`) example (copy `env.dev.example`):

```
TELEGRAM_API_TOKEN=replace_me
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/verification_db
WEBHOOK_HOST=http://localhost:8000
CALLBACK_PATH=/api/v1/webhook/report
CALLBACK_URL=${WEBHOOK_HOST}${CALLBACK_PATH}
SERVICE_PORT=8000
CODE_TTL_SECONDS=60
```

Manual steps you must perform:

- Create and fund a Telegram Gateway account and obtain `TELEGRAM_API_TOKEN`.
- Copy `env.dev.example` to `env.dev` and populate values.
- Run `docker-compose up --build` to start Postgres and the app.
- If you plan to use delivery webhooks, expose `WEBHOOK_HOST` publicly (ngrok or deploy behind TLS) and set `CALLBACK_URL` accordingly.

Testing:

- Start app: `docker-compose up --build`.
- Call `POST /api/v1/verification/start` with JSON `{ "phone_number": "+123..." }`.
- Check responses and your Telegram for a verification message.
- Call `POST /api/v1/verification/verify` with JSON `{ "phone_number": "+123...", "code": "XXXXXX" }`.
