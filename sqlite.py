from methods import db
while True:
    try:
        print(db.exec(input('>>>')))
    except Exception as e:
        print(f"ERROR: {e.args}")