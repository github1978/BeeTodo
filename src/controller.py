import sqlite3
import utils

TDITEMS_TABLE_NAME = "TDITEMS"


def dict_factory(cursor, row):
    return dict((col[0], row[idx]) for idx, col in enumerate(cursor.description))


conn = sqlite3.connect(utils.getExePath() + 'mytodo.db')
conn.row_factory = dict_factory


def sortToDoItems(items):
    pass


def queryItems(wheresql=None):
    if wheresql is None:
        return excuteSql("select * from " + TDITEMS_TABLE_NAME).fetchall()
    else:
        return excuteSql("select * from " + TDITEMS_TABLE_NAME + "where " + wheresql).fetchall()


def saveItems(items: list):
    sql = "insert into " + TDITEMS_TABLE_NAME + " values (?,?,?,?,?,?,?)"
    conn.executemany(sql, items)
    conn.commit()


def delItems(items: list):
    list_ids = []
    for item in items:
        list_ids.append(item['id'])
    sql = "delete from " + TDITEMS_TABLE_NAME + " where id in " + str(tuple(list_ids)).replace(',)', ')')
    excuteSql(sql)


def exportItems(items):
    pass


def closeDbConn():
    conn.close()


def excuteSql(sql):
    try:
        temp = conn.execute(sql)
        conn.commit()
        return temp
    except Exception as e:
        print(e)


if __name__ == '__main__':
    conn.execute(
        '''
        CREATE TABLE TDITEMS
        (
        id INT PRIMARY KEY NOT NULL,
        todo TEXT NOT NULL,
        imp  CHAR(50),
        emg  CHAR(50),
        state INT,
        create_date TEXT,
        sort INT
        );
        '''
    )
