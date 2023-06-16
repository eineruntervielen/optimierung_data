import random

import pandas as pd

NUM_MACHINES = 5
NUM_JOBS = 10

TASKS = [f"task_{n}" for n in range(NUM_MACHINES)]
JOBS = [f"jobs_{n}" for n in range(NUM_JOBS)]
MACHINES = [f"m_{n}" for n in range(NUM_MACHINES)]


def gen_random_job_table() -> pd.DataFrame:
    data = []
    for _ in range(NUM_JOBS):
        times = [f"t_{random.randint(1, 15)}" for _ in range(NUM_MACHINES)]
        perm_machines = MACHINES.copy()
        random.shuffle(perm_machines)
        data.append(list(zip(perm_machines, times)))
    return pd.DataFrame(data=data, columns=TASKS, index=JOBS)


if __name__ == '__main__':
    random.seed(1)
    df = gen_random_job_table()
    print(df)
