from pandas.core.indexes.category import contains
import requests
import pandas as pd

#bearer = "AAAAAAAAAAAAAAAAAAAAAK2q5QEAAAAAK%2BtSs7%2FdAtLyeZi6MJJLFOF3LI4%3DZhdJh56xrBp2mDfA42VCRzfeNNvcQtcaIJfaQ6ox2vqDZwbRYj"
bearer = "AAAAAAAAAAAAAAAAAAAAAFLg5QEAAAAAKTHSaWyIDCCNFxb5vFvCln7SWL4%3DtS0QK6xyXuSEguuGdpbwrssEAPiz88p1w7QeTEg6MXYe2Qp1V7"
headers = {"Authorization": f"Bearer {bearer}"}
#query = '("Carlos Manzo" OR @CarlosManzo) lang:es -is:retweet'
queries = [
    '("Carlos Manzo" OR @CarlosManzo) lang:es -is:retweet',
    '("Instituto Tecnologico de Morelia" OR #tecnmorelia OR #tecnm OR #tecmorelia) lang:es -is:retweet',
    '("GeneracionZ") lang:es -is:retweet'
]

for query in queries:
    url = f"https://api.x.com/2/tweets/search/all?query={query}&max_results=10&tweet.fields=created_at,author_id"

    r = requests.get(url, headers=headers)
    data = r.json()
    print(data)

    name = query[2:query.find('"', 2, len(query)-1)]
    if ' ' in name:
        name = name.replace(" ", "_")
    name = name.lower()
    #print(name)

    tweets = [[t["id"], t["created_at"], t["text"]] for t in data["data"]]
    df = pd.DataFrame(tweets, columns=["id", "fecha", "texto"])
    df.to_csv(f"./corpus/corpus_{name}.csv", index=False, encoding="utf-8")
