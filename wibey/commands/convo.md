---
description: Park the current conversation with a visible title for Mac workspace/Mission Control switching
allowed-tools: Bash
---

Review the conversation history and choose a terse, descriptive title (5-10 words max) that captures the main topic. Do not ask the user — decide yourself.

Then run:
```bash
python3 -c "print('\n' * 30)" && date "+%Y-%m-%d %H:%M %Z"
```

Then respond with ONLY the title as an `# **H1 bold**` markdown heading. No other text.
