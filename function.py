from typing import TypeAlias

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, RootModel

app = FastAPI()

Grid: TypeAlias = list[list[int]]
NUMPY_FILL_THRESHOLD = 64 * 64


class TaskData(BaseModel):
    input: Grid
    output: Grid | None = None


class PredictionRequest(RootModel[list[TaskData]]):
    pass


class PredictionResponse(BaseModel):
    predict: list[Grid]


def _fill_enclosed_area_python(grid: Grid) -> Grid:
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


def _fill_enclosed_area_numpy(grid: Grid) -> Grid:
    if not grid or not grid[0]:
        return grid

    filled_grid = np.array(grid, dtype=np.int8, copy=True)
    zeros = filled_grid == 0
    outside = np.zeros_like(zeros)

    outside[0, :] |= zeros[0, :]
    outside[-1, :] |= zeros[-1, :]
    outside[:, 0] |= zeros[:, 0]
    outside[:, -1] |= zeros[:, -1]

    while True:
        neighbors = np.zeros_like(outside)
        neighbors[1:, :] |= outside[:-1, :]
        neighbors[:-1, :] |= outside[1:, :]
        neighbors[:, 1:] |= outside[:, :-1]
        neighbors[:, :-1] |= outside[:, 1:]

        new_outside = zeros & neighbors & ~outside
        if not new_outside.any():
            break
        outside |= new_outside

    filled_grid[zeros & ~outside] = 4
    return filled_grid.tolist()


def fill_enclosed_area(grid: Grid) -> Grid:
    """Replace enclosed zeros with 4."""
    if not grid or not grid[0]:
        return grid

    if len(grid) * len(grid[0]) >= NUMPY_FILL_THRESHOLD:
        return _fill_enclosed_area_numpy(grid)
    return _fill_enclosed_area_python(grid)


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
