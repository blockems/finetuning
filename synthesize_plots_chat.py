import openai
from time import time,sleep
from uuid import uuid4

import os
import json

data_dir = "./roles" # replace with the actual directory path
json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

openai.api_key = open_file('openaiapikey.txt')

def gpt3_completion(prompt):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages = [{"role": "system", "content": "Agile coaching and program management expert"},
                            {"role": "user", "content": prompt}
                ]
            )
            print(response)                
            text = response['choices'][0]['message']['content'].strip()
            filename = '%s_gpt3.txt' % time()
            save_file('gtp3_logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    count = 0
    for file in json_files:
        with open(os.path.join(data_dir, file), 'r') as f:
            json_data = json.load(f)
            role = json_data['Role']
            description = json_data['Description']
            skills_required = json_data['Skills']['Required']
            skills_recommended = json_data['Skills']['Recommended']
            for skill in skills_required + skills_recommended:
                skill_name = skill['SkillName']
                skill_level = skill['SkillLevel']
                count += 1
                prompt = open_file('prompt.txt')
                prompt = prompt.replace('<<ROLE>>', role)
                prompt = prompt.replace('<<LEVEL>>', skill_level)
                prompt = prompt.replace('<<SKILL>>', skill_name)
                #prompt = prompt.replace('<<UUID>>', str(uuid4()))
                print('\n\n', prompt)
                
                outprompt = 'Role: %s\nSkill: %s\nSkill level: %s\nRandomness: %s\n\nTask: %s' % (role, skill_name, skill_level,str(uuid4) ,prompt)
                filename = (role + "_" + skill_name + "_" + skill_level).replace(' ','').replace('&','').replace('/','-').replace('\\','_') + '%s.txt' % time()
                save_file('prompts/%s' % filename, outprompt)
                
                completion = gpt3_completion(prompt)
                
                save_file('completions/%s' % filename, completion)
                print('\n\n', outprompt)
                print('\n\n', completion)
                #if count > 1:
                #    exit()