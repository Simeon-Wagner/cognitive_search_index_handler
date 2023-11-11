import subprocess
import json
import os
import requests
import argparse
from azure.identity import AzureCliCredential

def delete_doc_from_index(
        unique_id,
        service_name, 
        subscription_id=None, 
        resource_group=None, 
        index_name="default-index", 
        credential=None, 
        admin_key=None):
    #Connection without admin key and credential is not possible.
    if credential is None and admin_key is None:
        raise ValueError("credential and admin key cannot be None")
    
    #If no admin key for the Azure tenant is passed make sure that the az login cli is installed on your PC and az login has been runned.
    if not admin_key:
        admin_key = json.loads(
            subprocess.run(
                f"az search admin-key show --subscription {subscription_id} --resource-group {resource_group} --service-name {service_name}",
                shell=True,
                capture_output=True,
            ).stdout
        )["primaryKey"]

    #Current api-version (10.11.2023) is 2020-06-30
    url = f"https://{service_name}.search.windows.net/indexes/{index_name}/docs/index?api-version={api_version}"
    headers = {
        "Content-Type": "application/json",
        "api-key": admin_key,
    }

    #deleting each file specified on its ID. The field ID can be changed based on teh key value pairs of the index
    body = {  
    "value": [  
        {  
        "@search.action": "delete",  
        "id": str(unique_id)
        }
    ]  
    }  

    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        print(f"Succesfully deleted document {unique_id} from {index_name}")
    else:
        raise Exception(f"Failed to delete index. Error: {response.text}")
    
    return True

if __name__ == "__main__":
    #Add the ID of the docs in the index you want to delete
    to_delete_item = [7077]

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=".\\config.json", help="Path to config file containing settings for data preparation")
    
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    credential = AzureCliCredential()

    #Change this if you have more than one configuration in your config.json file
    service_name = config[0]["search_service_name"]
    subscription_id = config[0]["subscription_id"]
    resource_group = config[0]["resource_group"]
    index_name = config[0]["index_name"]
    api_version = config[0]["api_version"]

    #delete each file from the index specified in the config.json by its ID
    for doc in to_delete_item:
        delete_doc_from_index(  doc,
                                service_name=service_name,
                                subscription_id=subscription_id,
                                resource_group=resource_group,
                                index_name=index_name,
                                credential=credential
                                )




