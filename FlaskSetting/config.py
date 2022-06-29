from flask import Config

class config(object):
    TESTING = False
    DEBUG = False

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

class TestingConfig(Config):
    ENV = "TESTING"
    TESTING = True

