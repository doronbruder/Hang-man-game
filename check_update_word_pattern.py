from hangman import update_word_pattern

def check_update_word_pattern():
    """This function test the check&update function"""

    # checks if pattern updated in multiple indexes if needed
    if update_word_pattern("door",'____','o')=='_oo_':
        # make sure pattern doesnt changed when the letter isnt in the word
        if update_word_pattern('apple','_____','z')=='_____':
            # make sure pattern doesnt changed when the chosen letter already uncovered
            if update_word_pattern('b','b__k','b')=='b__k':
                # still works when the pattern consist of single letter
                if update_word_pattern('xxx','___','x')=='xxx':
                    print("The function passed the test")
                    return True

    print("There was a problem , fuction faild")
    return False




if __name__=="__main__":
    check_update_word_pattern()


