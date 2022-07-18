import random, sys

class Wordle:
    def __init__(self, num_letters, max_guesses, hint_tuple):
        self.num_letters = num_letters
        self.max_guesses = max_guesses
        self.hint_tuple = hint_tuple
        # Winning hint is all letters in the right place.
        self.winning_hint = self.hint_tuple[0] * self.num_letters
        self.word_set = set()
        self.answer_word = None

    def read_file(self, word_file):
        """
        Reads list of words from word_file, one line per word.
        Returns number of words read, or -1 if we failed to open the file for reading.
        """
        try:
            f = open(word_file, "r")
        except IOError:
            print("Failed to open file for reading:", word_file)
            return -1

        num_words = 0
        for line in f:
            line = line.strip()
            # Only accept self.num_letters words and convert them to all upper case.
            if len(line) == self.num_letters and line.isalpha():
                self.word_set.add(line.upper())
                num_words += 1
            # else:
                # print("Skipping line:", line)

        f.close()
        return num_words

    def random_answer(self):
        """
        Chooses a random word from self.word_set and assigns it to self.answer_word
        """
        self.answer_word = random.choice(tuple(self.word_set))

    def check_word(self, guess):
        """
        We will return a string with each letter having the following meaning:
        self.hint_tuple[0]: Letter is in the right place.
        self.hint_tuple[1]: Letter is in the wrong place.
        self.hint_tuple[2]: Letter is not found.
        """
        # Convert everything to uppercase.
        guess_list = list(guess.upper())
        answer_list = list(self.answer_word.upper())
        # hint_list starts with all "letters not found".
        hint_list = list(self.hint_tuple[2] * self.num_letters)
        # print(guess_list)
        # print(answer_list)
        # print(hint_list)
        # Look for characters that are in the right place. We must check this first before looking
        # for characters that are in the wrong place.
        for idx, _ in enumerate(guess_list):
            if guess_list[idx] == answer_list[idx]:
                # Put the "right place" hint into hint_list.
               hint_list[idx] = self.hint_tuple[0]
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
                hint_list[idx] = self.hint_tuple[1]
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

    def input_guesses(self):
        """
        This is the main loop that reads the guesses and checks each one.
        Returns number of guesses if the word was successfully guessed, 0 on failure.
        """
        num_guesses = 1
        current_hint = ""
        while num_guesses <= self.max_guesses and current_hint != self.winning_hint:
            prompt = "Enter guess #" + str(num_guesses) + " of " + str(self.max_guesses) + ": "
            guess_word = input(prompt).upper()
            # if len(guess_word) == num_letters and guess_word.isalpha():
            if len(guess_word) == self.num_letters and guess_word.isalpha() and guess_word in self.word_set:
                # print("Found")
                current_hint = self.check_word(guess_word)
                print(current_hint)
                if current_hint != self.winning_hint:
                    num_guesses += 1
            # else:
                # print("Not Found")

        if current_hint == self.winning_hint:
            return num_guesses
        else:
            return 0

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

w = Wordle(num_letters, max_guesses, hint_tuple)
words_read = w.read_file(word_file)
print("Number of words read:", words_read)
if words_read <= 0:
    sys.exit(1)

# print(w.word_set)

w.random_answer()
# print("Answer is", w.answer_word)

num_guesses = w.input_guesses()

if num_guesses > 0:
    print("Number of guesses:", num_guesses)
else:
    print("Ran out of guesses. The answer is:", w.answer_word)
