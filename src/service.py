import sqlite3
import utils

TDITEMS_TABLE_NAME = "TDITEMS"


def dict_factory(cursor, row):
    return dict((col[0], row[idx]) for idx, col in enumerate(cursor.description))


conn = sqlite3.connect('mytodo.db')
conn.row_factory = dict_factory
conn.execute(
    '''
    CREATE TABLE IF NOT EXISTS TDITEMS
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


def updateItems(items: list):
    keys_list = list(items[0].keys())
    id_index = keys_list.index("id")
    keys_list.remove("id")
    for i, v in enumerate(keys_list):
        keys_list[i] = v + "=?"
    values_list = []
    for item in items:
        temp = list(item.values())
        del (temp[id_index])
        temp.append(item["id"])
        values_list.append(tuple(temp))
    sql = "update " + TDITEMS_TABLE_NAME + " set " \
          + str(tuple(keys_list)).replace("(", "").replace(")", "").replace("'", "")\
          + " where id=?"
    try:
        conn.executemany(sql, values_list)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)


def queryItems(wheresql=""):
    sql = "select * from " + TDITEMS_TABLE_NAME + " where 1=1 " + wheresql
    result = excuteSql(sql)
    if result is None:
        return []
    result_list = excuteSql(sql).fetchall()
    result_list.sort(key=lambda k: (int(k.get("emg") + k.get("imp")), k.get("create_date")), reverse=True)
    return result_list


def saveItems(items: list):
    sql = "insert into " + TDITEMS_TABLE_NAME + " values (?,?,?,?,?,?,?)"
    try:
        conn.executemany(sql, items)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)


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
        conn.rollback()
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
