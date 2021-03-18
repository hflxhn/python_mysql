# Thu 26 Sep 21:27:05 CST 2019

import pymysql;
import time;
import json;

class Db():

    def __init__(self, config = {}):
        self.config = config;

    # connect mysql server
    def connect(self):
        self.conn = pymysql.connect(
            host = self.config['hostname'],
            port = self.config['hostport'],
            user = self.config['username'],
            passwd = self.config['password'],
            db = self.config['database'],
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor
        );
        self.cursor = self.conn.cursor();

    # close mysql server
    def close(self):
        self.cursor.close();
        self.conn.close();

    # result fun
    def result(self, data = "", code = 0, msg = "success"):
        result = {
            "code": code,
            "msg": msg,
            "time": int(time.time()),
            "data:": data
        }
        return result;

    # search all data
    def select(self, sql):
        try:
            self.connect();
            self.cursor.execute(sql);
            data = self.cursor.fetchall();
            self.close();
        except Exception as e:
            return self.result(None, 1, e.message);

        return self.result(data);

    # search one data
    def find(self, sql):
        try:
            self.connect();
            self.cursor.execute(sql);
            data = self.cursor.fetchone();
            self.close();
        except Exception as e:
            return self.result(None, 1, e);

        return self.result(data);

    def save(self, table, data):
        if "id" in data:
            return self.update(table, data);

        data['create_time'] = int(time.time());
        data['update_time'] = int(time.time());
        data_k = '';
        data_v = '';
        for k in data:
            data_k += k + ', ';
            if isinstance(data[k], dict):
                data[k] = json.dumps(data[k], ensure_ascii=False);
            data_v += "'" + str(data[k]) + "', ";

        sql = "insert into {0} ({1}) value ({2})".format(table, data_k[:-2], data_v[:-2]);

        try:
            self.connect();
            self.cursor.execute(sql);
            insert_id = self.conn.insert_id();
            self.conn.commit();
            self.close();
        except Exception as e:
            return self.result(sql, 1, e);

        return self.result(insert_id);

    def update(self, table, data):
        data['update_time'] = int(time.time());
        data_v = '';
        for k in data:
            if k != 'id':
                if isinstance(data[k], dict):
                    data[k] = json.dumps(data[k], ensure_ascii=False);
                data_v += k + '=';
                data_v += "'" + str(data[k]) + "', ";

        sql = "update {0} set {1} where id = {2}".format(table, data_v[:-2], data['id']);

        try:
            self.connect();
            self.cursor.execute(sql);
            self.conn.commit();
            self.close();
        except Exception as e:
            return self.result(sql, 1, e);

        return self.result(data);
