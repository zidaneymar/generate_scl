
from uxapi import uxapi
from interface import Entity
from interface import Action
from interface import Service


class Tools:
    api = uxapi()

    entities_global = []

    def get_all_service_under_org(self, organization):
        r = self.api.get_all_under_org(organization)
        result = []
        for module in r:
            if module["@"] == "mst.bot.service":
                # result.append(module)
                unit_service = Service(module)
                result.append(unit_service)
                
        return result
        

    def extract_entities(self, entity_param):
        entities = entity_param.get_sub_entites()
        for entity in entities:
            if not entity.is_unit_type():
                self.extract_entities(entity)
            else:
                self.entities_global.append(entity)
        results = self.entities_global
        self.entities_global = []
        return results


        # for service in get_all_service_under_org("qikang"):
        #     #print str(service)
        #     print service.description
        #     for action in service.actions:
        #         #print str(action)
        #         print action.name
        #         for each_input in action.input_params:
        #             extract_entities(each_input)
        #         for entity in entities_global:
        #             print str(entity)
        #         entities_global = []



# entity = get_all_service_under_org("qikang")[0].actions[0].input_params[0]
# extract_entities(entity)

# for entity in entities_global:
#     print str(entity)


# entity = get_all_service_under_org("swagger_test")[1].actions[0].input_params[0]
# extract_entities(entity)
# for entity in entities_global:
#     print str(entity)