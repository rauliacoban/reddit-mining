from pmaw import PushshiftAPI
import pandas as pd
import praw

client_id = 'sIXZTihLNiKiHw'
client_secret = 'EjfAsmz5z8mDbZohe4UPYTPIZsYmOQ'
user_agent = 'Test1'

infile = "data.csv"
outfile = "sorted.csv"

REFERENCE_TIMESTAMP = 1694062800

now = 1693511720

def downloadPosts(filename):
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, check_for_async=False)
    posts_raw = reddit.subreddit('worldnews').top(limit=10000, time_filter="year")
    posts = []
    for post_raw in posts_raw:
        posts.append([post_raw.title, post_raw.created, post_raw.upvote_ratio, post_raw.ups])
    posts = pd.DataFrame(posts,columns=['title', 'utc', 'ratio', 'upvotes'])
    return posts

def postsToCSV(posts, filename):
    posts.to_csv(filename, index=False)

def postsFromCSV(filename):
    posts = pd.read_csv(filename)
    return posts

def sortByTime(data):
    data = data.sort_values(by='utc')
    return data

if __name__ == "__main__":
    api = PushshiftAPI()
    posts = api.search_submissions(subreddit="science", limit=1000)
    post_list = [post for post in posts]
    print(post_list)


