from sys import argv
import json

data = json.loads(" ".join(argv[1:]))
print(type(data))
print(data)
