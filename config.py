class Config(object):
   ''' Common configuration '''

class DevelopmentConfig(Config):
   ''' Development configuration '''
   DEBUG = True
   
class TestingConfig(Config):
   ''' Testing configuration '''
   
class ProductionConfig(Config):
   ''' Production configuration '''
   DEBUG = False

app_config = {
   'development' : DevelopmentConfig,
   'production' : ProductionConfig,
   'testing' : TestingConfig,
   'default' : 'development'
}
