, create_symlink, compress_file
from augmet.generic.utils import get_operables



# def test_get_operables_success(dummy_job, sample_execution_info):



def test_create_symlink_success(dummy_job):
    source = "source_path"
    dest = "dest_path"

    with patch('os.symlink', MagicMock()) as mock_symlink:
        create_symlink(dummy_job, source, dest)

        # Check that the symlink function was called with the right arguments
        mock_symlink.assert_called_once_with(source, dest)
        dummy_job.log.assert_any_call(f"Linking {source} to {dest}")
        dummy_job.log.assert_any_call(f"[BASE] {source} Linking successeded")

def test_create_symlink_already_exists(dummy_job):
    """Test that create_symlink handles FileExistsError gracefully."""
    source = "source_path"
    dest = "dest_path"

    with patch('os.symlink', MagicMock(side_effect=FileExistsError)) as mock_symlink:
        create_symlink(dummy_job, source, dest)

        mock_symlink.assert_called_once_with(source, dest)
        dummy_job.log.assert_any_call(f"Linking {source} to {dest}")
        dummy_job.log.assert_any_call(f"Skipping: Symlink already exists. {dest}")

def test_compress_file_success(dummy_job,sample_execution_info):
    mock_input_path = ['pytest_folder/RawDataQC/some_sample_name/stage.fastp.txt']
    compressed_fname = "pytest_folder/RawDataQC/some_sample_name/stage.fastp.txt.gz"
    mock_compressed_suffixes = ['.txt']
    suffix = ".txt"