import time

import pandas as pd

from google.cloud import datastore

from google.oauth2.id_token import verify_firebase_token

from google.auth.transport import requests


class Database(datastore.Client):

    def get_status(self, name='default'):
        key = self.key('status', name)
        entity = self.get(key)
        if entity is None:
            entity = datastore.Entity(key)
            entity['assign'] = [0, 0, 0, 0]
            entity['done'] = [0, 0, 0, 0]
        return entity

    def get_user_data(self, data):
        request_adapter = requests.Request()
        uid = verify_firebase_token(data['token'], request_adapter)['user_id']
        if uid is None:
            return
        key = self.key('user_data', uid,)
        entity = self.get(key)
        if entity is None:
            entity = datastore.Entity(key)
            entity['n_start'] = 0
        return entity

    def get_session_data(self, data):
        request_adapter = requests.Request()
        uid = verify_firebase_token(data['token'], request_adapter)['user_id']
        if uid is None:
            return
        key = self.key('user_data', uid, 'session_data', str(data['session_id']))
        entity = self.get(key)
        if entity is None:
            entity = datastore.Entity(key)
            keys = [
                "houseCard1", "houseCard2",
                "playerCard1", "playerCard2",
                "action", "dif", "time", "point","intervenue"
            ]
            for k in keys:
                entity[k] = -100
        return entity
        
    def get_train_data(self,data):
        request_adapter = requests.Request()
        uid = verify_firebase_token(data['token'], request_adapter)['user_id']
        if uid is None:
            return
        user_key = self.key("user_data", uid)
        query = self.query(kind="session_data", ancestor=user_key)
        dbdata = list(query.fetch())
        print(dbdata)
        train_data = []
        for entity in dbdata:
            if int(entity["action"]) < 0:
                continue
            train_data.append(
                [
                    int(entity["dif"]),
                    int(entity["action"]),
                ]
            )
        return pd.DataFrame(train_data, columns=["dif", "act"])
