
from DbMysql import DbMysql;

class Init():

    __obj = None;
    __init_flag = True;

    # Singleton
    def __new__(cls, *args, **kwargs):
        if cls.__obj == None:
            cls.__obj = object.__new__(cls);
        return cls.__obj;

    """docstring for Init"""
    def __init__(self, config = {}):
        if self.__init_flag:
            config = {
                'hostname' : 'localhost',
                'database' : 'hflxhn',
                'username' : 'mw',
                'password' : '123',
                'hostport' : 3306,
                'prefix'   : 'hflxhn_',
            }
            self.db = DbMysql(config);
            self.__init_flag = False;

    """result fun"""
    def result(self, data = "", code = 0, msg = "success"):
        result = {
            "code": code,
            "msg": msg,
            "time": int(time.time()),
            "data": data
        }
        return result;

    # search one data
    def getOneData(self):
        sql = 'select * from hflxhn_user_log where id 1= 2';
        data = self.db.find(sql);
        return data;

    # search all data
    def getAllLists(self):
        sql = "select * from hflxhn_user_log where id = 2";
        data = self.db.select(sql);
        return data;

    # add data
    def addData(self):
        data = {
            "user_id": 666,
            "address": "8.8.8.8",
            "info": 'dmxy',
        }
        result = self.db.save('hflxhn_user_log', data);
        return result;

    # update data
    def updateData(self):
        data = {
            "user_id": 999,
            "address": "114.114.114.114",
            "info": '114.114.114.114_999_user1',
            "id": 80,
        }
        result = self.db.save('hflxhn_user_log', data);
        return result;

    # close mysql connection
    def colseDbConn():
        self.db.close();








if __name__ == '__main__':
    try:
        init = Init();

        data = init.getOneData();
        print(data);

        data = init.getAllLists();
        print(data);

        data = init.addData();
        print(data);

        data = init.updateData();
        print(data);
    except Exception as e:
        print(e);
