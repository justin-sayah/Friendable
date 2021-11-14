import requests, io, base64, cv2
import PIL.Image as img

def make_human(index):
    obj = img.open(io.BytesIO(requests.get("https://thispersondoesnotexist.com/image", headers={'User-Agent': 'My User Agent 1.0'}).content))
    obj.save('human_'+index+'.jpeg')