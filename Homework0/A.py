import nltk
import sys

greeting = sys.stdin.read()
print (greeting)

token_list = nltk.word_tokenize(greeting)
print ("The tokens in the greeting are")
lion = 0
wolf = 0
for token in token_list:
    print (token)
    if token.lower() == "lion":
        lion += 1
    if token.lower() == "wolf":
        wolf += 1
print("There were %d instances of the word 'lion' and %d instances of the word 'wolf'" % (lion, wolf))
