"""Build data for course Optimierung"""
import json
import random
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(kw_only=True, frozen=True)
class Job:
    """Reps a sequencing job"""

    job_id: str = field(default_factory=lambda: str(uuid4().hex))
    processing_time_s: int = field(default_factory=lambda: random.randint(5, 18))
    category: str = field(default_factory=lambda: random.choice("ABCXYZ"))


if __name__ == '__main__':
    data = list(Job().__dict__ for _ in range(300))
    with open(file="sequencing.json", mode="w", encoding="utf-8") as seq_json:
        json.dump(obj=data, fp=seq_json)
