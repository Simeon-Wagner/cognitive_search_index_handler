# cognitive_search_index_handler
Delete a document from an index within an Azure Cognitive Search Service
## Document deletion
* Add the required configurations of your Azure tenant to your config.json file.
* Enter the values of your unique identification field in the "to_delete_item" list
* Adjust the body of the http request in case the fiel id is not the unique identification field.
* Execute the script.
## Note
Make sure that you have the azure cli installed and have at least logged in once by executing the following command in your command prompt or powershell.

> az login

If you don't want to install the azure cli make sure to pass the azure admin key to the delete method. 


