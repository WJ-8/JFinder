import json
import os

dataset_name = "CWE789"
address = f"../data/raw/{dataset_name}/"

dataset = []

n = 0


def del_file(path):
    ls = os.listdir(path)
    for q in ls:
        c_path = os.path.join(path, q)
        if os.path.isdir(c_path):  # 如果是文件夹那么递归调用一下
            del_file(c_path)
        else:  # 如果是一个文件那么直接删除
            os.remove(c_path)
    print('文件已经清空完成')

for dir in range(1,4): #看着s的顺序来改
    filenames = os.listdir(address+f"s0{dir}/")
    for name in filenames:
        if name.split(".")[1] == "java" and "_" in name:
            with open(address+f"s0{dir}/" + name, "r") as f:
                fun = f.readlines()
                flag = -1  # 0是没有漏洞，1是有漏洞
            left = 0
            right = 0
            symbol = 0
            for i in fun:
                if "public class" in i:
                    class_name = i + "{"  # 类名
                if "private void goodG" in i:
                    good_code = ""
                    flag = 0
                    symbol = 1
                elif "public void bad(" in i:
                    bad_code = ""
                    flag = 1
                    symbol = 1
                if flag == 0:
                    if "{" in i:
                        good_code += i
                        left += 1
                    elif "}" in i:
                        good_code += i
                        right += 1
                    else:
                        good_code += i
                elif flag == 1:
                    if "{" in i:
                        bad_code += i
                        left += 1
                    elif "}" in i:
                        bad_code += i
                        right += 1
                    else:
                        bad_code += i
                if right == left and flag != -1:
                    if symbol == 1:
                        symbol = 0
                        continue
                    else:
                        if flag == 0:
                            dataset.append(json.dumps({"func": class_name + good_code + "}", "target": 0}))
                        else:
                            dataset.append(json.dumps({"func": class_name + bad_code + "}", "target": 1}))
                        flag = -1
                        right = left = 0
with open(f"../data/dataset/{dataset_name}.jsonl", "w") as f:
    f.write('\n'.join(dataset))

with open(f"../data/dataset/{dataset_name}.jsonl", "r") as f:
    data = f.readlines()
del_file("../data/slice/")
for i in data:
    with open(f"../data/slice/{n}.java", "w",encoding="utf8") as f:
        f.write(json.loads(i)["func"])
        n += 1
print("数据集切割完成")
