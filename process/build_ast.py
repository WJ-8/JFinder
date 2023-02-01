import os

import numpy as np

address = "../data/slice/"
filenames = os.listdir(address)
max = 0
mark = 0
for i in filenames:
    if int(i.split(".")[0]) > max:
        max = int(i.split(".")[0])
for i in range(max + 1):
    print(i)
    test = []
    with open(f"../data/slice/{i}.java.dot.txt") as f:
        data = f.readlines()
    arrays = np.zeros((200, 200))
    for q in data:
        sor, des = map(int, q.replace("\n", "").split(","))
        if sor < 200 and des < 200:
            arrays[sor][des] = 1
        else:
            break
    arrays = np.expand_dims(arrays, axis=0)
    if mark == 0:
        ast = arrays
        mark = 1
    else:
        ast = np.concatenate([ast, arrays], axis=0)
# 切分数据集

np.save("../data/dataset/ast.npy", ast)
print(ast.shape)
