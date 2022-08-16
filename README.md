# Create GitHub Issue for Leetcode Daily

[![Actions Status](https://github.com/jeremypruitt/gha-github-issue-for-leetcode-daily/workflows/Lint/badge.svg)](https://github.com/jeremypruitt/gha-github-issue-for-leetcode-daily/actions)
[![Actions Status](https://github.com/jeremypruitt/gha-github-issue-for-leetcode-daily/workflows/Integration%20Test/badge.svg)](https://github.com/jeremypruitt/gha-github-issue-for-leetcode-daily/actions)

This is a GitHub action that will create a GitHub issue for today's Leetcode daily problem. It's written in python which can be found in the `main.py` file.

> 🏁 To get started, go to the marketplace for this action and click the big green button in the top-right that contains the text "Use latest version" in it.

## Usage

This GitHub action can be configured to run on a schedule and can also be executed manually on-demand.

### Example workflow

```yaml
name: Create GitHub Issue for Leetcode Daily Problem

on:
  workflow_dispatch:
  schedule:
    - cron: "7 0 * * *" # UTC time

jobs:
  create_github_issue_for_leetcode_daily:
    runs-on: ubuntu-latest
    name: Create GH Issue for LC Daily
    permissions:
      issues: write
    steps:
      - name: Checkout the repository
        uses: actions/checkout@v3
      - name: Get daily LC problem and create new GH issue
        uses: jeremypruitt/gha-github-issue-for-leetcode-daily@master
```

## Examples

### Scheduled vs On-Demand

If you only want to run manually on-demand, and do not want it to run every day automatically, just remove the `schedule:` from the `on:` section. This leaves only the `workflow_dispatch` method, which enables the manual on-demand mechanism. Here is an example:

```yaml
on:
  workflow_dispatch:
```
