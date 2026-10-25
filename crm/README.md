# Dream Solutions Tennessee — Client Database (cleaned)

Cleaned, deduplicated client list for the radon business. Source: the
`RADON CLIENT INFORMATION 2022-2026.zip` export (1,334 raw contact records,
work span 2022-06-07 → 2026-10-23).

## Files

| File | What it is |
|---|---|
| `clean_clients.py` | Re-runnable pipeline (see below). The source of truth. |
| `clients_clean.csv` | Clean master — **1,322 unique contacts** (deduped + normalized). |
| `review_flags.csv` | Records needing human review (incomplete names, dead emails, possible dups). |
| `merge_log.csv` | The 12 true-duplicate merges (audit trail). |

## `clients_clean.csv` schema

`Contact ID, Primary name, Other names, Categories, Source roles, Phone primary,
Phone secondary, Phone extra, Email primary, Email secondary, Email extra,
Email status, First work date, Last work date, Distinct invoices, Invoices,
Service address primary, Service address count, Billing address, State,
Contact positions, Additional contexts, Merged IDs, Flags`

- Phones normalized to E.164 (`+1...`). Emails lowercased. Multi-value fields
  (the ` | `-joined ones) split into primary / secondary / extra columns.
- `Merged IDs` lists any original Contact IDs folded into this record.
- `Email status` = worst status across the record's emails:
  `valid` / `invalid` (domain has no mail server) / `risky_no_mx` / `disposable`
  / `invalid_syntax` / `missing`.

## Flag legend (`review_flags.csv`)

- `unnamed` — name never captured ("unidentified contact"), 20 records.
- `name_incomplete` — single-word name (no last name), 75 records.
- `possible_duplicate` — same name appears on 2+ records with different
  addresses; NOT auto-merged (could be the same realtor/investor with multiple
  properties, or genuinely different people).
- `email_invalid` / `email_risky_no_mx` / `email_disposable` — bad email.

## Data model note (important)

This export conflates **people** and **properties**. Many distinct people
(homeowner, seller, buyer, realtor, title agent) can share one service address,
and one person can span many addresses. Do **not** dedupe by address alone —
only "same name + same address" was merged (12 cases). Same-name-different-address
groups are left flagged, not merged.

## Re-run on a fresh export

```bash
python3 clean_clients.py "/path/to/RADON CLIENT INFORMATION <dates>.zip" /path/to/output
```

Requires `dig` (macOS default) for email-domain verification. Accepts a zip or an
already-extracted `ALL CLIENTS.csv`.
