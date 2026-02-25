import http.client
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()
global api_key
api_key = os.environ.get("POLL_API")

def imagegen(inputimage):
    encoded_prompt = urllib.parse.quote(inputimage)
    conn = http.client.HTTPSConnection("gen.pollinations.ai")
    headers = { 'Authorization': f"Bearer {api_key}" }
    conn.request("GET", f"/image/{encoded_prompt}?model=zimage&negative_prompt=extra%20fingers%2C%20deformed&enhance=true&seed=-1", headers=headers)
    res = conn.getresponse()
    data = res.read()
    with open("output.png", "wb") as f:
        f.write(data)
    print("Saved image to output.png")