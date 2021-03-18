
from dbMysql import Db;

if __name__ == '__main__':
    config = {
        'hostname' : 'localhost',
        'database' : 'hflxhn',
        'username' : 'mw',
        'password' : '123',
        'hostport' : 3306,
        'prefix'   : 'hflxhn_',
    }
    db = Db(config);

    # sql = 'select * from hflxhn_user where id = 2';
    # data = db.find(sql);
    # print(data)

    data = {
        "user_id": 666,
        "address": "8.8.8.8",
        "info": {
            "address": "114.114.114.114",
            "ip": "172.24.0.100",
        },
        "id": 2,
    }
    result = db.save('hflxhn_user_log', data);
    print(result)

