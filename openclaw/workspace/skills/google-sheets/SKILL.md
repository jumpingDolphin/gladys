---
name: google-sheets
description: Create, read, write, and append data to Google Sheets. Use when the user needs to work with spreadsheet data, create tables, log data, or analyze tabular information.
---

# Google Sheets Manager

Create and manage Google Sheets via API.

## Setup

Uses OAuth credentials from workspace:
- `google_credentials.json` - OAuth client config
- `google_token.json` - Access/refresh tokens

Scripts automatically refresh tokens when expired.

## Available Operations

### 1. Create Spreadsheet

```bash
cd google-sheets/scripts

# Create new spreadsheet
python3 create_sheet.py "Monthly Budget"
```

### 2. Read Data

```bash
cd google-sheets/scripts

# Read entire sheet (default Sheet1)
python3 read_sheet.py SHEET_ID

# Read specific range
python3 read_sheet.py SHEET_ID --range "Sheet1!A1:C10"

# CSV output
python3 read_sheet.py SHEET_ID --format csv > data.csv

# JSON output
python3 read_sheet.py SHEET_ID --format json
```

**Get SHEET_ID:** From the URL: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`

**Range notation:**
- `Sheet1` - Entire sheet
- `Sheet1!A1:C10` - Specific cells
- `Sheet1!A:A` - Entire column A
- `Sheet1!1:1` - Entire row 1

### 3. Write Data

```bash
cd google-sheets/scripts

# Write from JSON array
python3 write_sheet.py SHEET_ID --range "Sheet1!A1" \
  --data '[["Name", "Email"], ["Alice", "alice@example.com"]]'

# Write from CSV file
python3 write_sheet.py SHEET_ID --range "Sheet1!A1" --csv-file data.csv
```

**Note:** This overwrites existing data in the range.

### 4. Append Rows

```bash
cd google-sheets/scripts

# Append single row
python3 append_row.py SHEET_ID --row '["John", "john@example.com", "123"]'

# Append multiple rows
python3 append_row.py SHEET_ID --rows '[["A", "B"], ["C", "D"]]'

# Append from CSV
python3 append_row.py SHEET_ID --csv-file new_data.csv
```

**Note:** Appends to the end of existing data (doesn't overwrite).

## Workflow Patterns

### Create and Populate Spreadsheet

```bash
cd google-sheets/scripts

# Create spreadsheet
python3 create_sheet.py "Team Contacts"
# Note SHEET_ID from output

# Write headers
python3 write_sheet.py SHEET_ID --range "Sheet1!A1" \
  --data '[["Name", "Email", "Phone"]]'

# Append data rows
python3 append_row.py SHEET_ID --row '["Alice", "alice@example.com", "555-0001"]'
python3 append_row.py SHEET_ID --row '["Bob", "bob@example.com", "555-0002"]'
```

### Log Data Daily

```bash
cd google-sheets/scripts

# Append today's entry
python3 append_row.py LOG_SHEET_ID \
  --row "[\"$(date +%Y-%m-%d)\", \"Task completed\", \"2 hours\"]"
```

### Export and Process Data

```bash
cd google-sheets/scripts

# Export to CSV
python3 read_sheet.py SHEET_ID --format csv > /tmp/data.csv

# Process with standard tools
awk -F',' '{print $1, $3}' /tmp/data.csv
```

### Import CSV to New Sheet

```bash
cd google-sheets/scripts

# Create sheet
python3 create_sheet.py "Imported Data"
SHEET_ID="..." # from output

# Import CSV
python3 write_sheet.py $SHEET_ID --range "Sheet1!A1" --csv-file data.csv
```

## Common Tasks

### Create Expense Tracker

```bash
cd google-sheets/scripts

python3 create_sheet.py "Expenses 2026"
SHEET_ID="..."

# Headers
python3 write_sheet.py $SHEET_ID --range "Sheet1!A1" \
  --data '[["Date", "Description", "Amount", "Category"]]'

# Add expense
python3 append_row.py $SHEET_ID \
  --row "[\"$(date +%Y-%m-%d)\", \"Coffee\", \"4.50\", \"Food\"]"
```

### Read and Analyze Data

```bash
cd google-sheets/scripts

# Get all data as JSON
python3 read_sheet.py SHEET_ID --format json > data.json

# Process with jq
jq '.[] | select(.[3] == "Food")' data.json
```

### Batch Import

```bash
cd google-sheets/scripts

# Prepare CSV with multiple rows
cat > /tmp/batch.csv << EOF
Alice,alice@example.com,Developer
Bob,bob@example.com,Designer
Carol,carol@example.com,Manager
EOF

# Import all at once
python3 append_row.py SHEET_ID --csv-file /tmp/batch.csv
```

## Formulas and Formatting

**Writing formulas:**
```bash
# Formulas are written as strings
python3 write_sheet.py SHEET_ID --range "Sheet1!D2" \
  --data '[["=SUM(B2:C2)"]]'
```

**Limitations:**
- No formatting support (colors, fonts, etc.)
- For advanced formatting, use web UI or Google Sheets API batchUpdate requests

## Script Dependencies

All scripts require:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Notes

- **Account:** Gladys's personal Google account (not Simon's)
- **Storage:** Sheets count against 15GB Drive quota
- **Cell limits:** 10 million cells per spreadsheet (more than enough)
- **Rate limits:** 300 requests/minute per user
- **Collaboration:** Spreadsheets are private by default; share manually via web UI
