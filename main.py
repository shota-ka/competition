import function
import json
import argparse
import draw

if __name__ == '__main__':

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

    print(predict == output)

    if (args.draw):
        for i, (predict_i) in enumerate(predict):
            draw.draw_map(predict_i, i)
