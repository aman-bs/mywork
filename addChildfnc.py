from toil.job import Job
from toil.common import Toil
from argparse import ArgumentParser

def helloFromChild(message, memory="1G", cores=1, disk="1G"):
    return f"Hi, from child function with message {message}"

def helloFromParent(message, memory="1G", cores=1, disk="1G"):
    return f"Hello from Parent function with message {message}"

if __name__ == "__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args()
    options.clean="always"
    parentJob = Job.wrapFn(helloFromParent,"I am a parent function")
    childJob = Job.wrapFn(helloFromChild,"I am child")
    parentJob.addChild(childJob)
    parentJob.add

    with Toil(options) as toil:
        output=toil.start(parentJob)
    print(output)