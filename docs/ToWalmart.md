# To Sync To Walmart Laptop

## Git Rebase vs Merge

Use merge. Rebase is a niche optimization with a hidden trap: old SHAs become dangling references. Any Jira comment, CI link, Slack message, or agent log that cited one of those SHAs is now a broken pointer.

Rebase in theory is nice for minimizing annoying merge commits. But those merges actually happened, and your earlier commits were written onto different file states than what rebase implies.

