import ecorce_mastersheets.library.setup_expert as setup_expert
import ecorce_mastersheets.library.lawyerup.question_flow as question_flow
expert_definition = ''' Tu es un expert dans la distribution, la ventes pour des petits marchés et la production de produits. Tu auras la mission de livrer des rendements, statistiques ou justifications sur la ou les questions à venir.'''

def ask_experts(expert, question, print_answer):
    response = []
    local_response = expert.send_message(question)
    
    if print_answer:
        print("------------------------------------------------------------------")
        print(str(expert.name) + " thinks " + str(local_response))
    response.append(str(expert.name) + " responsed: " + str(local_response))

    return response

    # expert = setup_expert.Expert(expert_definition)
    # ask_experts(expert,"Aimes-tu le chocolat?", True)
ceo_chat = []

def main():
    """
    This is the main function of the program.
    """
    expert = setup_expert.Expert(expert_definition)
    ask_experts(expert,"Qui offre les meilleurs prix de legumes?", True)

    case1 = '''File1.xlsx'''
    case2 = '''File2.xlsx'''

    #contract_template
    answer = question_flow.question_flow(expert, case1, case2, False)
    with open("summary.pdf", "wb") as file:
        file.write(str(answer).encode("utf-8")) # .read())
    print(answer)
if __name__ == "__main__":
    main()




    # contract_template = """
    # CONTRACT AGREEMENT

    # Date: [DATE]
    # Parties: User 1 and User 2

    # Clause 1: Payment Terms
    # [PAYMENT_TERMS]

    # Clause 2: Delivery and Acceptance
    # [DELIVERY_TERMS]

    # Clause 3: Warranty
    # [WARRANTY_TERMS]

    # Clause 4: Dispute Resolution
    # [DISPUTE_RESOLUTION_TERMS]

    # Signatures:
    # _________________________ (User 1)
    # _________________________ (User 2)
    # """