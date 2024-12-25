import pytest
from unittest.mock import MagicMock
from main8 import AugmetRun, submit_demultiplex, capture_report_log_errors, return_passed_samples, start

@pytest.fixture
def mock_job(mocker):
    """Fixture to create a mocked Toil job."""
    job = MagicMock()
    job.log = MagicMock()
    return job

def test_augmet_run_init(mock_job):
    """Test AugmetRun object creation and attributes."""
    run_obj = AugmetRun(mock_job, "Aman", "2000-07-10")

    assert run_obj.name == "Aman"
    assert run_obj.age == 24
    assert run_obj.gender == "Male"

def test_submit_demultiplex(mock_job):
    """Test submit_demultiplex function."""
    run_obj = AugmetRun(mock_job, "Aman", "2000-07-10")
    demux_folder, sample_dict = submit_demultiplex(mock_job, run_obj)
    
    assert demux_folder == "path/to/folder"
    assert sample_dict == {'key1': 'v1', 'key2': 'v2'}

def test_capture_report_log_errors(mock_job):
    """Test capture_report_log_errors function."""
    run_obj = AugmetRun(mock_job, "Aman", "2000-07-10")
    lst = capture_report_log_errors(mock_job, "some_output", run_obj)
    
    assert lst == ["Ram", "Shyam"]

def test_return_passed_samples(mock_job):
    """Test return_passed_samples function."""
    run_obj = AugmetRun(mock_job, "Aman", "2000-07-10")
    pass_list, fail_list = return_passed_samples(mock_job, "some_output", {}, run_obj)
    
    assert pass_list == ["pass"]
    assert fail_list == ["fail"]

def test_start_function(mock_job):
    """Test the start function."""
    start(mock_job)
    
    # You can check if the logs were called with expected values.
    mock_job.log.assert_any_call("Entered into start function")
    mock_job.log.assert_any_call("updated age to 2000-07-19")  # Check the updated age logic

if __name__ == "__main__":
    pytest.main()
