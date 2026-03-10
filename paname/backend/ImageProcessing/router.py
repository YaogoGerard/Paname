from typing import List
from fastapi import APIRouter,UploadFile,File,Form,HTTPException
from ImageProcessing.schemas import Hairstyle
from ImageProcessing.services import HairestyleServices,AIService
import os
import shutil


IP_Router=APIRouter()
#ici c'est une route pour recuperer les coifures dispo
@IP_Router.get("/hairstyles",response_model=List[Hairstyle])
async def get_Styles():
    styles=HairestyleServices.all_styles()
    return styles
#c'est cette route qui transforme l'image
@IP_Router.post("/transform")
async def transform_hair(image: UploadFile = File(...), prompt: str = Form(...)):
    if not image.filename:
        raise HTTPException(status_code=400, detail="Nom de fichier manquant")

    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        
    file_path = os.path.join(upload_dir, image.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    try:
        result_image_base64 = await AIService.generate_new_hair(file_path, prompt)
        return {"status": "success", "image": result_image_base64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))