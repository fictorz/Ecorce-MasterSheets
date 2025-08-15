# from dialogue_citoyen.library.setup_expert import setup_expert
import library.setup_expert as setup_expert_module
import library.lawyerup.generate_contract as generate_contract

def ask_experts(expert, question, print_answer):
    response = []
    local_response = expert.send_message(question)
    
    if print_answer:
        print("------------------------------------------------------------------")
        print(str(expert.name) + " thinks " + str(local_response))
    response.append(str(expert.name) + " responsed: " + str(local_response))

    return response


def question_flow(expert, case1, case2, print_answer):

    
    # to pass model or expert. genai.configure(api_key=GOOGLE_API_KEY)
    # import google.generativeai as genai
    # genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
    # model = genai.GenerativeModel('gemini-2.0-flash')
    local_response = expert.send_message(case1 + " " + case2)
    if print_answer:
        print("response: " + local_response)
    legal_name1 = ""
    legal_name2 = ""
    return local_response # question_flow_with_legal_name(expert, legal_name1, case1, legal_name2, case2, print_answer)

def question_flow_with_legal_name(expert, legal_name1, case1, legal_name2, case2, print_answer):
    # response = []
    case1_introduction = '''Here is the legal case for customer 1'''
    complaint1 = case1_introduction + ' ' + legal_name1 + ' ' + case1
    # local_response = expert.send_message(case1_introduction + ' ' + case1)
    # if print_answer:
    #     print("response: " + local_response)

    case2_introduction = '''Here is the legal case for customer 2'''
    complaint2 = case2_introduction + ' ' + legal_name2 + ' ' + case2
    # local_response = expert.send_message(case2_introduction + ' ' + case2)
    # if print_answer:
    #     print("response: " + local_response)


    # legal_template_introduction = '''Provide an expert mediation text from the two cases'''
    # local_response = expert.send_message(legal_template_introduction)
    # if print_answer:
    #     print("response: " + local_response)
    local_response = ""

    python_pdf = generate_contract.generate_redacted_contract(legal_name1, legal_name2, complaint1, complaint2, local_response) #, local_response)

    return python_pdf

def lawyerup_process(legal_name1, case1, legal_name2, case2, print_answer):
    expert_definition = ''' You are a lawyer, acting as a mediator. Your name will be Expert.'''

    expert = [] #setup_expert.Expert(expert_definition)
    
    return question_flow(expert, legal_name1, case1, legal_name2, case2, print_answer)
    
