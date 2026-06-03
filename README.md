```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Engineer:
    """An AI engineer who ships."""

    name:     str = "Lakshmi Indugapalli"
    role:     str = "AI Engineer"
    based_in: str = "Bangalore, IN"

    works_on: tuple[str, ...] = (
        "vision-language models in production",
        "multi-agent coordination infrastructure",
        "reinforcement learning environments",
        "retrieval & generative pipelines",
    )

    stack: tuple[str, ...] = (
        "python  ·  go  ·  typescript",
        "pytorch  ·  cuda  ·  vllm  ·  flash-attn",
        "fastapi  ·  postgres  ·  nats  ·  docker",
        "ruff  ·  mypy --strict  ·  pytest",
    )

    believes: str = "Long horizon. Short sprints."


me = Engineer()
```

<sub>
<a href="https://medium.com/@indugapallignaneswara">writing</a>
&nbsp;·&nbsp;
<a href="https://ieeexplore.ieee.org/document/10958937/">paper</a>
&nbsp;·&nbsp;
<a href="https://www.kaggle.com/competitions/dishcovery-mission-ii-cvpr-2026/discussion/702130">kaggle</a>
&nbsp;·&nbsp;
<a href="https://www.linkedin.com/in/gnaneswara-indugapalli-367924252/">linkedin</a>
</sub>
