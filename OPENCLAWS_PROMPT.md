You are working on the GitHub repository: https://github.com/Jose-Gael-Cruz-Lopez/hackathons

## PROJECT OVERVIEW

This is an automated GitHub repository that tracks hackathons (coding events / build competitions). Users submit hackathons by creating a GitHub Issue with just a link, and an AI-powered GitHub Action automatically extracts the details (host/organizer, hackathon name, location, format, prize, etc.) and adds them to the README table.

## REPOSITORY STRUCTURE

```
hackathons/
├── README.md                              # Main page with the Hackathons table
├── ARCHIVE.md                             # Closed/past hackathons
├── CONTRIBUTING.md                        # Contribution guide
├── web/                                   # Next.js site that renders the README as a browsable board
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── link_only.yaml                 # PRIMARY: Just paste a URL, AI extracts everything
    │   ├── quick_add.yaml                 # FALLBACK: a few fields (link, host, name, format)
    │   ├── new_opportunity.yaml           # FULL: All fields manual
    │   ├── edit_opportunity.yaml          # Edit existing listing (not supported — close + re-add)
    │   ├── close_opportunity.yaml         # Mark listing as closed
    │   └── other.yaml                     # General feedback
    ├── scripts/
    │   ├── auto_extract.py                # Fetches URL + uses OpenAI to extract details
    │   ├── contribution_approved.py       # Processes manual submissions
    │   ├── update_readmes.py              # Generates the README table from listings.json
    │   ├── closing_soon.py                # Flags hackathons closing within 7 days
    │   ├── weekly_digest.py               # Generates a weekly digest issue
    │   ├── util.py                        # Shared utilities (formatting, JSON I/O, etc.)
    │   ├── listings.json                  # THE DATA: all hackathons stored here
    │   └── requirements.txt               # Python dependencies
    └── workflows/
        ├── auto_extract.yml               # Triggered when 'approved' label added to issue
        ├── contribution_approved.yml      # Processes non-AI submissions
        ├── closing_soon.yml               # Daily — updates closing-soon badges
        ├── weekly_digest.yml              # Weekly — posts a digest issue
        └── update_readmes.yml             # Auto-updates README when listings.json changes
```

## HOW THE AUTOMATION WORKS

1. User creates an issue using the "Add Hackathon (Just Paste Link)" template — they only paste a URL
2. A maintainer reviews and adds the `approved` label
3. The `auto_extract.yml` workflow triggers:
   - Fetches the webpage using `requests` + `BeautifulSoup`
   - Sends page content to OpenAI GPT-4o-mini to extract structured data
   - AI returns JSON with: company_name (host), title (hackathon name), locations, format, prize, is_hackathon
   - Script adds the new listing to `listings.json`
   - Runs `update_readmes.py` to regenerate the README table
   - Commits and pushes to main
   - Comments on the issue with extracted details, then closes the issue

## THE README TABLE

The README has a single section with a table between HTML comment markers:

**Hackathons** (`<!-- HACKATHONS_TABLE_START -->` / `<!-- HACKATHONS_TABLE_END -->`)
- Columns: Status | Host | Hackathon | Format | Location | Prize | Application | Date Posted
- `format` is one of: In-Person, Virtual, Hybrid

## IMPORTANT CONSTRAINTS

- The Register button MUST be blue using shields.io: `https://img.shields.io/badge/Register-blue?style=for-the-badge`
- The OpenAI API key is stored as a GitHub secret called `OPENAI_API_KEY`
- The AI model used is `gpt-4o-mini`
- All timestamps are in Pacific Standard Time (PST)
- The listings.json is the single source of truth — the README is auto-generated from it
- Never commit broken README tables
- Each listing in listings.json MUST have these required fields: id, company_name, title, url, locations, format, prize, active, is_visible, date_posted, date_updated, source

## WHAT SUCCESS LOOKS LIKE

When done:
1. Pasting a link and adding the `approved` label should correctly extract ALL details
2. ALL columns should be properly aligned — no data in wrong columns
3. The Register button should always be blue and in the Application column
4. No duplicate entries
5. No broken markdown tables
6. The workflow should handle errors gracefully and never commit bad data
