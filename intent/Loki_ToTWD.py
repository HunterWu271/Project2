#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for ToTWD

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
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_ToTWD.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

intentPth = os.path.dirname(__file__)
userDefinedPth = f"{intentPth}/USER_DEFINED.json"

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG:
        print("[ToTWD] {} ===> {}".format(inputSTR, utterance))

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    if utterance == "5000塊日元可以換多少元台幣":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if args[18] == '台幣':
                resultDICT['source'].append(args[3])
                numDICT = articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
                resultDICT['amount'].append(numDICT['number'][args[0]])

    if utterance == "5000塊瑞士法朗可以換多少元台幣":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if args[17] == '台幣':
                resultDICT['source'].append(args[3])
                numDICT = articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
                resultDICT['amount'].append(numDICT['number'][args[0]])

    if utterance == "5000塊韓元可以換台幣多少元":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if args[12] == '台幣':
                resultDICT['source'].append(args[3])
                numDICT = articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
                resultDICT['amount'].append(numDICT['number'][args[0]])

    if utterance == "5000瑞士法朗可以換多少元台幣":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if args[17] == '台幣':
                resultDICT['source'].append(args[0])
                numDICT = articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
                resultDICT['amount'].append(numDICT['number'][args[0]])

    if utterance == "5000美金可以換多少元台幣":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if args[13] == '台幣':
                numDICT= articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
                resultDICT['source'].append(numDICT['unit'][args[0]])
                resultDICT['amount'].append(numDICT['number'][args[0]])

    if utterance == "5000韓元可以換台幣多少元":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if args[7] == "台幣":
                numDICT = articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
                resultDICT['source'].append(numDICT['unit'][args[0]])
                resultDICT['amount'].append(numDICT['number'][args[0]])            
    
    resultDICT['target'].append('台幣')

    return resultDICT