# import os
# import google.generativeai as genai

# genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel('gemini-pro')

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load from .env

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set!")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-pro')

class Expert:
    def __init__(self, personna_definition):
        self.chat = model.start_chat(history=[])
        self.personna_definition = personna_definition
        # def setup_personna(personna_definition):
        _ = self.chat.send_message(personna_definition)
        self.name = self._get_name()

    def _get_name(self):
        response = self.chat.send_message("what is the name of the person(or title if name missing) I just gave you")
        print("Added new expert: " + response.text)
        self.name = response.text
        return self.name

    def send_message(self, question):
        response = self.chat.send_message(question)
        return response.text



# class expert
# def setup_master(master_setup_prompt, personnas):
#     genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
#     model = genai.GenerativeModel('gemini-1.5-pro')

#     master_chat = model.start_chat(history=[])
#     _ = master_chat.send_message(master_setup_prompt)
#     string_list = [str(item) for item in personnas] 
#     combined_personnas = ",".join(string_list)
#     print("----------------------------------------------------------------")
#     print("Experts count:" + str(len(string_list)))
#     _ = master_chat.send_message("Here are your experts and their associated description " + combined_personnas)
#     print("----------------------------------------------------------------")

#     # response = ceo_chat.send_message(board_question)
#     # return response.text
#     return master_chat
