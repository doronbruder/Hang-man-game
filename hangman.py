import hangman_helper


def create_abc_lst():
    """This function creates abc-list"""
    abc_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o'
        , 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    return abc_list



def create_empty_pattern(word_length):
    """This function create an empty pattern with a length of a chosen word"""
    pattern =""
    for i in range(word_length):
        pattern +='_'
    return pattern




def update_word_pattern(word,pattern,letter):
    """This fucntion reveals an appropiate letter in the pattern when the user is guessing right"""

    pattern=list(pattern)  # convert the pattern from a string to list

    # checks if the the secret word contain the letter
    for j in range(len(word)):
        if letter==word[j]:
            pattern[j]=letter # updates the appropiate place in the pattern

    pattern="".join(pattern)

    return pattern




def set_game_parameters(words_list):
    """This function sets the default parameters for the start of a game """

    word = hangman_helper.get_random_word(words_list) # sets randomally the secret word from the words list

    wrong_guess_lst = [] # sets the wrong guesses of the user to start empty

    error_count = 0 # sets  the error counter to start as zero

    pattern = create_empty_pattern(len(word)) # creates an empty pattern

    msg = hangman_helper.DEFAULT_MSG # updates the message to be the default for a  start situation

    return error_count, msg, pattern, word, wrong_guess_lst





def letter_is_valid(guess_letter):
    if type(guess_letter) is not str or len(guess_letter) != 1 or not guess_letter.islower():
        return True
    else:
        return False



def already_chosen(guess_letter,pattern,wrong_guess_lst):
    if guess_letter in wrong_guess_lst or guess_letter in pattern:
        return True
    else:
        return False




def user_entered_letter(input_type):

    if input_type == hangman_helper.LETTER:
        return True

    return False




def get_hint(error_count, msg, pattern, wrong_guess_lst):

    words = hangman_helper.load_words("words.txt")  # loads the words to a list

    filtered_words = filter_words_list(words, pattern, wrong_guess_lst)  # filters the words that fit to the pattern

    hint_letter = choose_letter(filtered_words, pattern)  # defines the best letter for a hint

    msg = hangman_helper.HINT_MSG + hint_letter  # update the  hint msg to the user

    hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg, ask_play=False)

    return msg






def run_single_round(error_count, msg, pattern, word, wrong_guess_lst):
    """This function runs a single round of the game """

    # if the user didnt go wrong 6 times or didnt win the game continues
    while (pattern != word) and (error_count < hangman_helper.MAX_ERRORS):

        # sets the game the game with the right default values
        hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg,ask_play=False)

        input_type, input_value = hangman_helper.get_input() # input function from an imported graphic class

        # if the user puted in a char
        if user_entered_letter(input_type):
            guess_letter = input_value # updates the guess to this letter


            # checks if the char is a valid letter for this game
            if letter_is_valid(guess_letter):
                msg = hangman_helper.NON_VALID_MSG  # if it isnt a valid char the user gets a message

            # if the guess is already chosen the user gets an appropiate message
            elif already_chosen(guess_letter,pattern,wrong_guess_lst):
                msg = hangman_helper.ALREADY_CHOSEN_MSG+guess_letter

            # if the guess is right  and the user tried it for the first time it revealed
            elif guess_letter in word:
                pattern= update_word_pattern(word,pattern,guess_letter)
                msg = hangman_helper.DEFAULT_MSG

            # the only left option is that the guess is wrong so the error  list & counter updated and the user
            else:
                error_count += 1
                wrong_guess_lst.append(guess_letter)
                msg = hangman_helper.DEFAULT_MSG


        # case when the user pressed on the hint buttom
        elif input_type== hangman_helper.HINT:

            msg = get_hint(error_count, msg, pattern, wrong_guess_lst)

    return error_count, pattern


def run_single_game(words_list):
    """This function runs the hangman game"""

    # sets appropiate parameters
    error_count, msg, pattern, word, wrong_guess_lst = set_game_parameters(words_list)

    # updates the error count and the pattern according the results of a single round
    error_count, pattern = run_single_round(error_count, msg, pattern, word, wrong_guess_lst)

    # if the the user reveals the secret word from the pattern  he gets a winning screen
    if pattern==word:
        msg=hangman_helper.WIN_MSG
        hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg,ask_play=True)

    # if the user went wrong above maximum times(6) he gets losing msg
    elif error_count==hangman_helper.MAX_ERRORS:
        msg=hangman_helper.LOSS_MSG+word
        hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg,ask_play=True)









def filter_words_list(words, pattern, wrong_guess_lst):

    hint_words = []

    # goes through all the potential words for a hint
    for word in words:

        flag = True

        # checks that the words length are equal
        if len(word) != len(pattern):
            continue

        # checks that the words do not contain letters from the bad list
        for letter in wrong_guess_lst:
            if letter in word:
                flag = False
                break

        if flag:
            # checks that all the letters are in the right place or not uncovered
            for index in range(len(word)):
                if not word[index] == pattern[index] and not pattern[index] == '_':
                    flag = False
                    break
        if flag:
            # checks that there are no double letters- even if the letter shown in the pattern
            for i in range(len(pattern)):
                if pattern[i] == "_" and word[i] not in pattern:
                    flag=True
                elif pattern[i]==word[i]:
                    flag=True
                else:
                    flag=False
                    break

        # if the word passes all the filters  add it to the list
        if flag:
            hint_words.append(word)

    # return all the possible hint words
    return hint_words





def choose_letter(words, pattern):
    """This function finds the most common letter in a list of words and make sure its not in the pattern already"""

    max=0
    abc_list = create_abc_lst() # creates abc list
    counter_lst=[0]*26 # a list that will count each letter in the words list that

    # checks which letters are in the words list but not in the pattern and updates the indexes
    for word in words:
        for letter in word:
            for i in range(len(abc_list)):
                if letter==abc_list[i] and not letter in pattern:
                    counter_lst[i]+=1

    # finds the maximal index
    for j in range(len(counter_lst)):
        if counter_lst[j]>counter_lst[max]:
            max=j

    return abc_list[max]





def main():
    """This function activate the game"""
    words_list=hangman_helper.load_words("words.txt") # load words list  from an external file
    wanna_play = True

    while wanna_play:
        run_single_game(words_list) # runs the game
        # every time a game is finished  the user gets a screen that offers a new game
        input_type, wanna_play = hangman_helper.get_input()






if __name__ == "__main__":
    hangman_helper.start_gui_and_call_main(main)
    hangman_helper.close_gui()
