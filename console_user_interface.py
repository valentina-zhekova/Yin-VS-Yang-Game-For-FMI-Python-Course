def take_user_choice(condition, wait_prompt, error_prompt, start_prompt=None,
                     function=input):
    if start_prompt:
        print(start_prompt)
    choice = function(wait_prompt)
    while not condition(choice):
        print(error_prompt)
        choice = function(wait_prompt)
    return choice


def user_input(prompt):
    return input(prompt)


def output_prompt(prompt):
    print(prompt)
