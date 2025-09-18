def function(data):

    target_data = data.get("train", [])
    predict = [] #予測結果を順番に格納
    for data_i in target_data:
        input = data_i.get('input', []) #入力
        output = data_i.get('output', []) # 目的値

    #ここを記入

    return predict