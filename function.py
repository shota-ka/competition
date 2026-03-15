from fastapi import FastAPI
from pydantic import BaseModel, field_validator, ValidationError
from typing import List
from collections import deque

app = FastAPI()

class PredictionResponse(BaseModel):
    predict: List[List[List[int]]]

    @field_validator('predict')
    @classmethod
    def check_not_empty(cls, v):
        if not v:
            raise ValueError("predict must contain at least one element.")
        return v

@app.post("/predict")
def function(target_data):

    """
    Args:
        - "input": 画像の 2次元リスト (高さ H × 幅 W)。
            例: [[pixel, pixel, ...], [pixel, pixel, ...]]
            ※ pixelには、0, 3(壁) が入ります
        - "output": 目的値(inputと同じ型) ※答え確認用

    Returns:
        predict_result: 予測結果のリスト。予測結果(inputと同じ型)を順番に格納
        ※塗りつぶす位置で、inputの0を4に変更
    """
    
    predict_result = []
    for data_i in target_data:
        input = data_i.get('input', []) 
        # output = data_i.get('output', []) 

        if not input or not input[0]:
            predict_result.append(input)
            continue

        height = len(input)
        width = len(input[0])
        predict = [row[:] for row in input]
        outside = [[False] * width for _ in range(height)]
        queue = deque()

        for y in range(height):
            for x in (0, width - 1):
                if predict[y][x] == 0 and not outside[y][x]:
                    outside[y][x] = True
                    queue.append((y, x))

        for x in range(width):
            for y in (0, height - 1):
                if predict[y][x] == 0 and not outside[y][x]:
                    outside[y][x] = True
                    queue.append((y, x))

        while queue:
            y, x = queue.popleft()
            for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if 0 <= ny < height and 0 <= nx < width and predict[ny][nx] == 0 and not outside[ny][nx]:
                    outside[ny][nx] = True
                    queue.append((ny, nx))

        for y in range(height):
            for x in range(width):
                if predict[y][x] == 0 and not outside[y][x]:
                    predict[y][x] = 4

        predict_result.append(predict)

    # predict_resultの型チェックが必要な方はコメントアウト
    # try:
    #     validated_data = PredictionResponse(predict=predict_result)
    # except ValidationError as e:
    #     print("【predict_resultの型が違います】")
    #     raise e
    
    return predict_result
