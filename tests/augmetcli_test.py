import pytest
import json
import datetime
import click
from augmetcli.base import validate_filter 

def test_validate_filter_empty_input():
    """Test that an empty input string returns an empty dictionary."""
    ctx = None 
    param = None  
    value = ''
    
    result = validate_filter(ctx, param, value)
    
    assert result == {}

def test_validate_filter_invalid_json():
    """Test invalid JSON input."""
    ctx = None
    param = None
    value = 'invalid_json'

    with pytest.raises(click.BadParameter):
        validate_filter(ctx, param, value)

def test_validate_filter_valid_json():
    """Test valid JSON input."""
    ctx = None
    param = None
    value = '{"completed_at": {"start": "2024-01-01", "end": "2024-01-02"}}'
    
    result = validate_filter(ctx, param, value)
    
    assert isinstance(result, dict)
    assert 'completed_at' in result
    assert isinstance(result['completed_at'], dict)

@pytest.mark.parametrize("date_str, expected", [
    ("2024-01-01", True),
    ("01/01/2024", True),
    ("01-01-2024", True),
    ("2024-01-01T00:00:00", True),
    ("2024-01-01T00:00:00.123456", True),
    ("January 01, 2024", True),
    ("Jan 01, 2024", True),
    ("invalid-date", False),
    ("2024-99-99", False),
])
def test_custom_date_time_validator(date_str, expected):
    """Test the custom date time validator."""
    result = validate_filter.custom_date_time_validator(date_str)
    
    if expected:
        assert isinstance(result, datetime.datetime)
    else:
        assert result is None

def test_validate_filter_valid_completed_at_with_start_and_end():
    """Test the filter when 'completed_at' has valid start and end dates."""
    ctx = None
    param = None
    value = '{"completed_at": {"start": "2024-01-01", "end": "2024-01-02"}}'

    result = validate_filter(ctx, param, value)
    
    assert isinstance(result, dict)
    assert 'completed_at' in result
    assert 'start' in result['completed_at']
    assert 'end' in result['completed_at']

def test_validate_filter_invalid_completed_at_with_start_and_end():
    """Test the filter when 'completed_at' has invalid start and end dates."""
    ctx = None
    param = None
    value = '{"completed_at": {"start": "invalid-date", "end": "2024-01-02"}}'

    with pytest.raises(click.BadParameter):
        validate_filter(ctx, param, value)

    value = '{"completed_at": {"start": "2024-01-01", "end": "invalid-date"}}'
    
    with pytest.raises(click.BadParameter):
        validate_filter(ctx, param, value)

def test_validate_filter_valid_completed_at_with_single_date():
    """Test the filter when 'completed_at' has a single valid date."""
    ctx = None
    param = None
    value = '{"completed_at": "2024-01-01"}'
    
    result = validate_filter(ctx, param, value)
    
    assert isinstance(result, dict)
    assert 'completed_at' in result
    assert isinstance(result['completed_at'], datetime.datetime)

def test_validate_filter_invalid_completed_at_with_single_date():
    """Test the filter when 'completed_at' has an invalid single date."""
    ctx = None
    param = None
    value = '{"completed_at": "invalid-date"}'
    
    with pytest.raises(click.BadParameter):
        validate_filter(ctx, param, value)
