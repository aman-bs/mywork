"""
program to learn how to add command line arguments to your toil workflow
"""

from toil.common import Toil
from toil.job import Job

class Hello(Job):
    def __init__(self, message):
        Job.__init__(self)
        self.message=message

    def run(self, fileStore):
        return f"Hello, i have a message for you: {self.message}"

if __name__ == "__main__":
    # using argparse
    
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Just for learning")
    parser.add_argument("--m", required=True, help="To echo user-defined message")
    parser.add_argument("--clean", default="always", help="Clean all the intermediary files after the process is finished")
    parser.add_argument("--jobStore", required=True, help="Specify the job store (e.g., file:my-job-store)")
    args = parser.parse_args()
    options = Job.Runner.getDefaultOptions(args.jobStore)
    options.clean = args.clean  # Set clean option
    hello_obj = Hello(args.m)

    with Toil(options) as toil:
        print(toil.start(hello_obj))

# python3 commandLine_with_toil.py  --m "Hi, how are you?" --clean always --jobStore file:my-job-store
    
"""
# using getDefaultArgumentParser()


if __name__=="__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    parser.add_argument("--m", help="to echo a user defined message", required=True)
    options = parser.parse_args()
    options.clean="always"
    options.logLevel = "OFF"
    hello_obj = Hello(options.m)
    with Toil(options) as toil:
        print(toil.start(hello_obj))


python3 commandLine_with_toil.py --m "hello there how r u doing" file:my-job-store

"""