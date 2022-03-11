import cfg
from sqlite3 import connect
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
connection = connect(cfg.dataBaseFile)
cursor = connection.cursor()
while True:
    try:
        query = prompt('>>> ',history=FileHistory('.sqlite_history'))
        cursor.execute(query)
        connection.commit() # После всех инсертов   
        res = cursor.fetchall()
        print(res)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"ERROR: {e.args}")
    
cursor.close()
connection.close()
