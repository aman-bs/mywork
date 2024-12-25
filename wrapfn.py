from toil.job import Job
from toil.common import Toil
from argparse import ArgumentParser

def hello1(message, memory="1G", cores=1, disk="1G"):
    return f"Hello there, this is first function with message {message}"

if __name__=="__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args()
    options.clean = "always"
    parent_job = Job.wrapFn(hello1, "Hi buddy!!")
    with Toil(options) as toil:
        output=toil.start(parent_job)
    print(output)
