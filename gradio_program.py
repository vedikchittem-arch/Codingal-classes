#create the sentiment dictionary

LEXICON = {
          "good":2,
          "great":3,
          "amazing":3,
          "love":3
          }
#negation and intensifier

NEGATION = {"not","no","never","hardly"}
INTENSIFIER = {
              "very":2,
              "really":2,
              "so":2,
              "extremely":3
              }

# three rules switches

USE_BUT_RULE = False
USE_NEGATION_WINDOW = False
NEGATION_WINDOW = 3

#punctuation

PUNCTUATION = ".,!?:;'/()"

# clean the word

def clean_word(word):
    return word.lower().strip(PUNCTUATION)


           