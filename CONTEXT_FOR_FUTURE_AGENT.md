# Context Document for Email Contact Extraction

## Situation Overview

The user (Meffff) has 4 CSV files containing email data:
- `Inbox.CSV` - 843 sent emails to 452 distinct recipients
- `Inbox2.CSV` - (not yet analyzed)
- `Inbox3.CSV` - (not yet analyzed)
- `Inbox4.CSV` - (not yet analyzed)

The goal is to identify everyone the user talked to while in New York, which is spread across these CSVs with many "fluff" emails mixed in.

## Current Progress

We are starting with `Inbox.CSV`, which contains **sent emails only** (emails the user sent to others).

The user wants to go through contacts **10 at a time** to manually evaluate which ones are real, valuable contacts worth adding to a CRM.

## The CRM Format

We have a file called `contacts_crm.csv` with these columns:
- First Name
- Last Name
- Email Address
- Company
- Key Notes
- Location/Office
- Primary Topic

**Important: It's okay if some fields are missing for a given contact.**

## Your Task

Work through the email recipients from `Inbox.CSV` in batches of **10 at a time**:

1. **Present the batch**: Show the user 10 email addresses with a count of how many emails were sent to each
2. **Let the user evaluate**: Ask the user which contacts from the batch are real people worth keeping
3. **For approved contacts only**: Use YOUR OWN INTELLIGENCE (not Python scripts) to:
   - Read through the actual email content in `Inbox.CSV`
   - Extract the person's first name, last name, company, location, primary topic, and key notes
   - Manually analyze the email bodies and subjects to understand who this person is
4. **Add to CRM**: Append only the approved contacts to `contacts_crm.csv`
5. **Move to next batch**: Repeat with the next 10 recipients

## Critical Instructions

### DO NOT:
- Run automated Python scripts to extract contact data
- Assume all contacts are worth keeping
- Fill in data for contacts the user hasn't approved
- Make up information that isn't in the emails
- Process all 452 contacts at once

### DO:
- Use your own intelligence to read and analyze emails
- Present 10 contacts at a time for user evaluation
- Only extract data for approved contacts
- Read the actual email content to understand context
- It's fine if some CRM fields are empty for a contact
- Ask the user which contacts from each batch are real people

## Data Limitations

The CSV exports **do not include date/timestamp metadata**. You cannot provide:
- First contact date
- Last contact date
- Chronological ordering

What you CAN extract:
- Names (from email fields or body)
- Email addresses
- Company (from domain or email content)
- Location (if mentioned in emails)
- Topics/context (from subject lines and body)
- Notes about the relationship

## The User's Judgment

The user has better judgment than any automated script about which contacts are valuable. Some emails may be:
- Bulk cold outreach that failed
- Generic info@ addresses
- Internal Duke system addresses
- Research project mass emails
- Not actual professional contacts

Only add contacts to the CRM that the user explicitly approves.

## Starting Point

Begin by showing the user the first 10 email recipients from `Inbox.CSV` sorted by email count (most emails first). These should be the top 10 people the user sent the most emails to.

The top recipients include people like:
- gabby.sullivan@qxo.com (16 emails)
- kbailas@updata.com (14 emails)
- alewinter@tzpgroup.com (12 emails)
- hkirby@battery.com (12 emails)
- And so on...

Good luck! Remember: manual evaluation, 10 at a time, user approval required, then manually extract the data using your intelligence.
