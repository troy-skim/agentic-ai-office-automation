import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
CREDS_PATH = "config/gsheet_service_account.json"


def get_gsheet_client():
    """Create and return Google Sheets client

    Returns:
        gspread.client.Client: Authorized gspread client instance.
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, SCOPES)
    return gspread.authorize(creds)


def write_to_gsheet(
    data: dict | list[dict],
    sheet_name: str = "Sheet1",
    spreadsheet_name: str = "AgenticAutomation",
):
    """Append structured data to specified Google Sheet

    Args:
        data (dict | list[dict]): Row(s) of data to append.
        sheet_name (str, optional): Name of the target worsheet tab. Defaults to Sheet1.
        spreadsheet_name (str, optional): Name of the google sheet to open. Defaults to "AgenticAutomation".
    """
    client = get_gsheet_client()
    sh = client.open(spreadsheet_name)

    try:
        worksheet = sh.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sh.add_worksheet(title=sheet_name, rows="100", cols="20")

    df = pd.DataFrame([data] if isinstance(data, dict) else data)

    headers = df.columns.tolist()

    # Ensure all rows use the same header order, even if missing
    df.fillna("", inplace=True)
    rows = df[headers].astype(str).values.tolist()

    # If sheet is empty, write header first
    if worksheet.row_count == 0 or not any(
        cell.strip() for cell in worksheet.row_values(1)
    ):
        worksheet.append_row(headers)

    worksheet.append_rows(rows)
    print(f"✅ Google Sheet '{sheet_name}' updated.")
