
from kubernetes import client
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# import os
import yaml

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ii05UHFEUWpsRkkwd3ljV3B2UXRzUENlWHpMUWRwYUg4djYtLWl6ZFFUazAifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJib3QiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlY3JldC5uYW1lIjoiYm90LXNlY3JldCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJib3Qtc2EiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJkMGNjNDEzYS05NzIzLTQwMzEtYTIxYi00OGU0NTIwNmM1YTUiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6Ym90OmJvdC1zYSJ9.UvhUSrHSUqn7MIYOUgDfsADr1L8ELL9dnhItjkBla5lHLbnih3e0TFY12c6A3xbtcLCcs8l6TJmhKAINYsTaifLqrShfnrQIj7DAj11LoCfMqxbjOmC7iVzsN6k0Vl0r3vzfaLQfU2LySPsXl_Nk25gStPu_S6n15cZmv_OJ5K7u5wcbHgCGDJOXRXQCoTspuJznhYHMwyIUBnUEJBA2RndRtr4QyReNQLjUh-yuja2UxD0ma8rvEuARqvdYx5xe676zGrxVKhGBMFiFLN4gy4lu3p9gXtTM4a_tHOChshOkN0LKmlYKRrHM6V9FJJj-V0O3JLmNunyci2wfCe60iw"

configuration = client.Configuration()
configuration.api_key_prefix["authorization"] = "Bearer"
configuration.host = "https://192.168.49.2:8443"
configuration.api_key["authorization"] = token
# configuration.api_key["authorization"] = os.getenv("KIND_TOKEN", None)
configuration.verify_ssl = False  # Only for testing with KinD!
# api_client = client.ApiClient(configuration)
core = client.CoreV1Api(client.ApiClient(configuration))
apps = client.AppsV1Api(client.ApiClient(configuration))


with open('deploy.yaml', 'r') as file:
    deploy = yaml.safe_load(file)

deploy_name = deploy.get("metadata").get("name")
print(deploy)


print(open('deploy.yaml', 'r').read())

if deploy.get("metadata").get("namespace"):
    deploy_namespace = deploy.get("metadata").get("namespace")
else:
    deploy_namespace = "default"
# ret = core.list_namespaced_pod(namespace="bot", watch=False)
# for pod in ret.items:
    # print(pod.metadata.creation_timestamp)
    # print(f"Name: {pod.metadata.name}, Namespace: {pod.metadata.namespace} IP: {pod.status.pod_ip}")
    # Name: example, Namespace: default IP: 10.244.2.2
    
letstry=True
# response = apps.read_namespaced_deployment_status(name=deploy_name, namespace=deploy_namespace)
# response = apps.create_namespaced_deployment(body=deploy_name, namespace=deploy_namespace)
while letstry == True:
    try:
        response = apps.create_namespaced_deployment(body=open('deploy.yaml', 'r').read(), namespace=deploy_namespace)
        response = apps.read_namespaced_deployment_status(name=deploy_name, namespace=deploy_namespace)
        if response.status.available_replicas < 0:
            print("Waiting for Deployment to become ready...")
            time.sleep(5)
        else:
            break
    except ApiException as e:
        print(f"Exception when calling AppsV1Api -> read_namespaced_deployment_status: {e}\n")
