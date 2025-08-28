import json
import draw

###################
file_path = "task002.json"
data_type = 'test'
###################

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

target_data = data.get(data_type, [])
for d, (data_i) in enumerate(target_data):
    input = data_i.get('input', [])
    output = data_i.get('output', [])
    size = len(input)
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    number = max(max(input))
    matrix_pre = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if (input[i][j]==3):
                    matrix[i][j] = 3

    for i in range(size):
        for j in range(size):
            if (input[i][j]==0):
                s = 0
                if (i != 0):
                    s += min([matrix[i-1][j],1])
                if (j != size-1):
                    s += min([matrix[i][j+1],1])
                if (i != size-1):
                    s += min([matrix[i+1][j],1])
                if (j != 0):
                    s += min([matrix[i-1][j-1],1])
                if (s >= 2):
                    matrix[i][j] = 4
    check = 0
    s_pre = 0
    check_switch=0
    while(check == 0):
        for i in range(size):
            for j in range(size):
                if (matrix[i][j]==4):
                    switch = 0
                    count = 1
                    while (switch == 0):
                        if (i-count >= 0):
                            if (matrix[i-count][j]==0):
                                switch = 2
                            elif (matrix[i-count][j]==3):
                                switch = 1
                            else:
                                count +=1
                        else:
                            switch = 2
                    if (switch == 1):
                        switch = 0
                        count = 1
                        while (switch == 0):
                            if (j+count <= size-1):
                                if (matrix[i][j+count]==0):
                                    switch = 2
                                elif (matrix[i][j+count]==3):
                                    switch = 1
                                else:
                                    count +=1
                            else:
                                switch = 2
                        if (switch == 1):
                            switch = 0
                            count = 1
                            while (switch == 0):
                                if (i+count <= size-1):
                                    if (matrix[i+count][j]==0):
                                        switch = 2
                                    elif (matrix[i+count][j]==3):
                                        switch = 1
                                    else:
                                        count +=1
                                else:
                                    switch = 2
                            if (switch == 1):
                                switch = 0
                                count = 1
                                while (switch == 0):
                                    if (j-count >= 0):
                                        if (matrix[i][j-count]==0):
                                            switch = 2
                                        elif (matrix[i][j-count]==3):
                                            switch = 1
                                        else:
                                            count +=1
                                    else:
                                        switch = 2
                                if (switch == 1):
                                    matrix[i][j] = 4
                                else:
                                    matrix[i][j] = 0  
                            else:
                                matrix[i][j] = 0
                        else:
                            matrix[i][j] = 0
                    else:
                        matrix[i][j] = 0
        s = 0
        for i in range(size):
            for j in range(size):
                s += matrix[i][j]
        print(s)
        if (check_switch != 0):
            if (s_pre == s):
                check = 1
        else:
            check_switch = 1
        s_pre = s


    print(matrix == output)
    draw.draw_map(matrix, d)