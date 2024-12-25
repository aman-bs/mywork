import logging

from toil.job import Job
from toil.common import Toil
from toil.lib.io import mkdtemp

from dataclasses import dataclass, field, fields
from datetime import datetime

'''
To test 
1. augmet_run_obj created in J1, passed into J2 and then called push_run_message.
2. augmet_run_obj created in J2 and then called.

this is to check feasibility that augmet_run_object which is created in start function can 
be passed into "prepare_data_from_upload_and_launch" or not.(line 773)

'''

config = {
    "api_key": "abcd_123",
    "default_api_key":"xyz_789",
    "token": "mock_tocken"
}

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

@dataclass
class AugmetRun:
    # job:Job
    name: str
    date_of_birth: str
    gender: str=field(init=False)
    age: int = field(init=False)
    counter: int = field(init=False)

    def __post_init__(self):
        super().__init__()
        self.load_run_info()

    def load_run_info(self):
        # require a better exception hand
        self.counter=0
        self.gender="Male"
        self.age=self.calculate_age(self.date_of_birth)

    def __setattr__(self, key, value):
        valid_fields = {field.name for field in fields(self.__class__)}
        print(f"All valid field values: {valid_fields}")
        if key == 'gender' and hasattr(self, 'gender'):
            raise AttributeError(f"Cannot modify attribute '{key}', it is already set.")
        
        if key not in valid_fields:
            raise AttributeError(f"Cannot set attribute '{key}', it is not a valid attribute.")
        
        super().__setattr__(key, value)

                
    def calculate_age(self, dob):
        dob = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

def submit_demultiplex(job, augmet_run_obj):
    name = augmet_run_obj.name
    age = augmet_run_obj.age
    gender = augmet_run_obj.gender
    job.log(f"[SUBMIT DEMULTIPLEX...] {name} is {age} years old and gender is {gender}.")
    demux_folder="path/to/folder"
    sample_dict={
        'key1':'v1',
        'key2':'v2'
        }
    return demux_folder, sample_dict

def capture_report_log_errors(job, augmet_run_obj):
    name = augmet_run_obj.name
    age = augmet_run_obj.age
    gender = augmet_run_obj.gender
    job.log(f"[CAPTURE REPORT LOG...]{name} is {age} years old and gender is {gender}.")
    lst = ["Ram", "Shyam"]
    return lst
            
def return_passed_samples(job, a,b):
    pass_list = ["pass"]
    fail_list = ["fail"]
    return pass_list, fail_list

def start(job):
    print("Entered into start function")
    try:
        p1 = AugmetRun( "Aman", "2000-07-10")
        p1.age = "2000-07-19"  # This will work
        job.log(f"updated age to {p1.age}")
        run_demultiplex = job.addFollowOnJobFn(submit_demultiplex, p1)
        demux_out = run_demultiplex.rv(0)
        sample_dict = run_demultiplex.rv(1)
        run_demultiplex.addFollowOnJobFn(capture_report_log_errors, p1)
        verify_fastq_sizes = run_demultiplex.addFollowOnJobFn(  # type:ignore
                return_passed_samples,
                demux_out,
                sample_dict,
                p1,
        )
        # job.log(f"{p1.job.rv()}")
        passed_samples = verify_fastq_sizes.rv(0)
        job.log(f"REturned values are as follows: {demux_out}")
    except AttributeError as e:
        job.log(e)

if __name__ == "__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args()
    options.clean = "always"

    parent_job = Job.wrapJobFn(start)

    with Toil(options) as toil:
        output = toil.start(parent_job)
        print("Entered into start function")

    print(f"output obtained = {output}")