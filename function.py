from collections import deque
from typing import TypeAlias

from fastapi import FastAPI
from pydantic import BaseModel, RootModel

app = FastAPI()

Grid: TypeAlias = list[list[int]]


class TaskData(BaseModel):
    input: Grid
    output: Grid | None = None


class PredictionRequest(RootModel[list[TaskData]]):
    pass


class PredictionResponse(BaseModel):
    predict: list[Grid]


def fill_enclosed_area(grid: Grid) -> Grid:
    """Replace enclosed zeros with 4."""
    if not grid or not grid[0]:
        return grid

    height = len(grid)
    width = len(grid[0])
    filled_grid = [row[:] for row in grid]
    outside = [[False] * width for _ in range(height)]
    queue = deque[tuple[int, int]]()

    for y in range(height):
        for x in (0, width - 1):
            if filled_grid[y][x] == 0 and not outside[y][x]:
                outside[y][x] = True
                queue.append((y, x))

    for x in range(width):
        for y in (0, height - 1):
            if filled_grid[y][x] == 0 and not outside[y][x]:
                outside[y][x] = True
                queue.append((y, x))

    while queue:
        y, x = queue.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < height and 0 <= nx < width and filled_grid[ny][nx] == 0 and not outside[ny][nx]:
                outside[ny][nx] = True
                queue.append((ny, nx))

    for y in range(height):
        for x in range(width):
            if filled_grid[y][x] == 0 and not outside[y][x]:
                filled_grid[y][x] = 4

    return filled_grid


def function(target_data: list[TaskData] | list[dict]) -> list[Grid]:
    """Run prediction for each input grid."""
    tasks = [task if isinstance(task, TaskData) else TaskData.model_validate(task) for task in target_data]
    return [fill_enclosed_area(task.input) for task in tasks]


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    """Run prediction for each input grid in the request body."""
    return PredictionResponse(predict=function(request.root))
