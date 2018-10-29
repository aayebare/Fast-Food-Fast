from app.models import Database

db = Database()


class Menu:
    def __init__(self, user_id, item_id, content, detail, price):
        self.content = content
        self.detail = detail
        self.price = price
        self.user_id = user_id
        self.item_id = item_id

    def add_item(self):
        '''add food item into the menu'''
        command = '''INSERT INTO menu (user_id,content,detail,price)
        VALUES (%s, %s, %s, %s)'''
        db.c.execute(command,
                     (self.user_id, self.content, self.detail, self.price))

    def get_menu(self):
        '''get all items in the menu'''
        command = "SELECT item_id, content, detail, price FROM menu"
        db.c.execute(command, )
        value = db.c.fetchall()
        items = []
        keys = ['item_id', 'content', 'detail', 'price']
        for item in value:
            items.append(dict(zip(keys, item)))
        return items

    def get_item_id(self):
        command_1 = "SELECT item_id FROM menu WHERE item_id = %s"
        

        #command = "SELECT item_id FROM menu WHERE item_id = '{}'".format(
        #    item_id)
        db.c.execute(command_1, (self.item_id, ))
        value = db.c.fetchall()
        print(value)
        if value:
           return value
        return False

    def get_Item_Detail(self):
        command = "SELECT content FROM menu WHERE item_id = %s"
        

        #command = "SELECT item_id FROM menu WHERE item_id = '{}'".format(
        #    item_id)
        db.c.execute(command, (self.item_id, ))
        value = db.c.fetchall()
        #print(value)
        if value:
           return value
        return False

