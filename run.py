
#import os
from app import app
from app.models import Database

#os.environ['env'] = 'development' 
#from app.models.user_models import c
db = Database()
db.create_tables()


if __name__ == "__main__":
 	app.run(debug=True)