import base64
import requests

class HairestyleServices():
    @staticmethod
    #liste des images
    def all_styles():
        return[
            {
                "id":1,
                "name":"afro",
                "url":"/hairstyles/afro.png",
                "prompt":"long voluminous curly hair, realistic, high quality"
            },
            {
                "id":2,
                "name":"locks",
                "url":"/hairstyles/locks.png",
                "prompt":"short skin fade haircut, clean edges, photorealistic"
            },
            {
                "id":3,
                "name":"moore",
                "url":"/hairstyles/moore.png",
                "prompt":"short skin curly hair,realistic, high quality"
            }
        ]

class AIService:
    @staticmethod
    #communication avec stability Matrix
    async def generate_new_hair(image_path: str, prompt: str):
        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

        url = "http://192.168.100.140"
        payload = {
            "init_images": [encoded_string],
            "prompt": f"{prompt}, highly detailed, photorealistic, cinematic lighting",
            "negative_prompt": "bald, deformed, ugly, blurry, low quality",
            "steps": 25,
            "cfg_scale": 7.5,
            "denoising_strength": 0.55,
            "sampler_name": "Euler a"
        }

        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json()['images'][0]
        else:
            raise Exception("Erreur de communication avec Stability Matrix")