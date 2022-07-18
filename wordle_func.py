import random, sys

def check_word(guess, answer, num_letters, hint_tuple):
    """
    We will return a string with each letter having the following meaning:
    hint_tuple[0]: Letter is in the right place.
    hint_tuple[1]: Letter is in the wrong place.
    hint_tuple[2]: Letter is not found.
    """
    # Convert everything to uppercase.
    guess_list = list(guess.upper())
    answer_list = list(answer.upper())
    # hint_list starts with all "letters not found".
    hint_list = list(hint_tuple[2] * num_letters)
    # print(guess_list)
    # print(answer_list)
    # print(hint_list)
    # Look for characters that are in the right place. We must check this first before looking
    # for characters that are in the wrong place.
    for idx, _ in enumerate(guess_list):
        if guess_list[idx] == answer_list[idx]:
            # Put the "right place" hint into hint_list.
           hint_list[idx] = hint_tuple[0]
           # Replace the found characters in guess with '2' and answer with '1'. They are different
           # so that found characters '2' cannot be found again in the answer as they are now '1'.
           guess_list[idx] = '2'
           answer_list[idx] = '1'
           # print(idx, "is identical")

    # Now that we have found all characters that are in the right place, we can now look for
    # characters that are in the wrong place.
    for idx, x in enumerate(guess_list):
        # We only care about letters. Numbers means they are have been "found" above.
        if x.isalpha() and x in answer_list:
            # Put the "wrong place" hint into hint_list.
            hint_list[idx] = hint_tuple[1]
            found_index = answer_list.index(x)
            # print(x, "found at index", found_index)
            # Replace the found characters in answer with '1' so that they cannot be found again.
            answer_list[found_index] = '1'
        # else:
            # print(x, "not found")
    # print(guess_list)
    # print(answer_list)
    # print(hint_list)
    return "".join(hint_list)

###############################################################################
# Main function begins here.
###############################################################################

# So we do not want to "hard code" anything; everything must be stored in variables.
# In the future, this could also be read from some configuration file.
word_file = "five_letter_words.txt"
num_letters = 5
max_guesses = 6
# O: Letter is in the right place.
# o: Letter is in the wrong place.
# .: Letter is not found.
hint_tuple = ('O', 'o', '.')

# Winning hint is all letters in the right place.
winning_hint = hint_tuple[0] * num_letters
word_set = set()
num_words = 0
try:
    f = open(word_file, "r")
except IOError:
    print("Failed to open file for reading:", word_file)
    sys.exit(1)

for line in f:
    line = line.strip()
    # Only accept num_letters words and convert them to all upper case.
    if len(line) == num_letters and line.isalpha():
        word_set.add(line.upper())
        num_words += 1
    # else:
        # print("Skipping line:", line)

f.close()
print("Number of words read:", num_words)

answer_word = random.choice(tuple(word_set))
# print("Answer is", answer_word)

num_guesses = 1
current_hint = ""
while num_guesses <= max_guesses and current_hint != winning_hint:
    prompt = "Enter guess #" + str(num_guesses) + " of " + str(max_guesses) + ": "
    guess_word = input(prompt).upper()
    # if len(guess_word) == num_letters and guess_word.isalpha():
    if len(guess_word) == num_letters and guess_word.isalpha() and guess_word in word_set:
        # print("Found")
        current_hint = check_word(guess_word, answer_word, num_letters, hint_tuple)
        print(current_hint)
        if current_hint != winning_hint:
            num_guesses += 1
    # else:
        # print("Not Found")

if current_hint == winning_hint:
    print("Number of guesses:", num_guesses)
else:
    print("Ran out of guesses. The answer is:", answer_word)
