from pydantic import BaseModel

#typage des donnes de sori apres la requete hairestyle
class Hairstyle(BaseModel):
    id:int
    name:str
    url:str
    prompt:str