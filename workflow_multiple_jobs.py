"""
A program to learn about addChild, addChildFn, addChildJobFn, the sequence of exection of parent, child
and FollowOn jobs (parent>child>followon), also how Dynamic job creation works
"""
from toil.common import Toil
from toil.job import Job

def helloWorld3(job, message):
    job_id = job.jobStoreID  
    job.log(f"[Child Job ID: {job_id}] {message}")

def helloWorld(job, message):
    job_id = job.jobStoreID  
    job.addChildJobFn(helloWorld3, f" world3 Child from {job_id}") # testing Dynamic job creation
    job.log(f"[Parent Job ID: {job_id}] Hi, here is a message for you: {message}")

def helloWorld2(message):
    return f"[Sibling] Hi from vanilla: {message}"

if __name__ == "__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args()
    options.clean = "always"
    options.logLevel = "INFO"

    parent = Job.wrapJobFn(helloWorld, "First")

    parent.addChildJobFn(helloWorld, "Second")
    j2 = Job.wrapJobFn(helloWorld, "Third")
    j3 = Job.wrapJobFn(helloWorld, "Last")
    # parent.addChildFn(helloWorld2, "Sibling")
    parent.addChild(j2)
    parent.addFollowOn(j3)

    with Toil(options) as toil:
        toil.start(parent)
