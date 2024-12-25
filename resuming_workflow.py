"""
using restart to resume failed workflow due to functional error or due to any node failure
"""

from toil.common import Toil
from toil.job import Job

class Hello(Job):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self, fileStore):
        return f"Hello, I have a message for you: {self.message}"

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = Job.Runner.getDefaultArgumentParser()
    parser.add_argument("--m", required=True, help="To echo user-defined message")
    
    args = parser.parse_args()

    options = Job.Runner.getDefaultOptions(args.jobStore)
    options.clean = "always"  
    options.logLevel = "OFF"

    hello_obj = Hello(args.m)

    with Toil(options) as toil:
        print(toil.start(hello_obj))


# python3 resuming_workflow.py --m "Hi, how are you?" file:my-job-store
# python3 resuming_workflow.py --m "Continuing your workflow" file:my-job-store --restart