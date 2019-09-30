""" Different configurations to be used by the Flask server
"""


class Config:  # pylint: disable=too-few-public-methods
    """
    Common configuration
    """


DEBUG = False
TESTING = False


class ProductionConfig(Config):  # pylint: disable=too-few-public-methods
    """
    Production configuration
    """
    DEBUG = False


class DevelopmentConfig(Config):  # pylint: disable=too-few-public-methods
    """
    Development configuration
    """
    DEBUG = True


class TestingConfig(Config):  # pylint: disable=too-few-public-methods
    """
    Testing configuration
    """
    TESTING = True
