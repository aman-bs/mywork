from dataclasses import dataclass, field, fields
from datetime import datetime

@dataclass
class Person:
    name: str
    date_of_birth: str
    gender: str=field(init=False)
    age: int = field(init=False)
    
    def __post_init__(self):
        super().__init__()
        self.load_run_info()
    
    def load_run_info(self):
        # require a better exception hand
        self.gender="Male"
        self.age=self.calculate_age(self.date_of_birth)


    def __setattr__(self, key, value):
        valid_fields = {field.name for field in fields(self.__class__)}
        print(f"Valid fields = {valid_fields}")
        if key == 'gender' and hasattr(self, 'gender'):
            raise AttributeError(f"Cannot modify attribute '{key}', it is already set.")
        
        if key not in valid_fields:
            raise AttributeError(f"Cannot set attribute '{key}', it is not a valid attribute.")
        
        super().__setattr__(key, value)

            
    def calculate_age(self, dob):
        if dob == "":
            raise ValueError("DOB not passed")
        dob = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

# Example usage
try:
    p1 = Person("Aman", "")
    print(f"Initialized = {p1}")

    p1.gender = "Female"  # This will raise an exception
except AttributeError as e:
    print(e)

# try:
#     p1.age = "2000-07-19"  # This will work
#     print(p1)
# except AttributeError as e:
#     print(e)
