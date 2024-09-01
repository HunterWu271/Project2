#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for fromTWD

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
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_fromTWD.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

intentPth = os.path.dirname(__file__)
userDefinedPth = f"{intentPth}/USER_DEFINED.json"

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG:
        print("[fromTWD] {} ===> {}".format(inputSTR, utterance))

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    if utterance == "30000元台幣可以換多少元美元":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if args[3] == '台幣':
                resultDICT['target'].append(args[18])
                numDICT = articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
                resultDICT['amount'].append(numDICT['number'][args[0]])

    if utterance == "30000台幣可以換多少元美金":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            numDICT = articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
            if numDICT['unit'][args[0]] == '台幣':
                resultDICT['target'].append(args[13])
                resultDICT['amount'].append(numDICT['number'][args[0]])

    if utterance == "30000台幣可以換美金多少元":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            numDICT = articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
            if numDICT['unit'][args[0]] == '台幣':
                resultDICT['target'].append(args[7])
                resultDICT['amount'].append(numDICT['number'][args[0]])

    if utterance == "3000塊台幣可以換新加坡幣多少元":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if args[3] == '台幣':
                resultDICT['target'].append(args[12])
                numDICT = articut_lv3.parse(args[0], userDefinedDictFILE=userDefinedPth)
                resultDICT['amount'].append(numDICT['number'][args[0]])

    resultDICT['source'].append('台幣')

    return resultDICT