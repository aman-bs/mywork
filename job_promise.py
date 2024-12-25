from toil.job import Job
from toil.common import Toil

def fun1(job):
    result = 5

def fun2(job, parent_result):
    x=7
    x = x + parent_result
    job.log(f"value of x={x}")

if __name__ == "__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args()
    options.clean = "always"
    options.logLevel = "INFO"
    parent = Job.wrapJobFn(fun1) 
    parent.addChildJobFn(fun2, parent.rv())

    with Toil(options) as toil:
        toil.start(parent)
