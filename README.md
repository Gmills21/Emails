# Emails

Email analysis tools for filtering NYC contacts from inbox exports.

## NYC Contact Finder

Tools to identify real conversations with people during New York trips.

### Files

- `NYC_CONTACTS.txt` - **Main output**: List of 109 people you talked to in NYC, sorted by conversation volume
- `nyc_conversations_clean.csv` - Full email details (463 conversations)
- `nyc_contacts_final.py` - Python script to generate the contact list

### Key Contacts from NYC

Top people you had conversations with:
- **Gabby Sullivan** @ QXO (12 emails) - Analyst position
- **Danielle Jones** @ IFSA-Butler (15 emails) - Study abroad
- **Devan Knoetze** @ Hudson Advisors (8 emails) - Interview follow-ups
- **Joseph Reiff** @ Barclays (8 emails) - Referral from Alexi Braun
- **Ben Matz** @ Bain (8 emails) - Interview process
- **Lavonne Hoang** @ HSBC (7 emails) - Interview conversations
- **Kristin Johnson** @ University of Sydney (7 emails) - Study abroad program
- **Jordan Bernstein** @ Battery (5 emails) - VC interest
- And 101+ more professional contacts

### Data Source

The analysis scans 4 CSV files containing ~225K emails total:
- `Inbox.CSV` - 46,051 emails
- `Inbox2.CSV` - 99,378 emails
- `Inbox3.CSV` - 69,518 emails
- `Inbox4.CSV` - 10,406 emails

### How to Use

Run the NYC contact finder:
```bash
python3 nyc_contacts_final.py
```

This will:
1. Filter out automated emails (newsletters, notifications, etc.)
2. Find personal conversations mentioning NYC
3. Generate `NYC_CONTACTS.txt` with all contacts sorted by email volume
4. Export full email details to `nyc_conversations_clean.csv`

### Filter Logic

The script:
- Removes self-sent emails
- Filters out automated/marketing emails
- Identifies personal conversations (greetings, follow-ups, etc.)
- Searches for NYC references (New York, Manhattan, Brooklyn, etc.)
- Groups by unique sender email addresses
- Sorts by conversation volume

---

**Result**: 109 unique people | 463 real conversations | NYC-related only
