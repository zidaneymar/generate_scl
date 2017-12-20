

from gen_tools import Tools
from interface import Entity
from interface import Action
from interface import Service

class Environment:
    def __init__(self):
        self.v_pool = []

class Variable():
    def __init__(self, entity):
        self.entity = entity
        self.token = None
    def add_to_env(self, env):
        env.v_pool.append(self)
        # if not self.entity.list_tag:
        self.token = "v_" + str(len(env.v_pool))
        # else:
        #     self.token = "l_" + str(len(env.v_pool))
# def generate_v_name(node):
#     if isinstance(node, Entity):
#         return 

def instantiation(node, env):
    if isinstance(node, Entity):
        return Variable(node)

# Avoid using unique name, but generate from an env

def generate_declaration(node, env):
    if isinstance(node, Entity):
        if node.is_unit_type() or node.is_disabled():
            return ""
        str1 = "CREATE \"%s\"" % node.type
        before = len(env.v_pool) - len(node.sub_entities) + 1
        for sub_node in node.sub_entities:
            if len(sub_node.sub_entities) and sub_node.list_tag:
                before -= len(sub_node.sub_entities)

        for sub_node in node.sub_entities:
            if not sub_node.list_tag:
                str1 += (" , %s = %s" % (sub_node.name, "v_%d" % before))
                before += 1
            else:
                before += len(sub_node.sub_entities)
                str1 += (" , %s = %s" % (sub_node.name, "[v_%d]" % before))
                before += 1
                
        new_variable = Variable(node)
        new_variable.add_to_env(env)
        str1 += " STORE %s\r\n" % new_variable.token
        return str1

def generate_get_input_for_basic_type(node, env):
    if isinstance(node, Entity):
        #res = "SET type = \"%s\"\r\n" % node.type
        #res += "SET hints = \"%s\"\r\n" % node.description
        #res += generate_declaration(node)
        res = say("Please enter a type of '%s', see description: '%s'" % (node.type, node.description))
        res += "\r\nGET_INPUT\r\n"
        new_variable = Variable(node)
        new_variable.add_to_env(env)
        res += "SET %s = USER_INPUT\r\n\r\n" % new_variable.token
        return res

def generate_get_input(node, env):
    if isinstance(node, Entity):
        res = ""
        if not node.is_unit_type() and not node.is_disabled():
            for entity in node.sub_entities:
                if entity.is_unit_type():
                    res += generate_get_input_for_basic_type(entity, env)
                else:
                    res += say("Please input details of this custom entity name: %s, type: %s, description: %s" % (entity.name, entity.type, entity.description))
                    # before_index = len(env)
                    res += generate_get_input(entity, env)
                    # After gnerate all children types, creating a new complex type
                    #res += generate_declaration(entity, env)
            res += generate_declaration(node, env)
            return res
        elif node.is_unit_type():
            res += generate_get_input_for_basic_type(node, env)
            return res
        else:
            return res

def generate_call(service, action, env):
    if isinstance(action, Action) and isinstance(service, Service):
        token_map = {}
        res = ""
        for input_param in action.input_params:
            res += generate_get_input(input_param, env)
            # res += generate_declaration(input_param, env)
            if not input_param.is_disabled():
                if not input_param.list_tag:
                    token_map[input_param.name] = ("v_" + str(len(env.v_pool)))
                else:
                    token_map[input_param.name] = ("[v_%s]" % str(len(env.v_pool)))
                    #token_map[input_param.name] = ("[l_%s]" % str(len(env.v_pool)))
        res += "CALL \"%s\", \"%s\"" % (service.id, action.name)
        for key in token_map:
            
            res += ", %s = %s" % (key, token_map[key])
        res += "\r\n"
        res += generate_call_error(token_map)
        res += generate_call_result(token_map)
        return res
        #for input_param in action.input_params:
def generate_call_result(token_map):
    res = "SAY CALL_RESULT\r\n"
    res += "SET call_feedback = CALL_RESULT\r\n"
    res += generate_feedback(token_map)
    return res
def generate_call_error(token_map):
    res = "ON_ERROR\r\n"
    res += "SAY CALL_ERROR\r\n"
    res += "SET call_feedback = CALL_ERROR\r\n"
    res += generate_feedback(token_map)
    res = res.replace("\r\n", "\r\n    ")
    res = res[:-4]
    return res

def generate_feedback(token_map):
    res = say("Is this action working properly?")
    res += "CREATE \"$qikang.empty\" STORE empty\r\n"
    res += "RENDER empty, actions = [yes_button, no_button, not_sure_button], renderer_id = \"qikang.empty_renderer\"\r\n"
    res += "GET_INPUT\r\n"
    res += "SET feed_back = \"Feedback: ${USER_INPUT}\"\r\n"
    res += "SET param = \"Param : "
    for key in token_map:
        res += "%s: ${%s}, " % (key, token_map[key])
    res = res[:-2]
    res += "\"\r\n"
    res += "SET res = \"Result : ${call_feedback}\"\r\n"
    res += "SET action_details = \"[TEST BOT LOG] Action:update_pet_with_form\"\r\n"
    res += "SET log = \"${action_details}, ${feed_back}, ${param}, ${res}\"\r\n"
    res += "LOG \"${action_details}, ${feed_back}, ${param}, ${res}\"\r\n"
    res += say("We have received your feedback: ${log}")
    res += "GO start\r\n"
    return res


def create_button(label, input_name, button_name):
    return "CREATE \"$mst.bot.action\", label=\"%s\", input=\"%s\" STORE %s\r\n" % (label, input_name, button_name)

def say(something):
    something = something.replace("\r\n", " ").replace("\n", " ")
    something = something.replace("\"", "\\\"")
    return "SAY \"%s\"\r\n" % str(something)

def get_input():
    return "GET_INPUT\r\n"

def render(action_names):
    res = "CREATE \"$qikang.empty\" STORE empty\r\n"
    res += "RENDER empty, actions = ["
    for name in action_names:
        res += "%s, " % name
    res = res[:-2]
    res += "], renderer_id = \"qikang.empty_renderer\"\r\n"
    return res


def scl_if(expression, then, scl_elif = None, scl_elif_then = None, scl_else_then = None):
    res = "IF %s\r\n" % expression
    res += "    %s\r\n" % then
    if scl_elif and scl_elif_then:
        res += "ELIF %s\r\n" % scl_elif
        res += "    %s\r\n" % scl_elif_then
    if scl_else_then:
        res += "ELSE\r\n"
        res += "    %s\r\n" % scl_else_then
    return res
def generate_actions_choices(service):
    if isinstance(service, Service):
        res = say("Please choose an action from below:")
        action_names = []
        for action in service.actions:
            res += create_button(action.name, action.name, action.name)
            action_names.append(action.name)
        res += render(action_names)
        res += get_input()
        for action in service.actions:
            res += scl_if("USER_INPUT == \"%s\"" % action.name, "GO %s" % action.name)
        return res
               
def generate_feedback_buttons():
    res = ""
    res += create_button("Yes", "Yes", "yes_button")
    res += create_button("No", "No", "no_button")
    res += create_button("Not sure", "Not sure", "not_sure_button")
    return res

# def get_unique_name(node):
#     if isinstance(node, Entity):
#         unique_name = node.type + "_" + node.name
#         unique_name.replace("$", "")
#         return unique_name 


tools = Tools()
env = Environment()
for service in tools.get_all_service_under_org("qikang.gen1"):
        #print str(service)
        print generate_feedback_buttons()
        print generate_actions_choices(service)

        for action in service.actions:

            print "%s:\r\n" % action.name
            print  say("Now we are testing action, action name: %s, action description: %s" % (action.name, action.description))
            #print str(action)
            #print action.name
            print generate_call(service, action, env)
                # Now we have the param






