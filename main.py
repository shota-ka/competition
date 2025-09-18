import function
import json
import draw

if __name__ == '__main__':

    file_path = "train.json"

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    predict = function.function(data)

    target_data = data.get("train", [])
    output = []
    for d, (data_i) in enumerate(target_data):
        output.append(data_i.get('output', []))

    print(predict == output)
    # draw.draw_map(predict, d)
