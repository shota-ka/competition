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

    filled_grid = [row[:] for row in grid]
    height = len(filled_grid)
    width = len(filled_grid[0])
    last_y = height - 1
    last_x = width - 1
    stack: list[tuple[int, int]] = []
    push = stack.append
    pop = stack.pop

    for y, row in enumerate(filled_grid):
        if row[0] == 0:
            row[0] = -1
            push((y, 0))
        if last_x and row[last_x] == 0:
            row[last_x] = -1
            push((y, last_x))

    top_row = filled_grid[0]
    if last_y:
        bottom_row = filled_grid[last_y]
        for x in range(width):
            if top_row[x] == 0:
                top_row[x] = -1
                push((0, x))
            if bottom_row[x] == 0:
                bottom_row[x] = -1
                push((last_y, x))
    else:
        for x in range(width):
            if top_row[x] == 0:
                top_row[x] = -1
                push((0, x))

    while stack:
        y, x = pop()
        if y > 0 and filled_grid[y - 1][x] == 0:
            filled_grid[y - 1][x] = -1
            push((y - 1, x))
        if y < last_y and filled_grid[y + 1][x] == 0:
            filled_grid[y + 1][x] = -1
            push((y + 1, x))

        row = filled_grid[y]
        if x > 0 and row[x - 1] == 0:
            row[x - 1] = -1
            push((y, x - 1))
        if x < last_x and row[x + 1] == 0:
            row[x + 1] = -1
            push((y, x + 1))

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
