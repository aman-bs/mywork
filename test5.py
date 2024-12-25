'''
Tried self.log by inheriting Toil but log is not appearing
'''
from toil.common import Toil
from toil.job import Job, logger
# from toil.job.Job.l
from dataclasses import dataclass, field

@dataclass
class Helper(Job):
    api_key:str
    message: str 
    # get_message: str = field(init=False)

    def __post_init__(self):
        Job.__init__(self)
        # self.message = "Test message"    #1
        # self.get_message = self.helper_function(message)    #1

    def run(self, fileStore):
        self.log(f"Triggering message: {self.message} with api_key: {self.api_key} ") #3
        # self.log("Some random toil logger") #2
        return f"Triggering message: {self.message} with api_key: {self.api_key} "

def start(job:Job, message:str):
    # job.log(f"{message}")
    help_obj = Helper("abc_123", message)
    # val = help_obj.get_message #1
    # val = help_obj.helper_function(message) #2
    # val = help_obj.run() #3
    val= job.log(f"from fun2: {help_obj}")
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
