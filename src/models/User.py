from db.database import Database
import pytz
from datetime import datetime, timedelta


class User():
    db = Database()

    def __init__(self, account_ig='', cookie='', dateExpired='', md5='', activo=''):
        self.account_ig = account_ig
        self.cookie = cookie
        self.dateExpired = dateExpired
        self.md5 = md5
        self.activo = activo

    @classmethod
    def getAllUser(self):
        result = self.db.get(
            "SELECT u.id, u.account_ig, u.cookie, u.dateExpired, u.md5, u.activo FROM users as u")
        if len(result) == 0:
            return []
        users = []
        for row in result:
            user = User(row[1], row[2], row[3], row[4], row[5])
            users.append(user.__dict__)
        return users

    @classmethod
    def findUser(self, account, md5):
        if md5 == '':
            raise ValueError("Los campos account y password son obligatorios")
        result = self.db.get(
            "SELECT u.id, u.account_ig, u.cookie, u.dateExpired, u.md5, u.activo FROM users as u WHERE u.md5 =%s and u.account_ig = %s", (md5, account))
        if len(result) == 0:
            return []
        user = User(result[0][1], result[0][2], result[0]
                    [3], result[0][4], result[0][4])
        return user.__dict__

    @classmethod
    def createOrUpdateUser(self, user):
        userFind = self.findUser(user['account_ig'], user['md5'])
        tz = pytz.timezone('America/Montevideo')
        nowDate = datetime.now(tz) + timedelta(days=365)
        if len(userFind) == 0:
            query = "INSERT INTO users (account_ig, cookie, dateExpired, `md5`, activo) VALUES (%s, %s, %s, %s, %s)"
            parameters = (
                str(user['account_ig']),
                str(user['cookie']),
                nowDate,
                str(user['md5']),
                1,
            )
            self.db.saveOrUpdate(query, parameters)
        else:
            query = "UPDATE users AS u SET u.cookie=%s, u.dateExpired=%s WHERE u.md5 = %s "
            parameters = (
                str(user['cookie']),
                nowDate,
                str(user['md5'])
            )
            self.db.saveOrUpdate(query, parameters)
