import random

def load_bully():
    with open("res/bully.txt", 'r') as file:
        bully_list = file.readlines()
    bully_list = [line.strip() for line in bully_list]
    return bully_list


def load_statements():
    with open("res/statements.txt", 'r') as file:
        statement_list = file.readlines()
    statement_list = [line.strip() for line in statement_list]
    return statement_list


def load_questions():
    with open("res/questions.txt", 'r') as file:
        question_list = file.readlines()
    question_list = [line.strip() for line in question_list]
    return question_list


bully_phrases = load_bully()
statement_phrases = load_statements()
question_phrases = load_questions()

bully_string = random.choice(bully_phrases)
statement_string = random.choice(statement_phrases)
question_string = random.choice(question_phrases)


if not statement_phrases:
    statement_phrases = load_statements()


        # Here we construct our final bulling sentence.It combines with two parts:
        # if main punch (bully) is question (has ?), then we combine random questions with random bully punch.
        # if not then we combine random statement with random bully punch, and finally
        # we replace our placeholders for <bully> and <victim> with usernames


if bully_string.find('?') != -1:
    sentence = question_string + ' ' + bully_string
else:
    sentence = statement_string + ' ' + bully_string


bully = "kolya"
victim = "petya"

sentence = sentence.replace("<bully>", bully)
sentence = sentence.replace("<victim>", victim)

print(sentence)