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
    stack: list[tuple[int, int]] = []

    for y in range(height):
        for x in (0, width - 1):
            if filled_grid[y][x] == 0:
                filled_grid[y][x] = -1
                stack.append((y, x))

    for x in range(width):
        for y in (0, height - 1):
            if filled_grid[y][x] == 0:
                filled_grid[y][x] = -1
                stack.append((y, x))

    while stack:
        y, x = stack.pop()
        if y > 0 and filled_grid[y - 1][x] == 0:
            filled_grid[y - 1][x] = -1
            stack.append((y - 1, x))
        if y + 1 < height and filled_grid[y + 1][x] == 0:
            filled_grid[y + 1][x] = -1
            stack.append((y + 1, x))
        if x > 0 and filled_grid[y][x - 1] == 0:
            filled_grid[y][x - 1] = -1
            stack.append((y, x - 1))
        if x + 1 < width and filled_grid[y][x + 1] == 0:
            filled_grid[y][x + 1] = -1
            stack.append((y, x + 1))

    for row in filled_grid:
        for x, value in enumerate(row):
            if value == 0:
                row[x] = 4
            elif value == -1:
                row[x] = 0

    return filled_grid


def function(target_data: list[TaskData] | list[dict]) -> list[Grid]:
    """Run prediction for each input grid."""
    return [
        fill_enclosed_area(task.input if isinstance(task, TaskData) else task["input"])
        for task in target_data
    ]


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    """Run prediction for each input grid in the request body."""
    return PredictionResponse(predict=function(request.root))
