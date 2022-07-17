import random

def check_word(guess, answer, num_letters, hint_letters):
    ''' We will return a string with each letter having the following meaning:'''
    ''' O: Letter is in the right place. '''
    ''' o: Letter is in the wrong place. '''
    ''' .: Letter is not found. '''
    guess_list = list(guess.upper())
    answer_list = list(answer.upper())
    # hint_list starts with all "letters not found".
    hint_list = list(hint_letters[2] * num_letters)
    # print(guess_list)
    # print(answer_list)
    # print(hint_list)
    # Look for characters that are in the right place. We must check this first before looking
    # for characters that are in the wrong place.
    for idx, _ in enumerate(guess_list):
        if guess_list[idx] == answer_list[idx]:
            # Put the "right place" hint into hint_list.
           hint_list[idx] = hint_letters[0]
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
            hint_list[idx] = hint_letters[1]
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

# Main function begins here.
word_file = "five_letter_words.txt"
num_letters = 5
max_guesses = 6
hint_letters = "Oo."

winning_hint = hint_letters[0] * num_letters
word_set = set()
f = open(word_file, "r")
for line in f:
    if line[0] != "#":
        word_set.add(line.rstrip().upper())
f.close()

# print(word_set)

answer_word = random.choice(tuple(word_set))
print("Answer is", answer_word)

num_guesses = 1
current_hint = ""
while num_guesses <= max_guesses and current_hint != winning_hint:
    prompt = "Enter guess #" + str(num_guesses) + ": "
    guess_word = input(prompt).upper()
    # if guess_word in word_set:
    if len(guess_word) == num_letters and guess_word.isalpha():
        # print("Found")
        current_hint = check_word(guess_word, answer_word, num_letters, hint_letters)
        print(current_hint)
        if current_hint != winning_hint:
            num_guesses += 1
    # else:
        # print("Not Found")

if current_hint == winning_hint:
    print("Number of guesses:", num_guesses)
else:
    print("Ran out of guesses. The answer is:", answer_word)
