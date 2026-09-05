# LeadFlow Bot — demonstration notes

Personal portfolio demonstration. Not client work.

## Start the bot

1. Create a virtual environment and install `.[dev]` (see README).
2. Copy `.env.example` to `.env`.
3. Create a bot with BotFather and paste the token.
4. Put your Telegram user ID in `ADMIN_IDS`.
5. Run:

```bash
alembic upgrade head
python -m app.seed
python -m app.main
```

Open the bot in Telegram and send `/start`.

## Create a token with BotFather

1. Open Telegram and search for `@BotFather`.
2. Send `/newbot`.
3. Choose a display name such as `LeadFlow Demo`.
4. Choose a username ending in `bot`.
5. Copy the token into `BOT_TOKEN`.
6. Optional: `/setdescription` and `/setabouttext` explaining that this is a portfolio demo.

## Configure administrator IDs

1. Message `@userinfobot` or `@getidsbot` and copy your numeric user ID.
2. Set `ADMIN_IDS=123456789` (comma-separated for more than one).
3. Restart the process.
4. Confirm `/admin` works for you and is denied from a second account.

## Recommended screenshot sequence

1. `/start` welcome plus the three-button menu
2. Submit a request — category keyboard
3. Confirmation summary with Confirm / Edit / Cancel
4. Success message showing `LF-…`
5. Administrator notification of the new lead
6. `/admin` counts
7. Lead detail with status buttons
8. Status changed to In Progress and the customer notice
9. Internal note on a lead
10. My requests on the customer side
11. CSV document received after Export

Keep fictional data in screenshots. Do not show a real phone number or a live token.

## Suggested portfolio captions

- “Telegram lead intake for a small studio — structured brief, admin desk, CSV export.”
- “Personal demo: aiogram 3 + SQLAlchemy 2, with tests and Docker, not client work.”
- “Customer FSM with confirmation, duplicate protection, and admin-only callbacks.”

## Demonstration checklist

- [ ] README labels the repo as a personal demonstration
- [ ] `.env` is not committed
- [ ] Seed data is fictional
- [ ] `/start` explains the bot in one short paragraph
- [ ] Form cannot be submitted without confirmation
- [ ] `/admin` is denied for a non-admin account
- [ ] Status change notifies the customer
- [ ] Export produces a UTF-8 CSV
- [ ] `pytest` is green without a Telegram token
- [ ] Screenshots use the sample studio story, not a real client
