# This script fetches all the metadata from the verbatim copy hosted on GitHub
# Actions. This includes getting the most up-to-date list of parquets.
#
# This script is used on GitHub Actions in the postprocessing stage.

import requests, json, os, sys

TAG = "v1.0"

BASE_URL = "https://api.github.com/repos/nguyenvukhang/backblaze"
api_github = lambda v: os.path.join(BASE_URL, v)


HEADERS = { "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" }  # fmt: skip
os.makedirs("output", exist_ok=True)
res = requests.get(api_github(f"releases/tags/{TAG}"), headers=HEADERS).json()
print(res, file=sys.stderr)
assets = filter(lambda a: a["name"].endswith(".zip"), res["assets"])
incl = [{"id": str(asset["id"]), "name": str(asset["name"])} for asset in assets]
print(json.dumps({"include": incl}))
