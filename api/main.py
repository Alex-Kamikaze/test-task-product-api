import uvicorn

from api.models import *
from views import *

def start():
    uvicorn.run("api.views:app", host = "127.0.0.1", port = "8080")