from exa_py import Exa
from datetime import date
import requests
import json

def exa_search(query):
    print('搜索:' + query)
    exa = Exa(api_key="your_exa_api_key")

    result = exa.search_and_contents(
    query,
    type="keyword",
    num_results=10,
    text=True
    )

    content = '今天日期是：' + str(date.today()) + '\n' + '---' + '\n'
    for i in result.results:
        content += '信息来源：' + i.title + '\n'
        content += '信息内容：' + i.text[:200] + '\n'
        content += '---' + '\n'
    return content

def web_search_reply(query):
    content = exa_search(query)
    prompt =f'''你是一名信息整理助手。\n
               根据接下来提供的搜索结果，回答用户的问题。\n
               问题：{query}\n
               搜索结果：{content}\n
               回答：
            '''
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": "llama3.1:8b-instruct-q8_0",
        "prompt": prompt,
        "stream": False
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers, stream=False)

    if response.status_code == 200:
        return response.json()['response']
    else:
        return f"Request failed with status {response.status_code}"
    
if __name__ == "__main__":
    result = exa_search("今天天气怎么样？")
    print(result)