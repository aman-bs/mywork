from toil.job import Job
from toil.common import Toil
from toil.lib.io import mkdtemp

from dataclasses import dataclass, field

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

@dataclass
class AugmetRun:
    job: Job
    name: str
    age: int
    gender: str
    food: str
    api_key:str = field(init=False)
    runtime_trigger_message:str = field(init=False)

    def __post_init__(self):
        self.api_key=config.get("api_key", "default")
        self.runtime_trigger_message = self.trigger_message(self.job)
    

    def trigger_message(self, job):
        message = f"{self.name} (Age: {self.age}, Gender: {self.gender}), eats {self.food} food."
        push_run_status_message(job, message, self)
        return message

def push_run_status_message(job, message, augmet_run_obj):
    if isinstance(augmet_run_obj, str):
        api_key=config["default_api_key"]
    else:
        api_key=augmet_run_obj.api_key
    job.log(f"Message from logger using API Key={api_key}: {message}")

def prepare_data_from_upload_and_launch(job, augmet_run_obj):
    # augmet_run_obj = AugmetRun(job=job, name="Aman", age=23, gender="Male", food="food")
    push_run_status_message(job=job,message=f"Hit, ready to launch??", augmet_run_obj=augmet_run_obj)


def start(job, food):
    augmet_run_obj = AugmetRun(job=job, name="Aman", age=23, gender="Male", food=food)
    augmet_run_obj.runtime_trigger_message  #eat(job)
    job.addChildJobFn(push_run_status_message, "Hi, from child job","run_json_path")
    job.addChildJobFn(push_run_status_message, "Hi, from child job with Augmet Class",
    AugmetRun(Job(), name="Harshit", age=13, gender="Male", food="Chinese"))
    random_message = "This is a message to test with augmetrun object call"
    push_run_status_message(job=job, message=random_message, augmet_run_obj=augmet_run_obj)
    job.addChildJobFn(prepare_data_from_upload_and_launch, augmet_run_obj)

if __name__ == "__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args()
    options.clean = "always"

    parent_job = Job.wrapJobFn(start, "vegan")

    with Toil(options) as toil:
        output = toil.start(parent_job)

    print(f"output obtained = {output}")

