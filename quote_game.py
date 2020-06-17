from quote_scraper import scrape_quotes, scrape_dob_loc, scrape_first_two, scrape_second_two
from random import randint
import re

class Quote:
    """ Class containing the model for each randomly generated quote"""
    def __init__(self, quote_details):
        self.text = quote_details[0]
        self.author = quote_details[1]
        self.bio_link = quote_details[2]

    def get_dob_loc(self):
        dob_loc = scrape_dob_loc(self.bio_link)
        return dob_loc

    def redact_name(self, string):
        """ redacts the name from the hint """
        author_pat = "(" + re.sub(" ","|",self.author) + ")"
        replace = "________"
        redacted = re.sub(author_pat, replace, string)
        return redacted
    
    def get_desc_first_hint(self):
        sentences = scrape_first_two(self.bio_link)
        sentences = self.redact_name(sentences)
        return sentences

    def get_desc_second_hint(self):
        sentences = scrape_second_two(self.bio_link)  
        sentences = self.redact_name(sentences) 
        return sentences

def create_quote():
    lol = scrape_quotes()
    rand_num = randint(0, len(lol))
    rand_quote = Quote(lol[rand_num])
    return rand_quote

# Start of guessing game
continue_playing = True 
while continue_playing:
    guess_left = 4
    quote = create_quote()
    print("Here's a quote:\n")
    print(quote.text)
    while guess_left > 0:
        player_guess = input(f"\nGuesses remaining: {guess_left}\nWho said this?  ")
        guess_left -= 1 

        # Check users answer
        if player_guess.lower() == quote.author.lower():
            print("Congratulations you guessed correctly!")
            break

        # Provides hints each incorrect guess
        elif guess_left == 3:
            print(f"\nHere's a hint: The author was born on {quote.get_dob_loc()}")
        elif guess_left == 2:
            print(f"\nHere's another hint: {quote.get_desc_first_hint()}\n")    
        elif guess_left == 1:
            print(f"\nHere's another hint: {quote.get_desc_second_hint()}\n")    
        else:
            print(f'Sorry you lost! The quote was by {quote.author}!\n')         
    
    play_again = input("Would you like to play again? (y/n)? ")
    if play_again.lower() == 'y':
        guess_left = 4
        print("Here we go again! Coming up with another quote\n --------")
        continue
    else:
        continue_playing = False 
