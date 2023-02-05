from pymongo import MongoClient

from utils.configs import get_mongo_creds

def get_mongo_connection():
    user, pwd, host, db = get_mongo_creds()

    con_str = f"mongodb+srv://{user}:{pwd}@{host}/{db}?retryWrites=true&w=majority"

    return MongoClient(con_str)
