from LLMManager import LLMManager

object_names = ['005_tomato_soup_can', '011_banana', '009_gelatin_box', '035_power_drill', '037_scissors']

for i in range(5):
    prompt = "I need a drill"
    print(LLMManager().process_input(prompt, object_names))

for i in range(5):
    prompt = "I am hungry"
    print(LLMManager().process_input(prompt, object_names))

for i in range(5):
    prompt = "I want to make birthday decorations"
    print(LLMManager().process_input(prompt, object_names))

for i in range(5):
    prompt = "I want to send a rocket"
    print(LLMManager().process_input(prompt, object_names))