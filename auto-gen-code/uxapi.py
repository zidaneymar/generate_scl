
from pprint import pprint
import requests
import types
# from interface import Entity
# from interface import Action
# from interface import Service


class uxapi:
    BASE_URL = 'https://uxapi.botletstore.com/api'
    DEV_TOKEN = "49b9f5d4-b660-41cb-9550-aa4c40f16bbd"
    HEADERS = {"Authorization" : "token:%s" % DEV_TOKEN}
    def get_entity_type(self, entity_name):
        invoke_url = self.BASE_URL + "/EntityType/%s" % entity_name
        r = requests.get(invoke_url, headers = self.HEADERS).json()
        return r
    
    def get_modules_info(self, namespace):
        invoke_url = self.BASE_URL + "/modules/%s" % namespace
        r = requests.get(invoke_url, headers = self.HEADERS).json()
        return r
    
    def get_organization_info(self, organization):
        invoke_url = self.BASE_URL + "/organizations/%s" % organization
        r = requests.get(invoke_url, headers = self.HEADERS)
        return r.json()

    def get_all_under_org(self, organization):
        invoke_url = self.BASE_URL + "/organizations/%s/modules" % organization
        r = requests.get(invoke_url, headers = self.HEADERS)
        return r.json()



# if __name__ == "__main__":
#     from interface import Entity
#     from interface import Action
#     from interface import Service
# #     a = uxapi()


#     print str(a.get_all_service_under_org("qikang")[0])


#     print ("\r\n")

# # We have three iterating
#     entity = a.get_all_service_under_org("qikang")[0].actions[0].input_params[0]
#     extract_entities(entity)