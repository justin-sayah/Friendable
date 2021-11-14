import requests, io, base64, cv2
import PIL.Image as img

def make_human():
    obj = img.open(io.BytesIO(requests.get("https://thispersondoesnotexist.com/image", headers={'User-Agent': 'My User Agent 1.0'}).content))
    obj.save('gen_human.jpeg')
    foto = cv2.imread('gen_human.png')
    encoded = base64.b64encode(foto)
    return ('data:image/png;base64,{0}"/>').format(encoded)

make_human()