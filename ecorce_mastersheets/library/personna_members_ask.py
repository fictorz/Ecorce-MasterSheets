import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

def request_personna(personna_definition, board_question):
    chat = model.start_chat(history=[])
    # def setup_personna(personna_definition):
    _ = chat.send_message(personna_definition)
    #  print(response.text)
    response = chat.send_message(board_question)
    return response.text


# chat = model.start_chat(history=[])
# response = chat.send_message("Make sure to answer with yes and no to the following questions")
# print(response.text)
# response = chat.send_message("Do you like apples")
# print(response.text)
# response = chat.send_message("Can you elaborate")
# print(response.text)

# chat2 = model.start_chat(history=[])
# response = chat2.send_message("Break down the following problem in two specific tasks separated by this string 'dsdsada'")
# print(response.text)
# response = chat2.send_message("I have back pain")
# print(response.text)
# # response = chat.send_message("Now explain it like I a Physics PhD student")
# # print(response.text)