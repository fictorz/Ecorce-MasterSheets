import dialogue_citoyen.library.setup_expert as setup_expert
import dialogue_citoyen.library.lawyerup.question_flow as question_flow
expert_definition = ''' You are a lawyer, acting as a mediator. Your name will be Expert.'''

def ask_experts(expert, question, print_answer):
    response = []
    local_response = expert.send_message(question)
    
    if print_answer:
        print("------------------------------------------------------------------")
        print(str(expert.name) + " thinks " + str(local_response))
    response.append(str(expert.name) + " responsed: " + str(local_response))

    return response

    expert = setup_expert.Expert(expert_definition)
    ask_experts(expert,"Aimes-tu le chocolat?", True)
ceo_chat = []
def main():
    """
    This is the main function of the program.
    """
    expert = setup_expert.Expert(expert_definition)
    ask_experts(expert,"Aimes-tu le chocolat?", True)

    case1 = '''I have noticed an accumulation of debris, including fallen branches, discarded construction materials, and general refuse, along the property line separating our properties. Additionally, there appears to be significant overgrowth of vegetation encroaching onto my property, creating an unsightly and potentially hazardous condition.'''
    case2='''The "accumulation of debris" referred to is naturally occurring yard waste, such as fallen leaves and branches, which are routinely cleared. The "discarded construction materials" are a few pieces of wood, neatly stacked and awaiting disposal. The "overgrowth" is minimal and consists of a few stray vines, which I will address. However, I believe they are exaggerating the issue to create a problem. I will also state that debris from their tree falls onto my property.'''
    contract_template = """
    CONTRACT AGREEMENT

    Date: [DATE]
    Parties: User 1 and User 2

    Clause 1: Payment Terms
    [PAYMENT_TERMS]

    Clause 2: Delivery and Acceptance
    [DELIVERY_TERMS]

    Clause 3: Warranty
    [WARRANTY_TERMS]

    Clause 4: Dispute Resolution
    [DISPUTE_RESOLUTION_TERMS]

    Signatures:
    _________________________ (User 1)
    _________________________ (User 2)
    """

    #contract_template
    answer = question_flow.question_flow(expert, case1, case2, False)
    with open("summary.pdf", "wb") as file:
        file.write(answer.read())
    print(answer)
if __name__ == "__main__":
    main()