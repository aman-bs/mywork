import pytest
from unittest import mock
from pathlib import Path

# Example of your uploader function (simplified)
def upload_file(file_path: str):
    path = Path(file_path)
    if not path.absolute().exists():  # Checking if the file exists
        raise FileNotFoundError(f"File {file_path} not found")

    # Simulated cloud upload logic
    # Your code to upload the file goes here
    print(f"Uploading {file_path} to the cloud...")
    return True

# Fixture to mock pathlib.Path.exists method
@pytest.fixture
def mock_file_system(monkeypatch):
    # Mock the exists method of pathlib.Path to always return True for the specific files
    def mock_exists(self):
        # Return True for our specific fake files
        if self.name in ["7682736582_R1_001.fastq.gz", "7682736582_R2_001.fastq.gz"]:
            return True
        return False

    # Use monkeypatch to replace pathlib.Path.exists with the mock method
    monkeypatch.setattr(Path, "exists", mock_exists)

    # Optionally, mock cloud upload if necessary
    cloud_mock = mock.Mock()
    cloud_mock.return_value = True  # Simulate a successful upload
    monkeypatch.setattr("your_module.upload_file", cloud_mock)

    return cloud_mock

# Test the uploader with mocked files
def test_upload(mock_file_system):
    # Test with file paths
    file1 = "7682736582_R1_001.fastq.gz"
    file2 = "7682736582_R2_001.fastq.gz"
    
    # Call your uploader function (it will use the mocked file system)
    result1 = upload_file(file1)
    result2 = upload_file(file2)
    
    # Check that the upload function is called correctly
    mock_file_system.assert_any_call(file1)
    mock_file_system.assert_any_call(file2)
    
    # Optionally, assert the returned result from your upload function
    assert result1 is True
    assert result2 is True
