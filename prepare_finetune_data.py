import os
import json


src_dir = 'completions/'
prompt_dir = 'prompts/'


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


if __name__ == '__main__':
    files = os.listdir(src_dir)
    data = list()
    for file in files:
        completion = open_file(src_dir + file)
        prompt = open_file(prompt_dir + file)
        info = {'prompt': prompt.replace('Randomness: <function uuid4 at 0x00000204235ED800>\n',''), 'completion': completion}
        data.append(info)
    with open('subjects.jsonl', 'w') as outfile:
        for i in data:
            json.dump(i, outfile)
            outfile.write('\n')