import openai
from time import time,sleep
from uuid import uuid4


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


openai.api_key = open_file('openaiapikey.txt')

roles = [
    'agile coach',
    'scrum master',
    'rte',
    'Tech Lead',
    'service train lead',
    'service owner lead',
    'developer',
    'tester',
    "ba",
    "delivery manager"
]


topics = [
    'Advanced Agile Concepts'
]

subtopics = [
    'Agile Manifesto and Principles Revisited',
    'Agile Maturity Models and Assessments',
    'Agile Governance and Compliance',
    'Agile Metrics and Reporting'
]

def gpt3_completion(prompt):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages = [{"role": "system", "content": "Training design lead at a large financial institution"},
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
    for role in roles:
            for topic in topics:
                for subtopic in subtopics:
                    count += 1
                    prompt = open_file('prompt.txt')
                    prompt = prompt.replace('<<ROLE>>', role)
                    prompt = prompt.replace('<<TOPIC>>', topic)
                    prompt = prompt.replace('<<SUBTOPIC>>', subtopic)
                    #prompt = prompt.replace('<<UUID>>', str(uuid4()))
                    print('\n\n', prompt)
                    completion = gpt3_completion(prompt)
                    outprompt = 'Role: %s\nTopic: %s\nSubTopic: %s\n\nLesson Outline: ' % (role, topic, subtopic)
                    filename = (role + "_" + topic + "_" + subtopic).replace(' ','').replace('&','') + '%s.txt' % time()
                    save_file('prompts/%s' % filename, outprompt)
                    save_file('completions/%s' % filename, completion)
                    print('\n\n', outprompt)
                    print('\n\n', completion)
                    if count > 1:
                        exit()
    #print(count)