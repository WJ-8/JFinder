import json
import numpy as np
project_name = "CWE789"
y=[]
with open(f"../data/dataset/{project_name}.jsonl", 'r', encoding='utf8') as f:
    c = f.readlines()
    for i in c:
        text = json.loads(i)["target"]
        y.append(int(text))
array_y = np.array(y)
print(array_y.shape)
np.save("../data/dataset/y.npy", array_y)
