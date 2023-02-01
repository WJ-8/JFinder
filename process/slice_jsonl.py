import os
import json
import random
dataset_name = "test"
n = 0

with open(f"../data/dataset/{dataset_name}.jsonl", "r",encoding="utf8") as f:
    data = f.readlines()
random.shuffle(data)

with open(f"../data/dataset/{dataset_name}.jsonl", "w",encoding="utf8") as f:
    for i in data:
        f.write(i)

def del_file(path):
    ls = os.listdir(path)
    for q in ls:
        c_path = os.path.join(path, q)
        if os.path.isdir(c_path):  # 如果是文件夹那么递归调用一下
            del_file(c_path)
        else:  # 如果是一个文件那么直接删除
            os.remove(c_path)
    print('文件已经清空完成')

del_file("../data/slice/")
for i in data:
    with open(f"../data/slice/{n}.java", "w") as f:
        f.write(json.loads(i)["func"])
        n += 1
print("数据集切割完成")