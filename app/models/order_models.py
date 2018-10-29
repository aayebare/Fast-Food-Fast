from app.models import Database

db = Database()


class Orders:
    def __init__(self,
                 user_id,
                 item_id,
                 order_id,
                 date_post,
                 content,
                 order_status="New"):
        self.date_post = date_post
        self.content = content
        self.order_status = order_status
        self.order_id = order_id
        self.user_id = user_id
        self.item_id = item_id

    def post_order(self):
        '''user posts an order'''
        command = '''INSERT INTO orders (user_id,item_id, date_post, content, order_status)
        VALUES (%s, %s, %s, %s, %s)
        '''
        db.c.execute(command, (self.user_id, self.item_id, self.date_post,
                               self.content, self.order_status))

    def get_user_orders(self):
        '''get history of all customer orders'''
        command = "SELECT date_post, content, order_status FROM orders WHERE user_id = %s"
        db.c.execute(command, (self.user_id, ))
        value = db.c.fetchall()
        all_orders = []
        keys = ['date', 'content', 'status']
        for order in value:
            all_orders.append(dict(zip(keys, order)))
        return all_orders

    def get_admin_orders(self):
        '''get all orders by admin'''
        command = "SELECT * FROM orders"
        db.c.execute(command, )
        value = db.c.fetchall()
        all_orders = []
        keys = ['user_id', 'item_id', 'order_id', 'date', 'content', 'status']
        for order in value:
            all_orders.append(dict(zip(keys, order)))
        return all_orders

    def get_single_order(self):
        '''get a single order by admin'''
        command = "SELECT * FROM orders WHERE order_id = %s"
        db.c.execute(command, (self.order_id, ))
        value = db.c.fetchall()
        single_order = []
        keys = ['user_id', 'item_id', 'order_id', 'date', 'content', 'status']
        for order in value:
            single_order.append(dict(zip(keys, order)))
        return single_order

    def update_order(self):
        '''admin update the status of an order'''
        command = "UPDATE orders SET order_status=%s WHERE order_id=%s"
        db.c.execute(command, (self.order_status, self.order_id))
