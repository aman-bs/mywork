from datetime import datetime
import logging

DATE_FORMATS = [
    "%Y-%m-%d",                # 2024-01-01
    "%m/%d/%Y",                # 01/01/2024
    "%d/%m/%Y",                # 01/12/2024 (DD/MM/YYYY)
    "%d-%m-%Y",                # 21-03-2024
    "%m-%d-%Y",                # 11-03-2024
    "%Y-%m-%dT%H:%M:%S",       # 2024-01-01T00:00:00
    "%Y-%m-%dT%H:%M:%S.%f",    # 2024-01-01T00:00:00.123456
    "%m/%d/%Y %H:%M:%S",       # 01/01/2024 12:00:00
    "%d/%m/%Y %H:%M:%S",       # 01/12/2024 12:00:00 (DD/MM/YYYY HH:MM:SS)
    "%B %d, %Y",               # January 01, 2024
    "%b %d, %Y",               # Jan 01, 2024
]

def parse_date(date_string: str) -> datetime:
    if not date_string:
        return None

    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            # logging.error(f"Failed to parse date: {date_string}")
            continue  # Try the next format if this one fails

    return None

# Test the function with various formats
test_dates = [
    "2024-01-01",
    "01/01/2024",
    "01/12/2024",
    "2024-01-01T00:00:00",
    "2024-01-01T00:00:00.123456",
    "2024-01-01 T00:00:00.123456",
    "01/01/2024 12:00:00",
    "January 01, 2024",
    "Jan 01, 2024",
    "01-03-2024"
]

for test_date in test_dates:
    parsed_date = parse_date(test_date)
    print(f"Original: {test_date} -> Parsed: {parsed_date}")


datetime.datetime(2024, 2, 14, 0, 0)
datetime.datetime(2024, 2, 14, 0, 0)