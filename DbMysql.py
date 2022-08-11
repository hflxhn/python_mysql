# Thu 26 Sep 21:27:05 CST 2019

import pymysql;
import time;
import json;

class DbMysql():

    __obj = None;
    __init_flag = True;

    # Singleton
    def __new__(cls, *args, **kwargs):
        if cls.__obj == None:
            cls.__obj = object.__new__(cls);
        return cls.__obj;

    """
    init mysql config
    -----------------
    config (dict): {hostname, database, username, password, hostport, prefix}
    """
    def __init__(self, config):
        if self.__init_flag:
            connect = self.connect(config);
            self.__init_flag = False;

    """
    result fun
    -----------------
    data (int|str|dict|list)
    code (int) : status code
    msg  (str) : tips info
    """
    def result(self, data = "", code = 0, msg = "success"):
        result = {
            "code": code,
            "msg": msg,
            "time": int(time.time()),
            "data": data
        }
        return result;

    # connect mysql server
    def connect(self, config):
        try:
            conn = pymysql.connect(
                host = config['hostname'],
                port = config['hostport'],
                user = config['username'],
                passwd = config['password'],
                db = config['database'],
                charset = 'utf8',
                cursorclass = pymysql.cursors.DictCursor,
            );
            cursor = conn.cursor();
            self.conn = conn;
            self.cursor = cursor;
            return self.result(True, 0, "conn mysql server success");
        except Exception as e:
            raise Exception(self.result(None, 1, e));

    # close mysql server
    def close(self):
        self.cursor.close();
        self.conn.close();

    # search all data
    def select(self, sql):
        try:
            self.cursor.execute(sql);
            data = self.cursor.fetchall();
            # self.close();
        except Exception as e:
            return self.result(sql, 1, e);

        return self.result(data);

    # search one data
    def find(self, sql):
        try:
            self.cursor.execute(sql);
            data = self.cursor.fetchone();
            # self.close();
        except Exception as e:
            return self.result(sql, 1, e);

        return self.result(data);

    # handle add data
    def handleAddData(self, data):
        data['create_time'] = int(time.time());
        data['update_time'] = int(time.time());

        data_k = '';
        data_v = '';
        for k in data:
            data_k += k + ', ';
            if isinstance(data[k], dict):
                data[k] = json.dumps(data[k], ensure_ascii=False);
            data_v += "'" + str(data[k]) + "', ";

        result = {
            "key": data_k[:-2],
            "val": data_v[:-2],
        };

        return result;

    # handle update data
    def handleUpdateData(self, data):
        data['update_time'] = int(time.time());
        data_v = '';
        for k in data:
            if k != 'id':
                if isinstance(data[k], dict):
                    data[k] = json.dumps(data[k], ensure_ascii=False);
                data_v += k + '=';
                data_v += "'" + str(data[k]) + "', ";

        return data_v[:-2];

    # save or update data
    def save(self, table, data):
        if not isinstance(table, str):
            return self.result(None, 1, 'table name must be a string');
        if not isinstance(data, dict):
            return self.result(None, 1, 'data must be a dict');

        if "id" in data:
            return self.update(table, data);

        data_result = self.handleAddData(data);
        field = data_result['key'];
        value = data_result['val'];

        sql = "insert into {0} ({1}) value ({2})".format(table, field, value);

        try:
            self.cursor.execute(sql);
            insert_id = self.conn.insert_id();
            self.conn.commit();
            # self.close();
        except Exception as e:
            return self.result(sql, 1, e);

        return self.result(insert_id, 0, 'add data success');

    # update data
    def update(self, table, data):
        data_result = self.handleUpdateData(data);

        sql = "update {0} set {1} where id = {2}".format(table, data_result, data['id']);

        try:
            self.cursor.execute(sql);
            self.conn.commit();
            # self.close();
        except Exception as e:
            return self.result(sql, 1, e);

        return self.result(sql, 0, 'update data success');
