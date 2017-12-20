from uxapi import uxapi

class Entity:
    entity_whitelist = ["$mst.auth.api_key", "mst.auth.api_key", "$mst.secret", "mst.secret"]
    def __init__(self, json):
        self.name = json["name"]
        self.type = json["type"]
        self.description = json["description"]
        self.list_tag = False
        self.sub_entities = self.get_sub_entites()

    @staticmethod
    def get_sub_entities_of_an_entity(entity_type):
        result = []
        api = uxapi()
        entity_info = api.get_entity_type(entity_type)
        if "fields" in entity_info and entity_info["fields"]:
            for entity in entity_info["fields"]:
                entity_obj = Entity(entity)
                result.append(entity_obj)
        return result

    @staticmethod
    def iterate_parents(entity_type):
        api = uxapi()
        if entity_type[0] == "$":
            entity_type = entity_type[1:]
        entity_info = api.get_entity_type(entity_type)

        if "parents" in entity_info and entity_info["parents"]:
            parent_type = entity_info["parents"][0]
            return Entity.iterate_parents(parent_type)
        result = []
        if "fields" in entity_info and entity_info["fields"]:
            for entity in entity_info["fields"]:
                entity_obj = Entity(entity)
                result.append(entity_obj)
        return result

    def is_unit_type(self):
        
        if self.type[0] != "$":
            return True
        else:
            return False
    def is_disabled(self):
        if self.type in Entity.entity_whitelist:
            return False
        for each_type in ["mst", "msp", "$mst", "$msp", "mso", "$mso"]:
            if str(self.type).startswith(each_type):

                print "### We don't support this type: %s" % self.type
                return True
        return False
    def is_list(self):
        if str(self.type).startswith("list"):
            return True
        return False

    def get_sub_entites(self):
        api = uxapi()
        result = []


        if not self.is_unit_type() and not self.is_disabled():
            entity_type = self.type[1:]
            entity_info = api.get_entity_type(entity_type)

            # result += Entity.iterate_parents(self.type)
            if "parents" in entity_info and entity_info["parents"]:
                parent_info = api.get_entity_type(entity_info["parents"][0][1:])
                parent_json = {
                    "@": parent_info["@"],
                    "type": "$" + parent_info["type_id"],
                    "name": "parent",
                    "description": parent_info["description"] 
                }
                if not "fields" in entity_info or not entity_info["fields"]:
                    entity_info["fields"] = [parent_json]
                else: 
                    entity_info["fields"].append(parent_json)
            if "fields" in entity_info and entity_info["fields"]:
                for entity in entity_info["fields"]:
                    entity_obj = Entity(entity)
                    result.append(entity_obj)
            return result
        elif self.is_list():
            self.type = self.type[5:-1]
            self.list_tag = True
            return self.get_sub_entites()
        else:
            return result
    def __str__(self):
        entity_info = "Entity Name: %s, Entity Type: %s, Entity Description: %s" % (self.name, self.type, self.description)
        sub_entity_info = ""
        for sub in self.sub_entities:
            sub_entity_info += " %s " % sub.name
        return entity_info + sub_entity_info
    # WARNING: Very Slow Implementation
    # def get_all_sub_entities(self):
    #     results = self.get_sub_entites()
    #     for result in results:
    #         if not result.is_unit_type():
                
        
class Action:
    def __init__(self, json):
        self.name = json["id"]
        self.description = json["description"]
        self.input_params = []
        self.output_params = []
        if "inputs" in json:
            for param in json["inputs"]:
                unit_param = Entity(param)
                self.input_params.append(unit_param)
        if "outputs" in json:
            for param in json["outputs"]:
                unit_param = Entity(param)
                self.output_params.append(unit_param)
    def __str__(self):
        action_info = "Action Name :%s, Action Desc: %s \r\n" % (self.name, self.description)
        input_info = "Input_Params: \r\n"
        for param in self.input_params:
            input_info += str(param)
            input_info += "\r\n"
        output_info = "Output_Params: \r\n"
        for param in self.output_params:
            output_info += str(param)
            output_info += "\r\n"
        
        return action_info + input_info + output_info
class Service:
    def __init__(self, json):
        self.description = json["description"]
        self.id = json["id"]
        self.actions = []
        if "actions" in json:
            for action in json["actions"]:
                action_obj = Action(action)
                self.actions.append(action_obj)
    def __str__(self):
        service_info = "Service Desc: %s \r\n" % (self.description)
        actions_info = "Actions: \r\n"
        for action in self.actions:
            actions_info += str(action)
            actions_info += "\r\n"
        
        return service_info + actions_info
        



