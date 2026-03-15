import argparse
import json
import timeit

import draw
import function


if __name__ == "__main__":
    loop = 1000

    parser = argparse.ArgumentParser()
    parser.add_argument("--draw", help="draw figures", default=False)
    args = parser.parse_args()

    file_path = "train.json"

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    target_data = data.get("train", [])
    predict = function.function(target_data)

    output = [data_i.get("output", []) for data_i in target_data]

    if predict == output:
        print("Correct")
    else:
        print("Incorrect")

    if args.draw:
        for i, predict_i in enumerate(predict):
            draw.draw_map(predict_i, i)

    result = timeit.timeit("function.function(target_data)", globals=globals(), number=loop)
    print(f"Processing time: {(result / loop) * 1000000} us")
