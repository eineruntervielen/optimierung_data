import json
import math
import random
from dataclasses import dataclass
from pprint import pp
from typing import Iterable, Callable
from kruk_job_shop import gen_data

STATIONS = 2


@dataclass
class Task:
    on_machine: int
    task_time: int


@dataclass
class Job:
    job_id: int
    tasks: list[Task]

@dataclass
class Machine:
    machine_id: int
    unavailable: int
    tasks_to_start_time: list[(int, Task)]


def simulated_annealing(
        initial_solution: list[Job],
        cost_function,
        temperature: int,
        cooling_rate: float,
        stopping_temperature: int
):
    current_solution: list[Job] = initial_solution
    best_solution: list[Job] = initial_solution

    while temperature > stopping_temperature:
        neighbor_solution = generate_neighbor(current_solution)
        current_cost = cost_function(current_solution)
        neighbor_cost = cost_function(neighbor_solution)

        print(f"{current_cost=} {neighbor_cost=} best: {cost_function(best_solution)}")

        if neighbor_cost < current_cost:
            current_solution = neighbor_solution
            if neighbor_cost < cost_function(best_solution):
                best_solution = neighbor_solution
                print(f"improve")
        else:
            probability = math.exp((current_cost - neighbor_cost) / temperature)
            if random.random() < probability:
                current_solution = neighbor_solution

        temperature *= cooling_rate
    return best_solution


def generate_neighbor(jobs: list[Job]) -> list[Job]:
    x1 = random.randint(0, len(jobs) - 1)
    x2 = random.randint(0, len(jobs) - 1)
    return_jobs = jobs.copy()
    return_jobs[x2], return_jobs[x1] = jobs[x1], jobs[x2]
    return return_jobs


def cost_function(jobs: list[Job], show: bool = False) -> int:
    if jobs:
        # jeder Job muss auf jeder Maschine bearbeitet werden.
        # Somit reicht es, die Anzahl der maschinen fpr den ersten
        # Job zu betrachten
        n_machines = len(jobs[0].tasks)
        machines = {machine: Machine(machine, 0, []) for machine in range(n_machines)}
        for job in jobs:
            current_time = 0
            for task in job.tasks:
                # fülle die Maschinen der Reihe nach auf
                current_time = max(machines[task.on_machine].unavailable, current_time) +  task.task_time
                # update
                machines[task.on_machine].unavailable = current_time
                machines[task.on_machine].tasks_to_start_time.append((current_time - task.task_time, task))
        if show:
            pp(machines)

        return max(machines.values(), key=lambda m: m.unavailable).unavailable

    return 0


if __name__ == '__main__':

    D = gen_data(m=10, n=3)
    pp(D)
    nJobs, nMachines = len(D), len(D[0])

    jobs = []
    for i in range(nJobs):
        tasks = [Task(*D[i][j]) for j in range(nMachines)]
        jobs.append(Job(i, tasks))

    pp(jobs)

    initial_solution: list[Job] = jobs  # Provide your initial solution
    temperature = 1000  # Set the initial temperature
    cooling_rate = 0.8  # Set the cooling rate
    stopping_temperature = 1  # Set the stopping temperature

    print("Initial solution:", cost_function(initial_solution, True))
    best_solution = simulated_annealing(initial_solution, cost_function, temperature, cooling_rate, stopping_temperature)
    print("Best solution:", cost_function(best_solution, True))
