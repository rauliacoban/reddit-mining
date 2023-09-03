import praw
import pandas as pd
import jsonlines

client_id = 'sIXZTihLNiKiHw'
client_secret = 'EjfAsmz5z8mDbZohe4UPYTPIZsYmOQ'
user_agent = 'Test1'

infile = "worldnews.jsonl"
outfile = "sorted.csv"

REFERENCE_TIMESTAMP = 1694062800

def postsToCSV(posts, filename):
    posts.to_csv(filename, index=False)

def postsFromNDJSON(filename):
    posts = []
    with jsonlines.open(filename) as reader:
        for line in reader:
            line = line["Item"]
            posts.append([line["created"]["S"], line["title"]["S"], line["id"]["S"]])
    posts = pd.DataFrame(posts,columns=['created', 'title', 'id'])

    return posts

def sortByTime(data):
    data = data.sort_values(by='created')
    return data

if __name__ == "__main__":
    posts = postsFromNDJSON(infile)
    posts = sortByTime(posts)
    postsToCSV(posts=posts, filename=outfile)
    print(posts)



