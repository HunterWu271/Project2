#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Others

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict,
        refDICT       dict,
        pattern       str

    Output:
        resultDICT    dict
"""
from utils import articut_lv3
from random import sample
import json
import os

DEBUG = True
CHATBOT_MODE = False

userDefinedDICT = {}
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except Exception as e:
    print("[ERROR] userDefinedDICT => {}".format(str(e)))

responseDICT = {}
if CHATBOT_MODE:
    try:
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_Others.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

intentPth = os.path.dirname(__file__)
userDefinedPth = f"{intentPth}/USER_DEFINED.json"

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG:
        print("[Others] {} ===> {}".format(inputSTR, utterance))

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    if utterance == "60000塊瑞士法郎可以換多少元美金":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            source = args[3]
            target = args[18]
            if source != '台幣' and target != '台幣':
                resultDICT['source'].append(source)
                resultDICT['target'].append(target)
                numDICT = articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
                resultDICT['amount'].append(numDICT['number'][args[0]])

    if utterance == "6000元美金可以換多少元日幣":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            source = args[3]
            target = args[18]
            
            if source != '台幣' and target != '台幣':
                resultDICT['source'].append(source)
                resultDICT['target'].append(target)
                numDICT = articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
                resultDICT['amount'].append(numDICT['number'][args[0]])

    if utterance == "6000美金可以換多少元日幣":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            target = args[13]
            numDICT = articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
            source = numDICT['unit'][args[0]]
            if source != '台幣' and target != '台幣':
                resultDICT['source'].append(source)
                resultDICT['target'].append(target)
                resultDICT['amount'].append(numDICT['number'][args[0]])

    return resultDICT