from flask import Flask, render_template
import advertools as adv
from task_code import *
from model import *
import os
import json

# link to display json
# https://stackoverflow.com/questions/62906140/displaying-json-in-the-html-using-flask-and-local-json-file
app = Flask(__name__)
app.config['IMG_FOLDER'] = "static/images/"

@app.route('/')
def hello():
    return "hello world"

@app.route('/data', methods=("POST", "GET"))
def html_table():
    df = read_data()
    df = df.head()
    return render_template('index.html', title="page", jsonfile=json.dumps(df.to_dict('dict')))

# @app.route('/stat', methods=("POST", "GET"))
# def stats():
#     df = read_data()
#     data1 = clean(df)
#     rows = data1.shape[0]
#     return render_template('index.html', title="page", jsonfile=json.dumps(df.to_dict('dict')))

@app.route('/more_tweeters', methods = ("POST","GET"))
def more_tweeters():
    df = read_data()
    data1 = clean(df)
    # top 10 users with more tweets
    data1['user_screen_name'] = data1['user_screen_name'].str.replace("b'","")
    data1['user_screen_name'] = data1['user_screen_name'].str.replace("'","")

    more_tweet = data1['user_screen_name'].value_counts()[:10]
    sampledf = pd.DataFrame()
    sampledf['people'] = more_tweet.index
    sampledf['tweetcount'] = more_tweet.values
    return render_template('index.html', title="page", jsonfile=json.dumps(sampledf.to_dict('dict')))

@app.route('/wordfreq', methods = ("POST","GET"))
def wordfrequency():
    df = read_data()
    data1 = clean(df)
    df  = word_frequency(data1)
    return render_template('index.html', title="page", jsonfile=json.dumps(df.to_dict('dict')))

@app.route('/wordcloud', methods = ("POST","GET"))
def wordcloud():
    df = read_data()
    data1 = clean(df)
    data1['tweet']  = data1['tweet'].str.replace("\n"," ")
    all_hashtags  =[]
    for tweet in data1['tweet']:
        tags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.lower())
        all_hashtags.append(tags)
    flatten_hashtags = [tag for tag_list in all_hashtags for tag in tag_list]
    hashtag_counts = collections.Counter(flatten_hashtags)
    hashtags = []
    counts = []
    print(hashtag_counts,"hiiiiiiiiiiiiiiiiiii")
    for hashtag,count in hashtag_counts.items():
        hashtags.append(hashtag), counts.append(count)
    hashtag_df = pd.DataFrame({'hashtags': hashtags,'count': counts})
    return render_template('index.html', title="page", jsonfile=json.dumps(hashtag_df.to_dict('dict')))

@app.route('/location', methods = ("POST","GET"))
def getloc():
    df = read_data()
    data1 = clean(df)
    locs = data1['userlocation'].str.replace("b''","N/A").str.replace("b'","").str.replace("'","").value_counts()
    loc_df = pd.DataFrame({"location":locs.index, "count":locs.values})
    return render_template('index.html', title="page", jsonfile=json.dumps(loc_df.to_dict('dict')))

@app.route('/emoji', methods = ("POST","GET"))
def getemojidf():
    df = read_data()
    data1 = clean(df)
    emojidf = getemoji(data1)
    emoji = []
    count = []
    for k,v in emojidf[:20]:
        emoji.append(k)
        count.append(v)
    emoji_df = pd.DataFrame({"emoji ":emoji, "count":count})
    return render_template('index.html', title="page", jsonfile=json.dumps(emoji_df.to_dict('dict')))

@app.route('/lang', methods = ("POST","GET"))
def getlang():
    df = read_data()
    data1 = clean(df)
    lang = data1['lang'].value_counts(ascending = False).index
    count = data1['lang'].value_counts(ascending = False).values
    sampledf = pd.DataFrame({"language" :lang, "count":count})
    return render_template('index.html', title="page", jsonfile=json.dumps(sampledf.to_dict('dict')))

@app.route('/daytweets', methods = ("POST","GET"))
def gettweetsaday():
    df = read_data()
    data1 = clean(df)
    data1['time']  = pd.to_datetime(data1['time'])
    data1['day'] = data1['time'].dt.day
    tweetaday  = pd.DataFrame(data1.groupby(['day'])['day'].count())
    tweetaday  = tweetaday.rename(columns={'day':'count'})
    tweetaday  = tweetaday.reset_index()
    return render_template('index.html', title="page", jsonfile=json.dumps(tweetaday.to_dict('dict')))

@app.route('/emotionpie', methods=("POST", "GET"))
def emotion():
    df = read_data()
    data1 = clean(df)
    emotion = get_sentiment(data1) 
    emotions = [ ]
    for i in emotion:
        emotions.append(i[0])
    emotdict = collections.Counter(emotions)
    return render_template('index.html', title="page", jsonfile=json.dumps(emotdict))

if __name__ == '__main__':
    app.run(debug = True)
