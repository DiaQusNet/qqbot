import requests
import json
import os
import base64
import threading
from features.web_search import exa_search

def clean_memory():
    global store
    store = {}

store = {}
def messages_with_id(member_id, group_id, message, ai_message=False, message_remain=4):
    global store
    
    sys_template = '''你是一名ai助手。
                   '''
    sys_message = {"role": "system","content": sys_template}
    #with lock:  # 
    if group_id in store:
        group = store[group_id] #dict
        if member_id in group:
            member_message = group[member_id] #list
            if not ai_message: 
                member_message.append({"role": "user","content": message})
                if len(member_message) == (2*message_remain + 2):
                    del member_message[1]
                    del member_message[1]
                return member_message
            else:
                member_message.append({"role": "assistant","content": message})
            return member_message
        else:
            group[member_id] = [sys_message, {"role": "user","content": message}]
            return group[member_id]
    else:
        store[group_id] = {}
        store[group_id][member_id] = [{"role": "user","content": message}]
        store[group_id][member_id].insert(0, sys_message)
        return store[group_id][member_id]
