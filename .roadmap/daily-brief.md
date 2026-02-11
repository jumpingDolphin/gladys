# Daily Brief

> Gladys sends a morning summary via Telegram without being asked.

## Content

- **Today's tasks** — open Todoist tasks, priorities, deadlines
- **Yesterday recap** — completed tasks, conversation summary
- **Swiss news** — biggest headlines focused on Switzerland (SRF/NZZ or similar RSS source)

## Trigger

Systemd timer calling the OpenClaw gateway API at a configured time (e.g., 07:00 CET).

## Steps

1. Create a systemd timer that triggers the gateway at the scheduled time.
2. Configure the agent prompt/skill to gather: Todoist tasks, yesterday's memory, Swiss news.
3. Format as a concise Telegram message.
4. Choose news source: SRF RSS, NZZ RSS, or a news API.

## Open Questions

| # | Question | Options |
|---|----------|---------|
| 1 | Swiss news source | SRF RSS vs. NZZ RSS vs. news API |
| 2 | Timing | Fixed schedule (07:00 CET) vs. configurable vs. on-demand |

## Validation

- [ ] Daily brief arrives in Telegram at the configured time.
- [ ] Includes today's tasks from Todoist.
- [ ] Includes yesterday's summary from memory.
- [ ] Includes relevant Swiss news headlines.
- [ ] Works reliably for 7 consecutive days.
