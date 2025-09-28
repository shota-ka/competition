import function
import json
import argparse
import draw
import timeit

if __name__ == '__main__':

    ######
    loop = 1000
    ######

    parser = argparse.ArgumentParser()
    parser.add_argument("--draw", help="draw figures", default=False)
    args = parser.parse_args()

    file_path = "train.json"

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    predict = function.function(data)

    target_data = data.get("train", [])
    output = []
    for d, (data_i) in enumerate(target_data):
        output.append(data_i.get('output', []))
    
    if (predict == output):
        print("正解")
    else:
        print("不正解")

    if (args.draw):
        for i, (predict_i) in enumerate(predict):
            draw.draw_map(predict_i, i)
    
    result =  timeit.timeit('function.function(data)', globals=globals(), number=loop)
    print(f"処理時間: {(result/loop)*1000000}µs")
