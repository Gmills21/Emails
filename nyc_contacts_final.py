#!/usr/bin/env python3
"""
Final NYC contacts analyzer - excludes self-emails and gives clean results.
"""
import csv
import re
from collections import defaultdict

def parse_csv_file(filename):
    """Parse a CSV file and return email records."""
    emails = []
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                emails.append(row)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
    return emails

def is_self_email(email):
    """Check if this is an email from Graham himself."""
    from_name = email.get('From: (Name)', '').lower()
    from_addr = email.get('From: (Address)', '').lower()
    
    # Check for Graham's emails
    if 'graham' in from_name or 'gmills' in from_addr or 'mills' in from_name:
        return True
    
    # Check for Exchange internal format (these are sent emails)
    if 'exchangelabs' in from_name.lower() and 'cn=recipients' in from_name.lower():
        return True
    
    return False

def is_automated_sender(email):
    """Check if sender appears to be automated/marketing."""
    from_name = email.get('From: (Name)', '').lower()
    from_addr = email.get('From: (Address)', '').lower()
    
    # Automated sender patterns
    automated_patterns = [
        'no-reply', 'noreply', 'donotreply', 'do-not-reply',
        'automated', 'notification', 'alert', 'notifications@',
        'newsletter', 'breaking news', 'daily', 'weekly',
        'recruiting@', 'careers@', 'jobs@', 'earlycareers@',
        'support@', 'team@', 'info@', 'contact@',
        'workday', 'myworkday', 'talent.icims', '@myworkday',
        'pymetrics', 'hirevue', 'sparkhire', 'jobvite',
        'mail.beehiiv', 'mg.', '@g.', 'mailer@',
        'unsubscribe', 'microsoft outlook', 'calendar',
        'duke delivered', 'bursar', 'registrar',
        'handshake', 'campus', '-request@', 'listserv',
        'campusgroups', 'housing at', 'student life',
        'econ_dfe', 'globaled@', 'elections',
        'human resources', 'talent acquisition',
        'donotreply@', 'updates@', 'news@'
    ]
    
    # Check patterns
    for pattern in automated_patterns:
        if pattern in from_addr or pattern in from_name:
            return True
    
    return False

def is_likely_personal_conversation(email):
    """Determine if this is likely a personal conversation."""
    body = email.get('Body', '')
    from_name = email.get('From: (Name)', '')
    subject = email.get('Subject', '')
    
    # Must have reasonable content
    if len(body) < 50:
        return False
    
    # Check for personal greeting patterns
    personal_patterns = [
        'hi graham', 'hello graham', 'dear graham',
        'hey graham', 'thanks for', 'thank you for',
        'nice to meet', 'great to meet', 'pleasure to meet',
        'following up', 'follow up', 'checking in',
        'wanted to reach out', 'hope this email finds',
        'hope you', 'best regards', 'best,', 'sincerely,',
        'looking forward', 'excited to', 're:', 'fw:'
    ]
    
    body_lower = body.lower()
    subject_lower = subject.lower()
    
    # Personal greeting check
    for pattern in personal_patterns:
        if pattern in body_lower[:800] or pattern in subject_lower:
            return True
    
    # Has a personal-sounding name
    if from_name:
        name_parts = from_name.split()
        if len(name_parts) >= 2 and len(body) > 200:
            return True
    
    return False

def extract_person_info(email):
    """Extract clean person information."""
    from_name = email.get('From: (Name)', '').strip()
    from_addr = email.get('From: (Address)', '').strip()
    
    # Clean up name
    if not from_name or '/o=' in from_name.lower():
        if from_addr:
            name_part = from_addr.split('@')[0]
            from_name = name_part.replace('.', ' ').replace('_', ' ').title()
        else:
            from_name = "Unknown"
    
    # Get company from email
    company = ""
    if '@' in from_addr:
        domain = from_addr.split('@')[1].lower()
        company = domain.replace('.com', '').replace('.org', '').replace('.edu', '').replace('.co.uk', '')
        company = company.split('.')[0].title()
    
    return from_name, from_addr, company

def contains_nyc_reference(email):
    """Check if email mentions NYC."""
    text = f"{email.get('Subject', '')} {email.get('Body', '')}".lower()
    
    nyc_keywords = [
        'new york', 'nyc', 'manhattan', 'brooklyn',
        'ny ', ' ny,', 'york city', 'queens', 'bronx',
        'wall street', 'midtown', 'downtown manhattan',
        'east village', 'west village', 'upper east',
        'upper west', 'financial district', 'tribeca',
        'soho', 'chelsea'
    ]
    
    for keyword in nyc_keywords:
        if keyword in text:
            return True
    return False

def main():
    print("=" * 80)
    print("NYC CONTACTS FINDER - Finding Real People You Talked To")
    print("=" * 80)
    
    all_emails = []
    files = ['Inbox.CSV', 'Inbox2.CSV', 'Inbox3.CSV', 'Inbox4.CSV']
    
    # Load all emails
    for filename in files:
        print(f"Loading {filename}...", end='')
        emails = parse_csv_file(filename)
        all_emails.extend([(filename, email) for email in emails])
        print(f" {len(emails)} emails")
    
    print(f"\nTotal emails loaded: {len(all_emails)}")
    
    # Filter step by step
    print("\n" + "=" * 80)
    print("FILTERING...")
    print("=" * 80)
    
    # Remove self emails
    not_self = [(f, e) for f, e in all_emails if not is_self_email(e)]
    print(f"Step 1: Removed self emails: {len(not_self)} remaining")
    
    # Remove automated
    not_automated = [(f, e) for f, e in not_self if not is_automated_sender(e)]
    print(f"Step 2: Removed automated: {len(not_automated)} remaining")
    
    # Keep personal conversations
    personal = [(f, e) for f, e in not_automated if is_likely_personal_conversation(e)]
    print(f"Step 3: Kept personal conversations: {len(personal)} remaining")
    
    # NYC-related only
    nyc_convos = [(f, e) for f, e in personal if contains_nyc_reference(e)]
    print(f"Step 4: NYC-related only: {len(nyc_convos)} remaining")
    
    # Group by person
    print("\n" + "=" * 80)
    print("GROUPING BY PERSON...")
    print("=" * 80)
    
    people = defaultdict(list)
    for filename, email in nyc_convos:
        person_name, person_email, company = extract_person_info(email)
        # Use email as primary key to avoid duplicates
        key = person_email.lower()
        people[key].append({
            'name': person_name,
            'email': person_email,
            'company': company,
            'source': filename,
            'email_obj': email
        })
    
    # Sort by number of emails
    sorted_people = sorted(people.items(), key=lambda x: len(x[1]), reverse=True)
    
    print(f"\nFound {len(sorted_people)} unique people\n")
    
    print("=" * 80)
    print("NYC CONTACTS - REAL PEOPLE YOU TALKED TO")
    print("=" * 80)
    print()
    
    # Display results
    output_lines = []
    for i, (email_key, email_list) in enumerate(sorted_people, 1):
        # Get consistent info from first email
        person_name = email_list[0]['name']
        person_email = email_list[0]['email']
        company = email_list[0]['company']
        
        line = f"{i:3d}. {person_name:35s} @ {company:20s} ({len(email_list)} emails)"
        print(line)
        output_lines.append(line)
        
        # Show a sample subject
        sample_subject = email_list[0]['email_obj'].get('Subject', 'No subject')[:70]
        detail = f"     {person_email}\n     Latest: {sample_subject}"
        print(detail)
        output_lines.append(f"     {person_email}")
        
        if len(email_list) > 1:
            subjects = [e['email_obj'].get('Subject', 'No subject')[:60] for e in email_list[:3]]
            for subj in subjects[1:3]:
                print(f"     - {subj}")
        
        print()
    
    # Save results
    print("=" * 80)
    print("SAVING RESULTS...")
    print("=" * 80)
    
    # Save simple contact list
    with open('NYC_CONTACTS.txt', 'w', encoding='utf-8') as f:
        f.write("NYC CONTACTS - PEOPLE YOU TALKED TO WHILE IN NEW YORK\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total: {len(sorted_people)} people\n")
        f.write(f"Total conversations: {len(nyc_convos)} emails\n\n")
        f.write("=" * 80 + "\n\n")
        
        for i, (email_key, email_list) in enumerate(sorted_people, 1):
            person_name = email_list[0]['name']
            person_email = email_list[0]['email']
            company = email_list[0]['company']
            
            f.write(f"{i}. {person_name} @ {company}\n")
            f.write(f"   Email: {person_email}\n")
            f.write(f"   Total emails: {len(email_list)}\n")
            f.write(f"   \n")
            
            # List subjects
            for j, item in enumerate(email_list[:5], 1):
                subject = item['email_obj'].get('Subject', 'No subject')
                f.write(f"   - {subject}\n")
            
            if len(email_list) > 5:
                f.write(f"   ... and {len(email_list) - 5} more\n")
            
            f.write("\n")
    
    print(f"✓ Saved to: NYC_CONTACTS.txt")
    
    # Save full emails to CSV
    with open('nyc_conversations_clean.csv', 'w', newline='', encoding='utf-8') as f:
        if nyc_convos:
            fieldnames = list(nyc_convos[0][1].keys()) + ['Source_File']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for filename, email in nyc_convos:
                row = dict(email)
                row['Source_File'] = filename
                writer.writerow(row)
    
    print(f"✓ Saved full emails to: nyc_conversations_clean.csv")
    
    print("\n" + "=" * 80)
    print("✓ COMPLETE!")
    print("=" * 80)
    print(f"\n📧 Found {len(sorted_people)} people you talked to in NYC")
    print(f"💬 Across {len(nyc_convos)} total conversations")
    print(f"\n📄 Check NYC_CONTACTS.txt for the full list!")

if __name__ == '__main__':
    main()
