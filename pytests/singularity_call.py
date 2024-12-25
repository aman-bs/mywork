import pytest
import json
import os
import shutil
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path
import subprocess
from augmet.jobs.basic import singularity_call  # Adjust import based on your module structure

@pytest.fixture
def mock_job():
    """Fixture to create a mock Job object."""
    job = MagicMock()
    job.log = MagicMock()
    return job

@pytest.fixture
def tool_parameters():
    return ["param1", "param2"]

@pytest.fixture
def execution_info():
    return ("stage", "sample", "sample_json")

@pytest.fixture(scope="module")
def sample_json_dict():
    sample_json = {
        "api_key": "API_123",
        "sample_info": {
            "workflow_info":{
                    "run_sample_id": "Dummy_Run_1234"
                }
            }
    }
    return sample_json

@pytest.fixture
def create_checkpoint_dir():
    checkpoint_dir = "sample_json"
    os.makedirs(checkpoint_dir, exist_ok=True)
    yield
    # Clean up the directory after the test
    # if os.path.exists(checkpoint_dir):
    #     os.rmdir(checkpoint_dir)  # You may want to remove files inside if necessary
    shutil.rmtree(checkpoint_dir)


def test_singularity_call_success(mock_job, tool_parameters, execution_info, sample_json_dict, create_checkpoint_dir):
    mock_tool = Path("/path/to/some_singularity_tool.sif")
    mock_exec_command = ["singularity", "exec", str(mock_tool)] + tool_parameters
    
    with patch("builtins.open", mock_open(read_data=json.dumps(sample_json_dict))):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            exit_code = singularity_call(
                job=mock_job,
                tool_parameters=tool_parameters,
                tool=mock_tool,
                execution_info=execution_info,
                stage="test_stage"
            )

            mock_run.assert_called_once_with(
                mock_exec_command,
                cwd=None,
                check=True,
            )
            assert exit_code == 0

# def test_singularity_call_with_error(mock_job, tool_parameters, execution_info):
#     mock_tool = Path("/path/to/mock_tool.sif")
    
#     with patch("subprocess.run") as mock_run:
#         mock_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd="mock_command")
        
#         with pytest.raises(RuntimeError):
#             singularity_call(
#                 job=mock_job,
#                 tool_parameters=tool_parameters,
#                 tool=mock_tool,
#                 execution_info=execution_info,
#                 stage="test_stage"
#             )

#         mock_run.assert_called_once()

# def test_singularity_call_with_popen(mock_job, tool_parameters, execution_info):
#     mock_tool = Path("/path/to/mock_tool.sif")
#     mock_exec_command = ["singularity", "exec", str(mock_tool)] + tool_parameters
    
#     with patch("subprocess.Popen") as mock_popen:
#         mock_process = MagicMock()
#         mock_process.communicate.return_value = (b"output", b"error")
#         mock_process.returncode = 0
#         mock_popen.return_value = mock_process
        
#         exit_code = singularity_call(
#             job=mock_job,
#             tool_parameters=tool_parameters,
#             tool=mock_tool,
#             execution_info=execution_info,
#             stage="test_stage",
#             communicate=True
#         )

#         mock_popen.assert_called_once_with(
#             mock_exec_command,
#             cwd=None,
#             stdin=None,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE
#         )
#         assert exit_code == 0
#         mock_process.communicate.assert_called_once()



    """_summary_
    """



# import pytest
# import json
# import os
# import shutil
# from unittest.mock import MagicMock, patch, mock_open
# from pathlib import Path
# import subprocess
# from augmet.jobs.basic import singularity_call  # Adjust import based on your module structure

# @pytest.fixture
# def dummy_job():
#     """Fixture to create a mock Job object."""
#     job = MagicMock()
#     job.log = MagicMock()
#     return job

# @pytest.fixture
# def execution_info():
#     return ("stage", "sample/json/path/samplejson.json", "sample_json")

# @pytest.fixture
# def sample_execution_info():
#     return ("stage", "sample/json/path/samplejson.json", "base_dir")

# @pytest.fixture(scope="module")
# def sample_json_file_dict():
#     sample_json = {
#         "api_key": "API_123",
#         "sample_info": {
#             "workflow_info":{
#                     "run_sample_id": "Dummy_Run_1234"
#                 }
#             }
#     }
#     return sample_json

# @pytest.fixture
# def create_checkpoint_dir():
#     checkpoint_dir = "base_dir"
#     os.makedirs(checkpoint_dir, exist_ok=True)
#     yield
#     shutil.rmtree(checkpoint_dir)


# def test_singularity_call_success(dummy_job, sample_execution_info, sample_json_file_dict, create_checkpoint_dir):
#     mock_tool = Path("/path/to/some_singularity_tool.sif")
#     tool_parameters = ["param1", "param2"]
#     mock_exec_command = ["singularity", "exec", str(mock_tool)] + tool_parameters
    
#     with patch("builtins.open", mock_open(read_data=json.dumps(sample_json_file_dict))):
#         with patch("subprocess.run") as mock_run:
#             mock_run.return_value.returncode = 0  
#             exit_code = singularity_call(
#                 job=dummy_job,
#                 tool_parameters=tool_parameters,
#                 tool=mock_tool,
#                 execution_info=sample_execution_info,
#                 stage="test_stage"
#             )

#             mock_run.assert_called_once_with(
#                 mock_exec_command,
#                 cwd=None,
#                 check=True,
#             )
#             assert exit_code == 0

# # def test_singularity_call_with_error(mock_job, tool_parameters, execution_info):
# #     mock_tool = Path("/path/to/mock_tool.sif")
    
# #     with patch("subprocess.run") as mock_run:
# #         mock_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd="mock_command")
        
# #         with pytest.raises(RuntimeError):
# #             singularity_call(
# #                 job=mock_job,
# #                 tool_parameters=tool_parameters,
# #                 tool=mock_tool,
# #                 execution_info=execution_info,
# #                 stage="test_stage"
# #             )

# #         mock_run.assert_called_once()

# # def test_singularity_call_with_popen(mock_job, tool_parameters, execution_info):
# #     mock_tool = Path("/path/to/mock_tool.sif")
# #     mock_exec_command = ["singularity", "exec", str(mock_tool)] + tool_parameters
    
# #     with patch("subprocess.Popen") as mock_popen:
# #         mock_process = MagicMock()
# #         mock_process.communicate.return_value = (b"output", b"error")
# #         mock_process.returncode = 0
# #         mock_popen.return_value = mock_process
        
# #         exit_code = singularity_call(
# #             job=mock_job,
# #             tool_parameters=tool_parameters,
# #             tool=mock_tool,
# #             execution_info=execution_info,
# #             stage="test_stage",
# #             communicate=True
# #         )

# #         mock_popen.assert_called_once_with(
# #             mock_exec_command,
# #             cwd=None,
# #             stdin=None,
# #             stdout=subprocess.PIPE,
# #             stderr=subprocess.PIPE
# #         )
# #         assert exit_code == 0
# #         mock_process.communicate.assert_called_once()
