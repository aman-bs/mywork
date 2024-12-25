# import logging
# import sys
# from toil.job import Job
# from toil.common import Toil
# from toil.lib.io import mkdtemp

# from toil.realtimeLogger import RealtimeLogger
# # Set up logging
# def configure_logging():
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)
#     toil_logger = logging.getLogger('toil')
#     toil_logger.setLevel(logging.INFO)

# # Call this function at the beginning of your script
# configure_logging()

# log = logging.getLogger(__name__)

# # The rest of your code remains the same...

# def start(job):
#     print("Entered into start function")
#     raise RuntimeError()
#     # Your existing logic...

# if __name__ == "__main__":
#     parser = Job.Runner.getDefaultArgumentParser()
#     options = parser.parse_args()
#     options.clean = "always"

#     parent_job = Job.wrapJobFn(start)

#     with Toil(options) as toil:
#         output = toil.start(parent_job)

#     print(f"output obtained = {output}")

class A:
    def __init__(self):
        self.counter=0

    def fun(self):
        return self.counter

if __name__=="__main__":
    obj = A()
    obj.counter+=1
    obj.counter+=1 
    obj.counter+=1 
    print(obj.fun())
    obj.counter+=1 
    obj.counter+=1 
    print(obj.fun())