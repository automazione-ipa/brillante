import pymongo
from app_v2.utils.logger import get_logger
import os

logger = get_logger()


class DBCore:

    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("DB_CONNECTION_STRING"))

        self.db = self.client['CB_V1']

    def insert(self, collection: str, generic_dict: dict):
        mycol = self.db[f"{collection}"]
        x = mycol.insert_one(generic_dict)
        return x

    def delete_by_id(self, collection: str, id: str):
        mycol = self.db[f"{collection}"]
        x = mycol.delete_one({"_id": id})
        return x

    def delete_stats_by_user(self, collection: str, id: str):
        mycol = self.db[f"{collection}"]
        x = mycol.delete_one({"user_id": id})
        return x

    def update_last(self):
        obj_last_id = self.reading_last_from_mongo(collection="status")["_id"]
        filtro = {"_id": obj_last_id}

        aggiornamento = {"$set": {"running": False}}

        res = self.db["status"].update_one(filtro, aggiornamento)
        return res

    def reading_last_from_mongo(self, collection: str):
        filter = {
        }
        limit = 1
        sort = list({
                        "_id": -1
                    }.items())

        mycol = self.db[f"{collection}"]
        res = mycol.find_one(filter=filter, sort=sort, limit=limit)
        return res

    def read_user(self, collection: str, user: str):
        filter = {"_id": user
                  }
        mycol = self.db[f"{collection}"]
        res = mycol.find_one(filter=filter)

        return res

    def read_white_list_user(self):
        mycol = self.db[f"white_list"]
        res = mycol.find()
        full_list = list(res)

        lst_available_email = []
        lst_used_email = []
        lst_used_nickdame = []

        for element in full_list:
            if element['user'] == '':
                lst_available_email.append(element['_id'])
            else:
                lst_used_email.append(element['_id'])
                lst_used_nickdame.append(element['user'])

        return lst_available_email, lst_used_email, lst_used_nickdame

    def update_white_list_user(self, user: str, email: str):
        mycol = self.db[f"white_list"]
        filtro = {"_id": email}
        aggiornamento = {"$set": {'user': user}}
        mycol = mycol.update_one(filtro, aggiornamento)

    def get_all_user(self, collection):
        project = {
            '_id': 1
        }
        mycol = self.db[f"{collection}"]
        res = mycol.find(projection=project)
        return list(res)

    def read_bot_last_session_starting_time(self, user: str):
        filter = {"user_id": user
                  }
        sort = list({
                        "transaction_datetime": -1
                    }.items())
        mycol = self.db[f"running_info"]
        res = mycol.find_one(filter=filter, sort=sort)
        return res

    def read_bot_stat_by_time(self, user: str):
        filter = {"user_id": user
                  }
        sort = list({
                        "stats_datetime": -1
                    }.items())
        mycol = self.db[f"running_stats"]
        res = mycol.find_one(filter=filter, sort=sort)
        return res

    def update_user_info(self, collection: str, user: str, generic_dict: dict):
        filtro = {"_id": user}

        aggiornamento = {"$set": generic_dict}

        mycol = self.db[f"{collection}"].update_one(filtro, aggiornamento)
