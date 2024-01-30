def select_menu(data, name):
    data = dict(sorted(data.items(), key=lambda x:str(x)))
    
    options = list(enumerate(data))

    print("-" * (9 + len(name)))
    print("Select a", name)
    print("-" * (9 + len(name)))

    for index, value in options:
        print(index, value)

    option = int(input())

    key = options[option][1]

    return key, data[key]

def bool_menu(prompt):
    print("-" * (18 + len(prompt)))
    print(prompt, "[y] [n (default)]")
    print("-" * (18 + len(prompt)))
    if input() == "y":
        return True
    return False