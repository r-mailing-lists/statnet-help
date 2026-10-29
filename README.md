# statnet-help

Help with statnet, the R packages for network analysis

Automated mbox archive. Updated daily via GitHub Actions.

## Structure

- `raw/` - Yearly .mbox files downloaded from [https://mailman23.u.washington.edu/pipermail/statnet_help/](https://mailman23.u.washington.edu/pipermail/statnet_help/), which keeps 2022 on. The years 2006 to 2021 are the list's own yearly files from its earlier address, mailman13.u.washington.edu, as the [Wayback Machine](https://web.archive.org/web/2021/https://mailman13.u.washington.edu/pipermail/statnet_help/) saved them: 2018 runs to 12 June and 2021 to 19 October, the days they were saved. Rebuilds of that archive wrote their own day into the Date line of most messages up to 2023; `tools/fix-rebuilt-dates.py` put back each message's date from its envelope line, once, and escaped the few lines of text that start with "From ".
- `processed/` - Structured JSON output from rmail-parser
- `sources/` - Where present, each message's page at the source and the characters that page restores, one JSON file per period
- `attachments/` - Text Mailman scrubbed out of messages, fetched once from the source and put back by rmail-parser, one gzip-compressed JSON file per period
- `meta.json` - List statistics

## Viewer

Browse these archives at [r-mailing-lists.thecoatlessprofessor.com](https://r-mailing-lists.thecoatlessprofessor.com/lists/statnet-help/)
