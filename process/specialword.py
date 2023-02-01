import jsonlines
from nltk import word_tokenize
from transformers import RobertaTokenizer

f_labels = []
f_codes = []
codes = []
project_name = "test"
f = open(f"../data/dataset/{project_name}.jsonl", 'r')

for item in jsonlines.Reader(f):
    f_codes.append(item['func'])
# #加载模型
tokenizer = RobertaTokenizer.from_pretrained("pls_model")

# 获取特殊词列表
count = 0
special_tokens_set = set([])
for f_code in f_codes:
    tokens = word_tokenize(f_code)
    print("这是第%d个代码" % count)
    for token in tokens:
        tokens_ids = tokenizer.convert_tokens_to_ids(token)
        if tokens_ids == 3:
            special_tokens_set.add(token)
    count = count + 1
special_tokens_list = list(special_tokens_set)
# 将special_tokens_list写入文本
f = open("../data/dataset/special_tokens_list.txt", 'w')
f.writelines(" ".join(str(i) for i in special_tokens_list))
f.close()
