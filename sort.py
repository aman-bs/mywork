from datetime import datetime, timedelta
from dateutil import parser
from calendar import monthrange
import logging

# Assuming extra_filter is already defined, as in your original example:
extra_filter = {"completed_at": {"start": "01/01/2024", "end": "31/01/2024"}}
extra_filter_query = {}

def parse_date(date_string: str) -> datetime:
    """
    Attempts to parse the given date string into a datetime object. 
    Uses `dateutil.parser.parse` which can handle various formats.
    """
    try:
        return parser.parse(date_string)
    except (ValueError, TypeError):
        logging.error(f"Failed to parse date: {date_string}")
        return None

if "completed_at" in extra_filter:
    completed_at_filter_value = extra_filter["completed_at"]
    extra_filter.pop("completed_at")
    
    if isinstance(completed_at_filter_value, dict):
        yy = datetime.today().year
        mm = datetime.today().month
        default_start_date = datetime(year=yy, month=mm, day=1)
        default_end_date = datetime(year=yy, month=mm, day=monthrange(yy, mm)[1])
        
        # Get start and end dates from the filter or use defaults
        start_cat = completed_at_filter_value.get("start", default_start_date)
        end_cat = completed_at_filter_value.get("end", default_end_date)
        
        # Parse start and end dates if they are strings
        if isinstance(start_cat, str):
            start_cat = parse_date(start_cat) or default_start_date
        if isinstance(end_cat, str):
            end_cat = parse_date(end_cat) or default_end_date

        # Prepare the filter query
        if not extra_filter_query:
            extra_filter_query["$match"] = {}

        extra_filter_query["$match"]["completed_at"] = {
            "$gte": start_cat,
            "$lte": end_cat,
        }

    elif isinstance(completed_at_filter_value, str):
        # Handle single string date input
        parsed_date = parse_date(completed_at_filter_value)
        if parsed_date:
            completed_at_value_min = parsed_date
            completed_at_value_max = completed_at_value_min + timedelta(days=1)

            # Prepare the filter query
            if not extra_filter_query:
                extra_filter_query["$match"] = {}

            extra_filter_query["$match"]["completed_at"] = {
                "$gte": completed_at_value_min,
                "$lte": completed_at_value_max,
            }
        else:
            logging.info(f"Invalid completed_at value received: {completed_at_filter_value}")
            completed_at_filter_value = ""