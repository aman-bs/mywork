from toil.common import Toil
from toil.job import Job

def hello_world(message):
    return f"Hi, a message from hello world function: {message}"

if __name__=="__main__":
    parser=Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args()
    options.clean="always"
    options.logLevel="OFF"

    hello_job = Job.wrapFn(hello_world, "Greetings of the day, reader")
    with Toil(options) as toil:
        print(toil.start(hello_job))
