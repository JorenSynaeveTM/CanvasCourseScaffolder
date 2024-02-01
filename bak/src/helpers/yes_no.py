def ask_yes_no_question(prompt):
    while True:
        user_input = input(prompt + " ").strip().lower()
        if user_input in ['y', 'n']:
            return user_input == 'y'
        else:
            print("Invalid input. Please enter 'y' for Yes or 'n' for No.")
