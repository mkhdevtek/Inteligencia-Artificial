import json
from facebook_scraper import get_posts

#for post in get_posts('Nintendo', pages=5, cookies='./cookies.txt'):
#    print(json.dumps(post, indent=2))


posts = list(get_posts('Nintendo', pages=3, cookies='./cookies.txt'))
print(f"Found {len(posts)} posts")
print(posts)
