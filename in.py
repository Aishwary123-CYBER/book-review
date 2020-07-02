import requests
res = requests.get("https://www.goodreads.com/book/title.json", params={"key": "TQZvfyF3DlIkCm9e7PWFxw", "title": "Steve Jobs",})
print(res.json())