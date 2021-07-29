import numpy as np
import matplotlib.pyplot as plt
import subprocess
import requests
import sys
import json
import re
from collections import Counter
from random import randint

session = requests.Session()
session.verify = False
session.headers = {
    'Accept': 'application/json',
}

def bash_command(cmd): 
  ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
  return ps.communicate()[0]

token = bash_command("cat /var/run/secrets/kubernetes.io/serviceaccount/token")
if token is not None:
  session.headers['Authorization'] = 'Bearer {0}'.format(token)

colors_ = lambda n: list(map(lambda i: "#" + "%06x" % randint(0, 0xFFFFFF),range(n)))
images = []

# URL Base
base_url = "https://kubernetes.default.svc.cluster.local/api/v1"
users_base_url = "https://kubernetes.default.svc.cluster.local/api/user.openshift.io/v1"
namespace = bash_command("cat /var/run/secrets/kubernetes.io/serviceaccount/namespace")
namespaces = session.get(base_url + "/namespaces")
namespaces.raise_for_status()

if namespaces.status_code != 200:
  print("Failed to get Namespaces: {}".format(namespaces.status_code))
  sys.exit(1)
for namespace in namespaces.json()["items"]:
  namespace_name = namespace["metadata"]["name"]
  if not namespace_name.startswith("openshift") and not namespace_name.startswith("kube") and not namespace_name.startswith("default"):
    builds = session.get("https://kubernetes.default.svc.cluster.local/apis/build.openshift.io/v1/namespaces/{}/buildconfigs".format(namespace_name))
    builds.raise_for_status()
    if builds.status_code != 200:
      print("Failed to get builds for namespace: {}".format(namespace_name))
      continue
    for build in builds.json()["items"]:
      image_src = build["spec"]["strategy"]["dockerStrategy"]["from"]["name"]
      image = re.search("^(?:(?=[^:\/]{1,253})(?!-)[a-zA-Z0-9-]{1,63}(?<!-)(?:\.(?!-)[a-zA-Z0-9-]{1,63}(?<!-))*(?::[0-9]{1,5})?/)?((?![._-])(?:[a-z0-9._-]*)(?<![._-])(?:/(?![._-])[a-z0-9._-]*(?<![._-]))*)(?::(?![.-])[a-zA-Z0-9_.-]{1,128})?$", image_src).group(1)
      images.append(image)
      
count = Counter(images).most_common()
count = count[:20]

data = {
    'titles': [key for key, _ in count],
    'data': [float(value) for _, value in count],
    'color': colors_(len(count))
}


# Creating plot
fig = plt.figure(figsize =(10, 7))
plt.pie(data["data"], labels = data["titles"])

plt.savefig('/app/serve/image-pi.png')