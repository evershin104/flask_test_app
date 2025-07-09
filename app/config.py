class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TITLE = "Test task app"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"       # Не работает вроде, не копал туда
    API_SPEC_OPTIONS = {
        "info": {
            "description": "API для отзывов с определением вайба",
        },
    }
