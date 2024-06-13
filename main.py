import requests_async as requests
import base64

async def generate_image(params):
    response = await requests.post(
        url=f"http://127.0.0.1:7860/sdapi/v1/txt2img", json=params
    )

    r = response.json()
    encoded_data = r["images"][0]
    decoded_data = base64.b64decode(encoded_data)

    img = open("pic.jpeg", "wb")
    img.write(decoded_data)
    img.close()
