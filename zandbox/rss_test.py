import feedparser

# URL of the RSS feed
feed_url = 'http://feeds.bbci.co.uk/news/rss.xml'

# Parse the RSS feed
feed = feedparser.parse(feed_url)

# Display the titles and links of the latest posts
for entry in feed.entries:
    # print(f"Title: {entry.title}")
    # print(f"Link: {entry.link}\n")
    print(entry)
