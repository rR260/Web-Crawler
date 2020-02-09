from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
## database work
from pymongo import MongoClient
import json

## these 2 functions are for removing unwanted hidden text from webpage
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

html1 = urllib.request.urlopen('https://randomaccesstechnology.wordpress.com/2018/03/24/iot/').read()  
html =text_from_html(html1)
html = html.lower()
a=""
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist
a=' '.join(unique_list(html.split()))
##html=html1.decode()
##html=html.translate(string.punctuation)
##p=RegexpTokenizer(r'\w+')
##z=p.tokenize(html)

stop_words= set(stopwords.words('english'))
word_tokens= word_tokenize(a)

filtered_sentence = [w for w in word_tokens if not w in stop_words]

filtered_sentence=[]

for w in word_tokens:
                if w not in stop_words:
                    filtered_sentence.append(w)
                   
## jason conversion

## my_json_string = json.dumps(filtered_sentence)
##print(filtered_sentence)

## datamongo code

try:
conn = MongoClient()
print("Connected successfully!!!")
except:
print("Could not connect to MongoDB")

# database
db = conn.database

# Created or Switched to collection names: my_gfg_collection
collection = db.abc

dict_key ={}
total_keywords=len(filtered_sentence)
dict_key = { i : filtered_sentence[i] for i in range(0, len(filtered_sentence) ) }

#print(dict_key)

#db_id = collection.insert_many(dict_key)
#print("Data inserted with record ids",db_id)

values = []
values = filtered_sentence

with open("file.txt", "w",encoding='utf-8') as output:
    output.write(str(values))


client = MongoClient()
db = client.test_database  # use a database called "test_database"
files = db.files   # and inside that DB, a collection called "files"

f = open('file.txt')  # open a file
text = f.read()    # read the entire contents, should be UTF-8 text

# build a document to be inserted
text_file_doc = { "contents" : text }
# insert the contents into the "file" collection
db.files.insert_one(text_file_doc)
db.files.save(text_file_doc)
# Printing the data inserted
cursor = files.find()
for record in cursor:
    print(record)
