import requests, json


TAG = "v0.3"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

release = requests.get(
    f"https://api.github.com/repos/nguyenvukhang/backblaze/releases/tags/{TAG}",
    headers=HEADERS,
).json()
incl = []


for asset in release["assets"]:
    if not asset["name"].endswith(".zip"):
        continue
    name = asset["name"][:-4]
    incl.append({"dl_url": asset["browser_download_url"], "name": name})

print(json.dumps({"include": incl}))
