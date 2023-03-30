import tgdd_scraper
import fpt_scraper
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Replace the placeholder with your Atlas connection string
uri = "mongodb+srv://hdkhang6803:KhangHocMai123@cluster0.i54r4z6.mongodb.net/?retryWrites=true&w=majority"

# Set the Stable API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))
                          
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['mydatabase']
collection = db['mycollection']

input_string = "laptop lenovo 3 ideapad"

dict_tgdd = tgdd_scraper.get_list(input_string)
#dict_fpt = fpt_scraper.get_list(input_string)
collection.insert_many(dict_tgdd)
#collection.insert_many(dict_fpt)
