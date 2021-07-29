# OCP Advanced Analytics Tool
This tool is meant to be used to generate advanced analytics in the form of graphs to help evaluate OpenShift based k8s clusters.
Using a simple python container this tool generates the graphs then serves those graphs using a flask webserver within the container. Use `oc expose` to get external access from the cluster.

Use cases:
- Migration preparations
- Healthcheck evaulations
- General cluster metrics (Not meant as a replacement for Prometheus)

## Current features
- OCP `BuildConfig` source image stats and shows the top 20 used images (Pi and Bubble Charts)

## Installation
```
# Install using kustomize
oc apply -k deploy/overlay/app/

# Expose HTTPS Web Server (If using wildcard OCP routes)
oc create route edge --service=adv-analytics
```
Note: This process was built for disconnected instances in mind so the above tool is built using 
a `BuildConfig` using the stock python3 image found in most clusters. This process will take a few minutes to build,
once completed the `Deployment` will automatically trigger and deploy the tool.

Go to the HTTPS hostname provided by the route generated to see the content
adv-analytics-adv-analytics.apps.<cluster-name>.<base-domain>

wget also can be used to retreive content
```
wget https://adv-analytics-adv-analytics.apps.<cluster-name>.<base-domain>/image-pi.png
wget https://adv-analytics-adv-analytics.apps.<cluster-name>.<base-domain>/image-bubble.png
```

