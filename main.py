from pylatex import Document, Section, Subsection, Command, Enumerate, Package
from pylatex.utils import italic, bold, NoEscape
import textract

def create_cs170_hw(num="0", author="", questions=[]):
    # Create document
    doc = Document()

    #Inclue packages
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('amssymb'))
    doc.packages.append(Package('enumitem'))

    # Make title
    title = 'CS 170 - HW %d' % (num)
    doc.preamble.append(Command('title', bold(title)))
    doc.preamble.append(Command('author', author))
    doc.preamble.append(Command('date', ''))
    doc.append(NoEscape(r'\maketitle'))

    # Instructions
    #with doc.create(Section("Instructions")) as section:
    #    section.append("N/A")

    # Create questions
    for question in questions:
        name = question[0]
        parts = question[1]
        with doc.create(Section(name)):
            if (parts > 0):
                with doc.create(Enumerate(enumeration_symbol=r"(\alph*)")) as enum:
                    for _ in range(0, parts):
                        enum.add_item("")

    # Generate Latex file
    file_name = "cs170_hw" + str(num)
    doc.generate_tex(file_name)
    print("%s.tex generated!" % (file_name))

def create_cs70_hw(num="0", author="", questions=[]):
    # Create document
    doc = Document()

    #Inclue packages
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('amssymb'))
    doc.packages.append(Package('enumitem'))

    # Make title
    title = 'CS 70 - HW %d' % (num)
    doc.preamble.append(Command('title', bold(title)))
    doc.preamble.append(Command('author', author))
    doc.preamble.append(Command('date', ''))
    doc.append(NoEscape(r'\maketitle'))

    # Sundry
    with doc.create(Section("Sundry", numbering=False)) as section:
        print("")

    # Create questions
    for question in questions:
        name = question[0]
        parts = question[1]
        with doc.create(Section(name)):
            if (parts > 0):
                with doc.create(Enumerate(enumeration_symbol=r"(\alph*)")) as enum:
                    for _ in range(0, parts):
                        enum.add_item("")

    # Generate Latex file
    file_name = "cs70_hw" + str(num)
    doc.generate_tex(file_name)
    print("%s.tex generated!" % (file_name))

# Main
print("Welcome to the Berkeley EECS Homework Generator!")

# Get inputs
author = input("What is your name? ")

create_hw = create_cs170_hw
class_name = input("What class is this for? (Format as all lowercase without spaces, e.g. cs70) ")
while (True):
    if class_name == "cs170":
        create_hw = create_cs170_hw
        break
    elif class_name == "cs70":
        create_hw = create_cs70_hw
        break
    class_name = input("Please enter a valid class. ")

hw_num = input("What number homework is this? ")
while (True):
    if hw_num.isdigit():
        break
    hw_num = input("Please enter a valid number. ")
hw_num = int(hw_num)

file_path = input("What is the file path? ")

# Try parsing the file
try:
    # extract text from the PDF file
    text = textract.process(file_path, method='pdfminer').decode('utf-8')
    lines = text.splitlines()
    print

    # Testing
    with open('test.txt', 'w+') as f:
        f.write(str(text))

    # setup
    question_list = [] # list of questions, represented as tuples
    first_question = 1 # index of first question
    question_num = first_question # current question number
    a_char = 97 # index of 'a' character
    curr_char = a_char # letter of current part
    part_count = 0 # number of parts to the quesiton
    name = "" # name of current question

    # loop through each line
    for i in range(0, len(lines)):
        line = lines[i]
        # Check if new question found
        if (line[0:2] == str(question_num) + " "):
            # If NOT the first question, append the previous question to list
            if (question_num != first_question):
                question_list.append((name, part_count))

            name = line[2:]
            question_num += 1
            curr_char = a_char
            part_count = 0

        # Alt question number formatting
        elif (line[0:1] == str(question_num)):
            # If NOT the first question, append the previous question to list
            if (question_num != first_question):
                question_list.append((name, part_count))

            #Prepare the next line to be the quesiton name
            line = lines[i+1]
            name = line[2:]
            question_num += 1
            curr_char = a_char
            part_count = 0

        # Check if next part found
        elif (line[0:3] == "(%s)" % (chr(curr_char))):
            part_count += 1
            curr_char += 1

    # Append the last question to list
    question_list.append((name, part_count))

    # Create the homework
    create_hw(hw_num, author, question_list)
except Exception as e:
    print(e)
    print("That is not a valid file path. Goodbye.")