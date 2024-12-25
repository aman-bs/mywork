from toil.common import Toil
from toil.job import Job
from dataclasses import dataclass, field

@dataclass
class Helper(Job):
    api_key:str
    get_message: str = field(init=False)

    def __post_init__(self):
        Job.__init__(self)
        # message = "Test message"    #1
        # self.get_message = self.helper_function(message)    #1

    def helper_function(self, job, message: str):
        job.log(f"Triggering message: {message} with api_key: {self.api_key} ") #3
        # self.log("Some random toil logger") #2
        return f"Triggering message: {message} with api_key: {self.api_key} "

def start(job:Job, message:str):
    # job.log(f"{message}")
    help_obj = Helper("abc_123")
    # val = help_obj.get_message #1
    # val = help_obj.helper_function(message) #2
    val = help_obj.helper_function(job, message) #3
    job.log(f"from fun2: {val}")
    return val

# def fun1(job:Job, message:str):
#     job.log(f"{message}")
#     new_message = message + "Again..."
#     fun2(job, new_message)
#     return

# def main(job:Job, )

if __name__=="__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args()
    options.clean = "always"

    main = Job.wrapJobFn(start, "Hi There!!")

    with Toil(options) as toil:
        toil.start(main)
