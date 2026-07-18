---
description: How to start a new coding session with full project context
---

## Steps

1. Read the shared agent context to understand the project:
   - Read `.agent/project_description.md` for the full project specification
   - Read the latest 2-3 entries in `.agent/context/JOURNAL.md` to see what was done recently
   - Read `.agent/context/REGISTRY.md` to see what modules exist and their status

2. Check architecture decisions if working on a relevant area:
   - Browse `.agent/architecture/` for any ADRs related to your task

3. When finishing your session, you MUST:
   - Append a new entry at the TOP of `.agent/context/JOURNAL.md` using the template
   - Update `.agent/context/REGISTRY.md` if you created or modified any modules
