import string

start_line = ("<?xml version='1.0' encoding='UTF-8' standalone='no'?><!--Created with JFLAP "
              "7.1.--><structure>&#13;\n<type>fa</type>&#13;<automaton>&#13;\n\n")
initial_state = ("<state id='0' name='q0'>&#13;"
                 "<x>0.0</x>&#13;"
                 "<y>0.0</y>&#13;"
                 "<initial/>"
                 "</state>&#13;")
final_line = "\n</automaton>&#13;\n</structure>"
state_title = "<!--The list of states.-->&#13;\n\n"
transition_title = "\n<!--The list of transitions.-->&#13;\n"

initial_state_exists = False
words = []
states = []
transitions = []
word = ""
lowercase_alphabet = string.ascii_lowercase
x_cord = 0
y_cord = 0
prefixes = {"":(0, (x_cord,y_cord))}

print("-DFA Generator-\nKeep inputting strings and enter '0' to finish program:")
while True:

    try:
        word = input()
    except EOFError:
        break

    for letter in word:
        if letter not in lowercase_alphabet and word != "0":
            print("Error: Input not in alphabet")
            exit(2)

    if word == "0":
        break
    else:
        words.append(word)

words.sort()

y_cord = (-100 * len(words)) / 4

# Create states & transitions & start final
#     new_word = word[:3]
current_id = 0
transition_id = -1
for word in words:
    x_cord = 75
    y_cord += 50
    prefix_exists = False
    prefix = ""

    if len(word) == 0:
        y_cord -= 100
        if not initial_state_exists:
            initial_state = "<state id ='0' name='q0'>&#13;<x>0.0</x>&#13;<y>0.0</y>&#13;<initial/><final/></state>&#13;"
            initial_state_exists = True
        else:
            continue

    for index in range(len(word)):
        prefix += word[index]
        letter = prefix[len(prefix) - 1]
        current_id += 1
        # print(f"Prefix:{prefix}, Letter:{letter}, current_id:{current_id}")
        # print(f"Prefixes list: {prefixes}\nCurrent Prefix: {prefix}")
        if prefix in prefixes:
            current_id -= 1
            transition_id = prefixes[prefix][0]
            temp_cords = prefixes[prefix][1]
            if index == len(word) - 1:
                states[transition_id-1] = (
                f"<state id ='{transition_id}' name='q{transition_id}'>&#13;<x>{temp_cords[0]}</x>&#13;<y>{temp_cords[1]}</y>&#13;<final/></state"
                f">&#13;")
            else:
                prefix_exists = True
                x_cord += 75

            continue
        elif prefix_exists:
            prefix_exists = False
        else:
            transition_id = current_id - 1

        x_cord += 75

        if index == len(word) - 1:
            state = (
                f"<state id ='{current_id}' name='q{current_id}'>&#13;<x>{x_cord}</x>&#13;<y>{y_cord}</y>&#13;<final/></state"
                f">&#13;")
        else:
            state = (f"<state id ='{current_id}' name='q{current_id}'>&#13;<x>{x_cord}</x>&#13;<y>{y_cord}</y>&#13;</state"
                     f">&#13;")


        if index == 0:
            transition = (f"\n<transition>&#13; <from>0</from>&#13;"
                          f"\n<to>{current_id}</to>&#13;"
                          f"\n<read>{letter}</read>&#13;"
                          "\n</transition>&#13;\n")
        else:
            transition = (f"\n<transition>&#13; \n<from>{transition_id}</from>&#13;"
                          f"\n<to>{current_id}</to>&#13;"
                          f"\n<read>{letter}</read>&#13;"
                          "\n</transition>&#13;\n")
        prefixes_length = len(prefixes)
        prefixes[prefix] = (current_id, (x_cord, y_cord))
        states.append(state)
        transitions.append(transition)
        # print(f"State {current_id} generated for letter '{letter}' at position ({x_cord}, {y_cord})")
        # print(f"Transition created from state {current_id - 1} to state {current_id} on input '{prefix}'")

if len(words) > 0:
    print(start_line)
    print(state_title)

    print(f"{initial_state}\n")
    for state in states:
        print(f"{state}\n")

    print(transition_title)
    for transition in transitions:
        print(transition)

    print(final_line)

# if len(words) > 0:
#     with open('pythonDFA.jiff', mode="w") as file:
#         file.write(start_line)
#         file.write(state_title)
#
#         file.write(f"{initial_state}\n")
#         for state in states:
#             file.write(f"{state}\n")
#
#         file.write(transition_title)
#         for transition in transitions:
#             file.write(transition)
#
#         file.write(final_line)
