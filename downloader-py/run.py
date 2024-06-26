import requests
from sys import argv
from os import stat, path
from subprocess import run


def read_file(path: str):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except:
        return None


BASE_URL = "https://api.github.com/repos/nguyenvukhang/backblaze"
api_github = lambda v: path.join(BASE_URL, v)


if len(argv) < 2:
    print("Please supply the target tag as the first CLI arg.")
    exit(1)


# curl -L \
#   -H "Accept: application/vnd.github+json" \
#   -H "Authorization: Bearer <YOUR-TOKEN>" \
#   -H "X-GitHub-Api-Version: 2022-11-28" \
#
TAG = argv[1]
TOKEN = read_file(".env")


print("Using tag:", TAG)

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


res = requests.get(api_github(f"releases/tags/{TAG}"), headers=HEADERS).json()
print(res.keys())


def curl(id: str, name: str):
    cmd = ["curl", "-o", name, "-L", "-H", "Accept: application/octet-stream"]
    cmd += ["-H", f"Authorization: Bearer {TOKEN}"] if TOKEN is not None else []
    cmd += [api_github(f"releases/assets/{id}")]
    run(cmd)


for asset in res["assets"]:
    print("name:", asset["name"])
    print(asset.keys())
    curl(asset["id"], asset["name"])
    print("waiting...")
    break
