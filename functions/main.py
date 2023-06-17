from ibmcloudant.cloudant_v1 import CloudantV1, Document
import os
import requests

def get_all_reviews(client):
    res = [d["doc"] for d in client.post_all_docs(
        db="reviews", include_docs=True
    ).get_result()["rows"]]
    return res
def find_review(client, selector):
    res = client.post_find(
        db="reviews", selector=selector
    ).get_result()
    return res
def get_requests(param_dict, client):
    res = None
    if("dealerId" in param_dict):
        res = find_review(client, {"dealership": { "$eq": int(param_dict["dealerId"])}})["docs"]
    else:
        res = get_all_reviews(client)
    return {"body": res}
def post_review(client, document):
    return client.post_document(db="reviews", document=document)
def main(param_dict):
    client = CloudantV1.new_instance()
    if("__ow_method" in param_dict and param_dict["__ow_method"] == "get"):
        return get_requests(param_dict, client)
    elif("__ow_method" in param_dict and param_dict["__ow_method"] == "post"):
        try:
            post_review(client, param_dict["review"])
            return {"body": "success" }
        except:
            return {"body": "failure" }
