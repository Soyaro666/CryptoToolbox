from qrandom import QRandom
from file_encryption import Crypter


def get_integer(**params):
    try:
        text = params.get("text", "enter number from above list")
        choice = params.get("default", 0)
        tmp_input = ''
        if choice is not None:
            print(text)
            tmp_input = input(f"leave empty for {choice}:")
        else:
            tmp_input = input(text+":")
        if tmp_input != '':
            choice = int(tmp_input)
    except ValueError:
        print("not a number")
    else:
        return choice


def print_list(options: list):
    print("")
    for index in range(1, len(options)):
        print(f"{index}.: {options[index]}")
    print(f"0.: {options[0]}\n")


def main():
    license = open("LICENSE", "r")
    lines = license.readlines()
    for line in lines:
        print(line)
    rng_obj = QRandom()
    choice = 999
    params = {}
    while choice > 0:
        print("What do you want to do?")
        options = ["exit",
                   "output random number in range",
                   "Generate a random Password",
                   "encode a file",
                   "play rock, paper, scissors"]
        print_list(options)
        choice = get_integer()
        if not 0 <= choice < len(options):
            print("not an option")
            choice = 999
            input("press enter to continue")
        elif choice == 1:
            first = get_integer(text="enter first number of range",
                                default=1024)
            second = get_integer(text="enter second number of range (optional)",
                                 default=None)
            if first == 0 and second == 0:
                print("42, joker.")
            else:
                if first is not None and first != '' and first != 0:
                    params["min"] = first
                else:
                    params["min"] = 1024
                if second is not None and second != '' and second != 0:
                    params["max"] = second
                else:
                    params["max"] = 0
                print(rng_obj.get(min=params["min"], max=params["max"]))
            choice = 999
            input("press enter to continue")
        elif choice == 2:
            full_charset = QRandom.alphabet()
            length = None
            while length is None:
                print("Note: A password must have 4 or more digits")
                length = get_integer(text="enter length of password",
                                     default=16)
                if not 4 <= length:
                    print(f"{length} is too small")
                    length = None
                    input("press enter to continue")
            password = None
            choice = 999
            charset = []
            while choice > 0:
                options = ["generate",
                           "lowercase characters",
                           "uppercase characters",
                           "numbers",
                           "special characters"]
                print_list(options)
                choice = get_integer()
                if not 0 <= choice < len(options):
                    print("not an option")
                    choice = 999
                    input("press enter to continue")
                else:
                    if choice == 0:
                        if len(charset) == 0:
                            password = rng_obj.generate_pwd(num=length)
                        else:
                            password = rng_obj.generate_pwd(num=length, charset=charset)
                        print("Your generated Password:")
                        print(password+"\n")
                        input("press enter to continue")
                    if choice == 1:
                        for string in full_charset:
                            if string.isalpha() and charset.index(string) == -1:
                                charset.append(string.lower())
                    if choice == 2:
                        for string in full_charset:
                            if string.isalpha() and charset.index(string) == -1:
                                charset.append(string.upper())
                    if choice == 3:
                        for string in full_charset:
                            if string.isnumeric() and charset.index(string) == -1:
                                charset.append(string)
                    if choice == 4:
                        for string in full_charset:
                            if not (string.isalpha()
                                    or string.isnumeric()
                                    or charset.index(string) != -1):
                                charset.append(string)
            choice = 999
        elif choice == 3:
            choice = 999
            source_file = None
            output_file = None
            key_file = None
            while choice > 0:
                options = ["encrypt", f"set Source-File (required, currently {source_file})"]
                if source_file is None:
                    options.append(f"set Output-File (optional, currently {output_file})")
                    options.append(f"set Keyfile (optional, currently {key_file})")
                else:
                    if output_file is None:
                        options.append(f"set Output-File (optional, currently {source_file}.out)")
                    else:
                        options.append(f"set Output-File (optional, currently {output_file})")
                    if key_file is None:
                        options.append(f"set Keyfile (optional, currently {source_file}.key)")
                    else:
                        options.append(f"set Keyfile (optional, currently {key_file})")
                print_list(options)
                choice = get_integer()
                if not 0 <= choice < len(options):
                    print("not an option")
                    choice = 999
                elif choice > 0:
                    selection = ''
                    if choice == 1:
                        selection = "Source-File"
                    elif choice == 2:
                        selection = "Output-File"
                    else:
                        selection = "Key-File"
                    print(f"Please enter a {selection} including it's path.")
                    print("This program can handle relative and absolute paths.")
                    print("If the file is stored inside this programs folder you ",
                          "can just enter the filename without a path")
                    print("If you type None the current setting for this file will ",
                          "be reset to default. 'None' is case sensitive.")
                    filename = input("[path/]file:")
                    if filename == "None":
                        filename = None
                    if choice == 1:
                        source_file = filename
                    elif choice == 2:
                        output_file = filename
                    elif choice == 3:
                        key_file = filename
                elif source_file is None:
                    choice = 999
                    print("a Source-File is required.")
                else:
                    params = {"input_file": source_file}
                    if output_file is None:
                        params["output_file"] = f"{source_file}.out"
                    else:
                        params["output_file"] = output_file
                    if key_file is None:
                        params["key_file"] = "None"
                    else:
                        params["key_file"] = key_file
                    response = Crypter.encode(input_file=params["input_file"],
                                              output_file=params["output_file"],
                                              key_file=params["key_file"])
                    print(response)
                    input("press enter to continue")
            choice = 999
        elif choice == 4:
            player_choice = 4
            options = ["exit", "rock", "paper", "scissors"]
            print("\nWhat does this have to do with a CryptoToolbox, you may ask.")
            print("Simple: you're manually giving a number. This will be compared to",
                  "a number from the quantum random generator.")
            print("If your number is one bigger than the random one you win.")
            print("if your number is one smaller than the random one you lose.")
            print("if the numbers are equal it's a draw, nobody wins or loses.")
            while player_choice > 3:
                print("\nReady?")
                print_list(options)
                player_choice = get_integer()
                if not 0 <= player_choice < len(options):
                    print("not an option")
                    choice = 999
                    input("press enter to continue")
                elif player_choice > 0:
                    print(f"\nyou chose {options[player_choice]}")
                    npc_choice = int(round(rng_obj.get(min=1, max=3), 0))
                    print(f"I chose {options[npc_choice]}")
                    diff = npc_choice - player_choice
                    if diff < -1:
                        diff += 3
                    if diff > 1:
                        diff -= 3

                    if diff == 0:
                        print("pass, we chose the same.")
                    elif diff > 0:
                        print(f"I win, {options[npc_choice]} over {options[player_choice]}")
                    elif diff < 0:
                        print(f"You win, {options[player_choice]} over {options[npc_choice]}")
                    player_choice = 4


if __name__ == '__main__':
    main()
