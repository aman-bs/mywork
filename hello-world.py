from toil.job import Job
from toil.common import Toil
from dataclasses import dataclass


@dataclass
class Person(Job):
    name: str
    age: int
    gender: str
    food: str

    def __post_init__(self):
        # super().__init__()
        Job.__init__(self)

    def run(self, fileStore):
        return f"{self.name} (Age: {self.age}, Gender: {self.gender}) is eating {self.food}."

# def eat(Job, food):
#     Job.log(f"Aman 23, Gender: Male) is eating {food}.")
#     return "Success"

# def main(person, food):
#     return person.eat(food)

if __name__ == "__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args()
    options.clean = "always"


    # parent_job = Job.wrapJobFn(eat,"vegan")
    
    Aman = Person(name="Aman", age=23, gender="Male", food="Vegan")
    # parent_job = Job.wrapFn(main, Aman, "vegan")  
    parent_job = Job.wrapJobFn(Aman, "vegan")  

    print(parent_job)

    with Toil(options) as toil:
        output = toil.start(Aman)

    print(output)

