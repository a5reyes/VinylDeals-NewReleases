import praw
import re
import string

reddit = praw.Reddit(
    client_id="...",
    client_secret="...",
    user_agent="..."
)

#misc. intro
def main():
    category = input("What are you looking for - Deals or new releases - ")
    get_reddit(category)

#getting posts and their direct links from subreddit
def get_reddit(category, str_limit):
    if category == "deals" or "deal" in category:
        sub = "VinylDeals"
    if category == "releases" or "release" in category:
        sub = "VinylReleases"
    subreddit = reddit.subreddit(sub)
    posts = {}
    expired_posts = {}
    num_limit = int(str_limit)
    for post in subreddit.new(limit=num_limit):
        if "Guidelines" in post.title or "Discussion" in post.title:
            continue
        if "direct" in post.selftext:
            link = post.selftext.split("direct")
            links = link[1].replace("(", "").replace(")", "").replace("]", "")
            direct_link = re.split(r"[*[]", links)
            posts.update({post.title : [direct_link[0], post.url]}) #post.selftext for description w/ directlink
        else:
            posts.update({post.title : [post.selftext, post.url]}) #post.selftext for description
        if "Direct" in post.selftext:
            link = post.selftext.split("Direct")
            links = link[1].replace("(", "").replace(")", "").replace("]", "")
            direct_link = re.split(r"[*[]", links)
            posts.update({post.title : [direct_link[0], post.url]})
        else:
            posts.update({post.title : [post.selftext, post.url]}) 
        #checking if post is expired
        if subreddit == "VinylDeals":
            post_id = post.id
            submission = reddit.submission(id=post_id)
            submission.comments.replace_more(limit=1)
            is_expired = False
            for comment in submission.comments.list():
                if "expired" in comment.body.casefold():
                    is_expired = True
                    expired_posts[post.title] = [direct_link[0], post.url] 
                    break
            if is_expired and post.title in posts:
                del posts[post.title]
    return posts

#formatting results from chosen subreddit
def return_res(records, sub):
    results = []
    for title, des in records.items():
        if sub == "releases":
            if des[0] == "" or not des[0].startswith("https"):
                results.append("- {} - {}".format(title, des[1]))
            else:
                results.append("- {} - {}".format(title, des[0]))
        if sub == "deals":
            if des[0] == "" or not des[0].startswith("https"):
                results.append("- {} - {}".format(title, des[1]))
            else:
                results.append("- {} - {}".format(title, des[0]))
    return [result for result in results]

#sorting choices - by price (ascending or descending)
def sort_prices(vinyls, order):
    deals_prices = []
    for post in vinyls.keys():
        post_str = str(post)
        if "$" in post_str:
            try:
                title, cost = post_str.split("$")
            except (ValueError):
                etc, title, cost = post_str.split("$")
            value = cost.split(" ")
            deal = float(value[0].rstrip(string.punctuation))
            if deal not in deals_prices:
                deals_prices.append(deal)
        else:
            del post
    if order == "descending":
        deals_prices.sort(reverse=True)
    else:
        deals_prices.sort()
    results = []
    for deal in deals_prices:
        for post in vinyls.keys():
            if str(deal) in post:
                ref = vinyls.get(post)
                if ref[0] == "":
                    results.append("- {} - {}".format(post, ref[1]))
                else:
                    results.append("- {} - {}".format(post, ref[0]))
    return [result for result in results]

#sorting choices - by number of lps/records
def num_vinyl(vinyls):
    multi_vinyls = list(vinyls.items())
    results = []
    for vinyl in multi_vinyls:
        pattern = r"\[?[a-zA-Z\s]*\d+(\s?[Xx]?\s?)?LP\s?[a-zA-Z\s]*\]?"
        if re.search(pattern, vinyl[0], re.IGNORECASE):
            if vinyl[1][0] == "":
                results.append("- {} - {}".format(vinyl[0], vinyl[1][1]))
            else:
                results.append("- {} - {}".format(vinyl[0], vinyl[1][0]))
        else:
            continue
    return [result for result in results]

#sorting choices - by size of lp/record
def size_vinyl(vinyls):
    vinyl_sizes = ['7"', '10"', '12"']
    releases = list(vinyls.items())
    results=[]
    for release in releases:
        if any(size in release[0] for size in vinyl_sizes):
            results.append("- {} - {}".format(release[0], release[1][0]))
    return [result for result in results]

if __name__ == "__main__":
    main()
