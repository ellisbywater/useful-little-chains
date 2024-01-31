from langchain.callbacks.base import BaseCallbackHandler
from pyboxen import boxen

def boxen_print(*args, **kwargs):
    print(boxen(*args, **kwargs))

class ChatModelStartHandler(BaseCallbackHandler):
    def on_chat_model_start(self, serialized, messages, **kwargs):
        print("\n\n\n============== Sending Messages ==============\n\n\n")
        for message in messages[0]:
            if message.type == "system":
                boxen_print(message.content, title="System Message", color="yellow")
            elif message.type == "human":
                boxen_print(message.content, title="Human Message", color="green")
            elif message.type == "ai" and "function_call" in message.additional_kwargs:
                call = message.additional_kwargs["function_call"]
                boxen_print(f"Running tool {call['name']} with args {call['arguments']}", title=message.type, color="cyan")
            elif message.type == "ai":
                boxen_print(message.content, title="AI Message", color="blue")
            elif message.type == "function":
                boxen_print(message.content, title="Function Message", color="magenta")
            else:
                boxen_print(message.content, title=message.type)