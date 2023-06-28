import random
from pprint import pprint

import pandas as pd  # type: ignore

MachineId = str
ProcessingTime = int
Task = tuple[MachineId, ProcessingTime]
Job = list[Task]
JobTaskMatrix = list[Job]


def transform_to_matrix(data: pd.DataFrame) -> JobTaskMatrix:
    """Extracts the data from a pandas DataFrame and returns a nested array
    """
    clean = list(map(lambda row:
                     list(map(lambda e: (int(e[0].split("_")[1]), int(e[1].split("_")[1])), row)),
                     data.values))

    return clean


def gen_random_job_table(num_machines: int, num_jobs: int, seed: int = 0) -> pd.DataFrame:
    random.seed(seed)
    df_columns = [f"task_{n}" for n in range(num_machines)]
    df_indices = [f"jobs_{n}" for n in range(num_jobs)]
    data = list(list(zip(
        [f"t_{random.randint(1, 15)}" for _ in range(num_machines)],
        random.sample([f"m_{n}" for n in range(num_machines)], k=num_machines)
    ) for _ in range(num_jobs)))
    return pd.DataFrame(data=data, columns=df_columns, index=df_indices)


if __name__ == '__main__':
    df = gen_random_job_table(num_jobs=10, num_machines=5)
    df2 = transform_to_matrix(df)
    pprint(df2)
    from kruk_job_shop import solve_model

    print(solve_model(df2))
