import json
import math
import random
from typing import Iterable, Callable

from workload_sequencing import Job

STATIONS = 2


def simulated_annealing(
        initial_solution: list[list[Job]],
        cost_function,
        temperature: int,
        cooling_rate: float,
        stopping_temperature: int
):
    current_solution: list[list[Job]] = initial_solution
    best_solution: list[list[Job]] = initial_solution

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


def generate_neighbor(packages: list[list[Job]]) -> list[list[Job]]:
    x1 = random.randint(0, len(packages) - 1)
    x2 = random.randint(0, len(packages) - 1)
    return_packages = packages.copy()
    return_packages[x2], return_packages[x1] = packages[x1], packages[x2]
    return return_packages


def cost_function(packages: list[list[Job]]) -> int:
    usage = {s: 0 for s in range(STATIONS)}
    for jobs in packages:
        for s in range(STATIONS):
            usage[s] = max(usage[s], usage[s - 1] if s > 0 else 0) + jobs[s].processing_time_s

    return usage[STATIONS - 1]


def group_by(iterable: Iterable, key: Callable) -> dict[..., list]:
    """Group items by their key

    :param iterable: Iterable of items
    :param key: Key function to map an item to its key
    :return: Dict of keys to the list of items with that key
    """
    key2item = {}
    for item in iterable:
        key_value = key(item)
        if isinstance(key_value, list):
            key_value = tuple(key_value)
        key2item.setdefault(key_value, []).append(item)
    return key2item


if __name__ == '__main__':
    with open(file="sequencing.json", mode="r", encoding="utf-8") as seq_json:
        jobs = [Job(**job) for job in json.load(seq_json)]

    packages: list[list[Job]] = [jobs[s * STATIONS:s * STATIONS + STATIONS] for s in range(int(len(jobs) / STATIONS))]

    print("Packages:")
    for package in packages:
        print(f"\t{[job.processing_time_s for job in package]}")

    initial_solution: list[list[Job]] = packages  # Provide your initial solution
    temperature = 1000  # Set the initial temperature
    cooling_rate = 0.8  # Set the cooling rate
    stopping_temperature = 1  # Set the stopping temperature

    print("Initial solution:", cost_function(initial_solution))
    best_solution = simulated_annealing(initial_solution, cost_function, temperature, cooling_rate,
                                        stopping_temperature)
    print("Best solution:", cost_function(best_solution))
