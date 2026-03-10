from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from ImageProcessing.router import  IP_Router

app=FastAPI()
app.include_router(IP_Router)
app.mount("/hairstyles",StaticFiles(directory="ImageProcessing/hairstyles"))