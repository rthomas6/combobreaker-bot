import praw
import json
import pprint
import time

sub_list = ['pics', 'askreddit', 'funny', 'reactiongifs', 'showerthoughts', 'gaming', 'gifs']


def count_words(text):
    return len(text.split(' '))

def is_comboable(comment):
    #3 words or less
    if count_words(comment.body) > 3:
        return False
    #No links
    if 'http' in comment.body:
        return False
    #No more than 16 hours old
    #if (time.time() - float(comment.created)) > (16 * 60 * 60):
    #    #print('Too old found: {} secs old'.format(time.time() - float(comment.created)))
    #    #print('https://www.reddit.com' + comment.permalink + '?context=3')
    #    return False
    #Has enough upvotes
    if int(comment.score) < 5:
        #print('Not enough votes: {} votes'.format(comment.score))
        return False
    return True

def scan_comment_level(comment_forest, combo_count):
    for comment in comment_forest:
        if is_comboable(comment):
            if combo_count == 3:
                #send reply
                #print('found combo chain')
                #pprint.pprint(vars(comment))
                print('https://www.reddit.com' + comment.permalink + '?context=4')
            else:
                scan_comment_level(comment.replies, combo_count+1)

def scan_comments(submission):
    submission.comments.replace_more(limit=0)
    scan_comment_level(submission.comments, 0)
    for comment in submission.comments:
        scan_comment_level(comment.replies, 0)

with open('secrets.json', 'r') as secrets:
    auth = json.loads(secrets.read())

reddit = praw.Reddit(client_id  = auth['client_id'],
                  client_secret = auth['client_secret'],
                  user_agent    = auth['user_agent'],
                  username      = auth['username'],
                  password      = auth['password'])

for sub in sub_list:
    subreddit = reddit.subreddit(sub)
    for submission in subreddit.hot(limit=150):
        #pprint.pprint(vars(submission))
        if(time.time() - float(submission.created) < (6 * 60 * 60)):
            scan_comments(submission)
