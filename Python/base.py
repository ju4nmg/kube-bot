
from kubernetes import client, watch
from kubernetes.client.rest import ApiException
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# import os
import yaml
import time
import sys

# runit= 

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ii05UHFEUWpsRkkwd3ljV3B2UXRzUENlWHpMUWRwYUg4djYtLWl6ZFFUazAifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJib3QiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlY3JldC5uYW1lIjoiYm90LXNlY3JldCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJib3Qtc2EiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJkMGNjNDEzYS05NzIzLTQwMzEtYTIxYi00OGU0NTIwNmM1YTUiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6Ym90OmJvdC1zYSJ9.UvhUSrHSUqn7MIYOUgDfsADr1L8ELL9dnhItjkBla5lHLbnih3e0TFY12c6A3xbtcLCcs8l6TJmhKAINYsTaifLqrShfnrQIj7DAj11LoCfMqxbjOmC7iVzsN6k0Vl0r3vzfaLQfU2LySPsXl_Nk25gStPu_S6n15cZmv_OJ5K7u5wcbHgCGDJOXRXQCoTspuJznhYHMwyIUBnUEJBA2RndRtr4QyReNQLjUh-yuja2UxD0ma8rvEuARqvdYx5xe676zGrxVKhGBMFiFLN4gy4lu3p9gXtTM4a_tHOChshOkN0LKmlYKRrHM6V9FJJj-V0O3JLmNunyci2wfCe60iw"

configuration = client.Configuration()
configuration.api_key_prefix["authorization"] = "Bearer"
configuration.host = "https://192.168.49.2:8443"
configuration.api_key["authorization"] = token
# configuration.api_key["authorization"] = os.getenv("KIND_TOKEN", None)
configuration.verify_ssl = False 
# api_client = client.ApiClient(configuration)
core = client.CoreV1Api(client.ApiClient(configuration))
apps = client.AppsV1Api(client.ApiClient(configuration))


# yaml=open('deploy.yaml', 'r').read()
# ret = core.list_namespaced_pod(namespace="bot", watch=False)
# for pod in ret.items:
    # print(pod.metadata.creation_timestamp)
    # print(f"Name: {pod.metadata.name}, Namespace: {pod.metadata.namespace} IP: {pod.status.pod_ip}")
    # Name: example, Namespace: default IP: 10.244.2.2

    
def create_deploy(deploy_file):

    with open(deploy_file, 'r') as file:
        deploy = yaml.safe_load(file)

    deploy_name = deploy.get("metadata").get("name")

    if deploy.get("metadata").get("namespace"):
        deploy_namespace = deploy.get("metadata").get("namespace")
    else:
        deploy_namespace = "default"

    response = apps.create_namespaced_deployment(body=deploy, namespace=deploy_namespace)
    try:
        response = apps.read_namespaced_deployment_status(name=deploy_name, namespace=deploy_namespace)
        if response.status.available_replicas != int(deploy.get("spec").get("replicas")):
            print("Waiting for Deployment to become ready...")
            time.sleep(5)
        else:
            return
    except ApiException as e:
        print(f"Exception when calling AppsV1Api -> read_namespaced_deployment_status: {e}\n")
#
def watch_namespace(namespace):
    # count = 10
    for event in watch.Watch().stream(core.list_namespaced_event, namespace=namespace, timeout_seconds=10):
        print(event['object'].message)
        # count -= 1
        # if not count:
        #     watch.Watch().stop()



# f"Event - Message: {event['object']['message']} at {event['object']['metadata']['creationTimestamp']}"
 # watcher = watch.Watch()
 #        for event in watcher.stream(
 #            resource.get,
 #            namespace=namespace,
 #            name=name,
 #            field_selector=field_selector,
 #            label_selector=label_selector,
 #            resource_version=resource_version,
 #            serialize=False,
 #            timeout_seconds=timeout
 #        ):
 #            event['object'] = ResourceInstance(resource, event['object'])
 #            yield event 






if sys.argv[1] == 'deploy':
    create_deploy(sys.argv[2])
elif sys.argv[1] == 'watch':
    watch_namespace(sys.argv[2])
else:
    print('wrong command')
    sys.exit()

    