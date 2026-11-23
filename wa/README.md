# wa: the cloud route to the WhatsApp bot

Agents change and read WhatsApp campaigns here, in the cloud. Nobody uses the inbox page in a browser for this (Directive D27).

- Push `wa/requests/<date>-<role>-<what>.json`. The workflow `wa-ops` answers in `wa/results/<same name>.json` within about a minute.
- One action: `{"by": "Paid Media Buyer", "op": "switches"}`
- Several, run in order, stopping at the first failure: `{"by": "Paid Media Buyer", "ops": [{"op": "broadcast.create", "args": {"name": "FV Jind SCO: Saturday video", "template": "fv_jind_video_v2", "language": "en", "audience": "Jind customers", "params": {}}}, {"op": "broadcasts", "args": {"days": 1}}]}`
- The list of actions: start the workflow `wa-ops` by hand with `op` empty, or read `scripts/wa_ops.py` and the bot's `src/ops.mjs`.
- A request file is processed once. To run something again, push a new file with a new name.

Rules
- This repo is public. Never put a phone number or a person's name in a request. A request holding a number is refused.
- Answers hold counts and settings only. For people (leads, chats), use the Control Room People and Funnel tabs or the lead sheets.
- A broadcast created here is HELD until Rishi replies GO with its code on WhatsApp. Do not look for another way to start it.
- Refused on purpose: a higher autopilot budget (Approvals tab), the ad signal switch (`signal.yml`, Rishi's word), deleting templates, lists of numbers.
- If the action you need is missing, do not open the browser: write a line for the SMX chat in strategy/LIVE_STATUS.md and it gets added.
