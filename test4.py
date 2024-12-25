from toil.common import Toil
from toil.job import Job
from dataclasses import dataclass, field

@dataclass
class Mock(Job):
    def fun3(self, job, obj):
        job.log(f"Message from fun3: {obj}")
        job.log(f"new key added = {obj.nationality}")


class Helper(Job):
    def __init__(self, api_key):
        Job.__init__(self)
        self.api_key=api_key

        # message = "Test message"
        # self.get_message = self.helper_function(message)

    def helper_function(self,job: Job, message):
        job.log(f"from helper function: Triggering message: {message} with api_key: {self.api_key} ")
        # self.log("Some random toil logger")
        return f"Triggering message: {message} with api_key: {self.api_key} "

def fun2(job:Job, message:str):
    # job.log(f"{message}")
    help_obj = Helper("abc_123")
    # val = help_obj.get_message
    val = help_obj.helper_function(job, message)
    job.log(f"from fun2: {val}")
    help_obj.nationality = "Indian"
    Mock().fun3(job, help_obj)
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

    main = Job.wrapJobFn(fun2, "Hi There!!")

    with Toil(options) as toil:
        toil.start(main)
