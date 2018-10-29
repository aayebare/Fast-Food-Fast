class Base():
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Base):
    DEBUG = True
    DEVELOPMENT = True
   
class TestingConfig(Base):
    DEBUG = False
    TESTING = True

class ProductionConfig(Base):
    DEBUG = False
    TESTING = False
   
 