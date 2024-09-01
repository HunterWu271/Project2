#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
import os
import re
import pandas as pd
from datetime import datetime
from MoneyExchange import runLoki
#from pprint import pprint


logging.basicConfig(level=logging.DEBUG)

path = os.path.dirname(__file__)
exchangeRateDF = pd.read_csv(f'{path}/2024-08-01_ExchangeRate.csv', index_col = 0)

punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
def getLokiResult(inputSTR):
    punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    inputLIST = punctuationPat.sub("\n", inputSTR).split("\n")
    filterLIST = []

    # 這裹要多加一個refDICT，因為現在的作法，需要先設好
    # 字典中的key及empty list值。
    refDICT = {'source':[], 'target':[], 'amount':[]}
    # 下面也得加入refDICT
    resultDICT = runLoki(inputLIST, filterLIST=filterLIST, refDICT=refDICT)
    logging.debug("Loki Result => {}".format(resultDICT))
    return resultDICT

class BotClient(discord.Client):

    def resetMSCwith(self, messageAuthorID):
        '''
        清空與 messageAuthorID 之間的對話記錄
        '''

        # 113.08.01 現在的作法，得先在templateDICT中把要
        # 用到的key及其empty list的值
        templateDICT = {    "id": messageAuthorID,
                             "updatetime" : datetime.now(),
                             "latestQuest": "",
                             "false_count" : 0,
                             "source":[],
                             "target":[],
                             "amount":[],
        }
        return templateDICT

    async def on_ready(self):
        # ################### Multi-Session Conversation :設定多輪對話資訊 ###################
        self.templateDICT = {"updatetime" : None,
                             "latestQuest": ""
        }
        self.mscDICT = { #userid:templateDICT
        }
        # ####################################################################################
        print('Logged on as {} with id {}'.format(self.user, self.user.id))

    async def on_message(self, message):
        # Don't respond to bot itself. Or it would create a non-stop loop.
        # 如果訊息來自 bot 自己，就不要處理，直接回覆 None。不然會 Bot 會自問自答個不停。
        if message.author == self.user:
            return None

        logging.debug("收到來自 {} 的訊息".format(message.author))
        logging.debug("訊息內容是 {}。".format(message.content))
        if self.user.mentioned_in(message):
            replySTR = "我是預設的回應字串…你會看到我這串字，肯定是出了什麼錯！"
            logging.debug("本 bot 被叫到了！")
            msgSTR = message.content.replace("<@{}> ".format(self.user.id), "").strip()
            logging.debug("人類說：{}".format(msgSTR))
            if msgSTR == "ping":
                replySTR = "pong"
            elif msgSTR == "ping ping":
                replySTR = "pong pong"

# ##########初次對話：這裡是 keyword trigger 的。
            elif msgSTR.lower() in ["哈囉","嗨","你好","您好","hi","hello"]:
                #有講過話(判斷對話時間差)
                if message.author.id in self.mscDICT.keys():
                    timeDIFF = datetime.now() - self.mscDICT[message.author.id]["updatetime"]
                    #有講過話，但與上次差超過 5 分鐘(視為沒有講過話，刷新template)
                    if timeDIFF.total_seconds() >= 300:
                        self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)
                        replySTR = "嗨嗨，我們好像見過面，但卓騰的隱私政策不允許我記得你的資料，抱歉！"
                    #有講過話，而且還沒超過5分鐘就又跟我 hello (就繼續上次的對話)
                    else:
                        replySTR = self.mscDICT[message.author.id]["latestQuest"]
                #沒有講過話(給他一個新的template)
                else:
                    self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)
                    replySTR = msgSTR.title()

# ##########非初次對話：這裡用 Loki 計算語意
            else: #開始處理正式對話
                #從這裡開始接上 NLU 模型
                resultDICT = getLokiResult(msgSTR)

                # 因為 self.mscDICT[message.author.id]中的幾個關鍵字的值都是表列
                # 故用 .extend() 的方式
                self.mscDICT[message.author.id]['source'].extend(resultDICT['source'])
                self.mscDICT[message.author.id]['target'].extend(resultDICT['target'])
                self.mscDICT[message.author.id]['amount'].extend(resultDICT['amount'])
                print()
                # print(self.mscDICT[message.author.id])
                # 因為這些關鍵字的值都是list，故使用索引來取得真正的值
                if self.mscDICT[message.author.id]['source'][0] == '台幣':
                    amount = self.mscDICT[message.author.id]['amount'][0]
                    target = self.mscDICT[message.author.id]['target'][0]
                    rate = float(exchangeRateDF.at[target, exchangeRateDF.columns[3]])
                    resAmount = round(amount/rate, 2)
                    replySTR = f"{amount}元台幣可以兌換{resAmount}{target}。"
                elif self.mscDICT[message.author.id]['target'][0] == '台幣':
                    amount = self.mscDICT[message.author.id]['amount'][0]
                    source = self.mscDICT[message.author.id]['source'][0]
                    rate = float(exchangeRateDF.at[source, exchangeRateDF.columns[3]])
                    resAmount = round(amount*rate, 2)
                    replySTR = f"{amount}元{source}可以兌換{resAmount}台幣。"
                else:
                    amount = self.mscDICT[message.author.id]['amount'][0]
                    target = self.mscDICT[message.author.id]['target'][0]
                    source = self.mscDICT[message.author.id]['source'][0]
                    rateTarget = float(exchangeRateDF.at[target, exchangeRateDF.columns[3]])
                    rateSource = float(exchangeRateDF.at[source, exchangeRateDF.columns[3]])
                    interAmount = round(amount*rateSource, 2)
                    resAmount = round(interAmount/rateTarget, 2)
                    replySTR = f"{amount}元{source}可以兌換{resAmount}{target}。"

                logging.debug("######\nLoki 處理結果如下：")
                logging.debug(resultDICT)
            await message.reply(replySTR)
            # 上面做完，清空資訊，以免前次的資訊殘留
            self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id) 


if __name__ == "__main__":
    with open("account.info", encoding="utf-8") as f: #讀取account.info
        accountDICT = json.loads(f.read())
    client = BotClient(intents=discord.Intents.default())
    client.run(accountDICT["discord_token"])
