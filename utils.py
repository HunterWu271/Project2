import json
import os 
from ArticutAPI import Articut 

MonExcRoot = os.path.dirname(__file__)
with open(f"{MonExcRoot}/account.info") as f:
    account = json.load(f)

articut_lv3 = Articut(username=account['username'], apikey=account['api_key'],
                      level="lv3", version="v270")
