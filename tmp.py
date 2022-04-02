
class cursor():
    def __init__(self,db):
        self.cursor = db.cursor()
    def execute(self,query,params=None):
        #print(query)
        if params:
            return self.cursor.execute(query,params)
        else:
            return self.cursor.execute(query)
        
    def fetchall(self):
        return self.cursor.fetchall()
vars = {}