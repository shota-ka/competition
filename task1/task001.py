import json
import draw

###################
file_path = "task001.json"
data_type = 'train'
###################

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

target_data = data.get(data_type, [])
for d, (data_i) in enumerate(target_data):
    input = data_i.get('input', [])
    output = data_i.get('output', [])
    matrix = [[0 for _ in range(9)] for _ in range(9)]
    number = max(max(input))
    for i in range(9):
        for j in range(9):
            if (input[i//3][j//3] == number):
                matrix[i][j] = input[i%3][j%3]
    print(matrix == output)
    draw.draw_map(matrix, d)