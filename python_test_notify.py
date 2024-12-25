# import logging
# from dataclasses import dataclass, field, fields
from datetime import datetime
# from toil.job import Job
# from toil.common import Toil
import time


# config = {
#     "api_key": "abcd_123",
#     "default_api_key":"xyz_789",
#     "token": "mock_tocken"
# }

def get_date_time_stamp() -> str:
    """Get current datetime stamp

    :return: Current data in format: DD/MM/YYYY HH:MM:SS
    :rtype: str
    """
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return str(dt_string)


# logging.basicConfig(level=logging.INFO)

# log = logging.getLogger(__name__)

# @dataclass
# class AugmetRun:
#     job: Job
#     name: str
#     date_of_birth: str
#     gender: str=field(init=False)
#     age: int = field(init=False)

#     def __post_init__(self):
#         super().__init__()
#         self.load_run_info()

#     def load_run_info(self):
#         self.gender="Male"
#         self.age=self.calculate_age(self.date_of_birth)

                
#     def calculate_age(self, dob):
#         dob = datetime.strptime(dob, "%Y-%m-%d")
#         today = datetime.today()
#         age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
#         return age

#     def notify(self, job, notification, admin_message = get_date_time_stamp()):
#         job.log(f"Notify: {notification} triggered with admin message: {admin_message}")
#         return True
    
# def start(job):
#     print("Entered into start function")
#     person_Aman = AugmetRun(job=job, name="Aman", date_of_birth="2001-07-10")
#     person_Aman.notify(job,"Hi Aman! Greetings of the day.")
#     time.sleep(10)
#     person_Aman.notify(job, "This is again a notification", "admin message")
#     time.sleep(10)
#     person_Aman.notify(job, "Hi")


# if __name__ == "__main__":
#     parser = Job.Runner.getDefaultArgumentParser()
#     options = parser.parse_args()
#     options.clean = "always"

#     parent_job = Job.wrapJobFn(start)

#     with Toil(options) as toil:
#         output = toil.start(parent_job)


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def notify(self, notification, admin_message = get_date_time_stamp()):
        print(f"Notify: {notification} triggered with admin message: {admin_message}")
        return True
    

def notify2(notification, admin_message = get_date_time_stamp()):
    print(f"Notify: {notification} triggered with admin message: {admin_message}")
    return True

if __name__ == "__main__":
    print(f"start time = {datetime.now()}")
    person_aman = Person("Aman", 23)
    person_aman.notify("Hi Aman! Greetings of the day.")
    time.sleep(5)
    person_aman.notify("Hi")
    print(f"second object start time = {datetime.now()}")
    person_jenith = Person("Jenith", 25)
    person_jenith.notify("Gi Jenith! Greetings of the day.")
    time.sleep(5)
    person_jenith.notify("Hi")
    print(f"end time = {datetime.now()}")
    notify2("Gello")
    time.sleep(5)
    notify2("Gelllloo")