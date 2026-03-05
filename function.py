from fastapi import FastAPI
from pydantic import BaseModel, field_validator, ValidationError
from typing import List

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

        #ここを記入

    # predict_resultの型チェックが必要な方はコメントアウト
    # try:
    #     validated_data = PredictionResponse(predict=predict_result)
    # except ValidationError as e:
    #     print("【predict_resultの型が違います】")
    #     raise e
    
    return predict_result
