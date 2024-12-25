from toil.common import Toil
from toil.job import Job

def first_job(job):
    result = "Hello, World!"
    return result

def second_job(job, previous_result):
    job.log(f"Received from first job: {previous_result}")

if __name__ == "__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args()
    options.clean = "always"
    options.logLevel = "INFO"
    parent = Job.wrapJobFn(first_job)
    parent.addChildJobFn(second_job, parent.rv())
    with Toil(options) as toil:
        print(toil.start(parent))
