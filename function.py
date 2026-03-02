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
def function(data: dict):

    """
    Args:
        data (dict): 以下の構造を持つ辞書:
            - "train": データのリスト。各要素は辞書。
                - "input": 画像の 2次元リスト (高さ H × 幅 W)。
                           例: [[pixel, pixel, ...], [pixel, pixel, ...]]
                - "output": 目的値(inputと同じ型) ※答え確認用

    Returns:
        predict_result: 予測結果のリスト。予測結果(inputと同じ型)を順番に格納
    """

    target_data = data.get("train", [])
    predict_result = []
    for data_i in target_data:
        input = data_i.get('input', []) 
        # output = data_i.get('output', []) 

        #ここを記入

    try:
        validated_data = PredictionResponse(predict=predict_result)
    except ValidationError as e:
        print("【predict_resultの型が違います】")
        raise e
    
    return predict_result
