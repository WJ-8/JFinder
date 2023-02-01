import json
import os

project_name = "test"
cnt = 0


def del_file(path):
    ls = os.listdir(path)
    for q in ls:
        c_path = os.path.join(path, q)
        if os.path.isdir(c_path):  # 如果是文件夹那么递归调用一下
            del_file(c_path)
        else:  # 如果是一个文件那么直接删除
            os.remove(c_path)
    print('文件已经清空完成')


with open(f"../data/dataset/{project_name}.jsonl", 'r') as f:
    c = f.readlines()

# 对多个jsonl文件合并
# with open("E:\\magic-cb\\data\\raw\\qemu\\train.jsonl",'r')as k:
#     c+=k.readlines()
# with open("E:\\magic-cb\\data\\raw\\qemu\\valid.jsonl", 'r') as m:
#     c += m.readlines()
#     with open("F:\\zsw\\ffqejson\\qemu.jsonl",'w')as m:
#         for i in c:
#             cnt+=1
#             m.write(i)

# 对单个jsonl的提取
del_file("../data/pls_slice")
for i in c:
    with open("../data/pls_slice/" + str(cnt) + ".java", 'w') as m:
        cnt += 1
        text = json.loads(i)["func"].replace("\n", "")
        m.write(text)

print(cnt)
