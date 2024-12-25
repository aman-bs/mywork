"""
defining a workflow in toil, and triggering it as an object
"""

from toil.common import Toil
from toil.job import Job
from toil.lib.io import mkdtemp
import os

class Hello(Job):
    def __init__(self, message):
        super().__init__(self)
        self.message=message
    def run(self, fileStore):
        return f"Hello world, here is a message {self.message}"
    
if __name__ == "__main__":
    jobstore: str = mkdtemp("tutorial_invokeworkflow")
    os.rmdir(jobstore)
    options = Job.Runner.getDefaultOptions(jobstore)
    options.logLevel = "OFF"
    options.clean = "always"

    hello_job = Hello("Woot")
    with Toil(options) as toil:
        print(toil.start(hello_job))
