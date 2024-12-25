from toil.common import Toil
from toil.job import Job


def helloWorld(job, message, memory="1G", cores=1, disk="1G"):
    job.log(f"Here is the message for you!!: {message}")
    return ""
    
# def helloWorld2(job, message, memory="1G", cores=1, disk="1G"):
#     job.log(f"Hello, world!, here's a TESTTTTT HELLOWORLD2: {message}")
#     return f"Hello, world!, here's a message: {message}"
    
# def helloWorld3(job, message, memory="1G", cores=1, disk="1G"):
#     job.log(f"Hello, world!, here's a TESTTTTT HELLOWORLD3: {message}")
#     return f"Hello, world!, here's a message: {message}"


if __name__ == "__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args()
    options.clean = "always"
    parent_job = Job.wrapJobFn(helloWorld, "Parent Job called")
    job1 = parent_job.addFollowOnJobFn(helloWorld, "Hello from followonJob on parent job!!")
    job2 = parent_job.addChildJobFn(helloWorld, "Hello from child1 job on parent job!!")
    job2 = parent_job.addChildJobFn(helloWorld, "Hello from child2 job on parent job!!")
    job2 = job1.addFollowOnJobFn(helloWorld, "Hello from follow on job on parent's followon job!!")

    with Toil(options) as toil:
        output = toil.start(parent_job)
    print(output)