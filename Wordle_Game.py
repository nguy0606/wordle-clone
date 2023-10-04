import tkinter as tk
import time
from os import listdir
from random import randint

root = tk.Tk()
root.geometry("600x600")
root.title("Wordle Game")
game_type_var = tk.StringVar()
word_list = {}
entry_var = tk.StringVar()
used_ltr_var = tk.StringVar()
message_var = tk.StringVar()
tries_var = tk.StringVar()

#Game class holds important non-interface variables
class Game:
    secret_word = ''
    length = 5
    new_length = 5
    guesses = 5
    new_guesses = 5
    tries = 5
    used_letters = []

#functions
def set_game(set_length):
    Game.new_length = set_length
    Game.new_guesses = set_length + 1
    game_type_str = f'{Game.new_length} Letter Word'
    game_type_var.set(game_type_str)

def start_game():

    Game.length = Game.new_length
    Game.guesses = Game.new_guesses

    #check for wordlist
    if 'words.txt' not in listdir():
        message_var.set('Missing words.txt')
        return
    #turn into dictionary
    if Game.length not in word_list:
        generate_wordlist(word_list, Game.length)
    Game.secret_word = word_list[Game.length][randint(0,len(word_list[Game.length]))]
    print(Game.secret_word)
    Game.used_letters = []
    update_used_letters()
    Game.tries = Game.guesses
    guess_btn.config(state='normal')
    wordbox.config(height = Game.guesses)
    wordbox.config(state='normal')
    wordbox.delete(0.0, 'end')
    wordbox.config(state='disabled')
    word_entry.delete(0, 'end')
    tries_var.set(f'Guess ({Game.tries} tries remain)')

def generate_wordlist(word_list, word_length):
    word_list[word_length] = []
    f = open('words.txt', mode='r')
    for line in f.readlines():
        line = line.strip()
        if len(line) == word_length and line.isalpha():
            word_list[word_length].append(line.lower())
    f.close()

def update_used_letters():
    str = ''
    Game.used_letters.sort()
    for letter in Game.used_letters:
        str += letter + ' '
    used_ltr_var.set(str)

def submit():
    new_word = entry_var.get()
    message_var.set('')
    #verify
    if len(new_word) != Game.length:
        message_var.set(f'Please enter a word that is {Game.length} letters long')
        return
    if not new_word.isalpha():
        message_var.set(f'Please enter a word with only alphabetic characters')
        return
    if new_word.lower() not in word_list[Game.length]:
        message_var.set('Please guess a valid English word')
        return

    #insert word entry into word box
    wordbox.config(state='normal')
    #wordbox.delete(0.0,tk.END)
    if wordbox.get(1.0) != '\n':
        wordbox.insert(tk.END, '\n')
    wordbox.insert('end', new_word)
    wordbox.config(state='disabled')

    letter_check(new_word)

    #add to used letters list
    for letter in new_word:
        if letter not in Game.used_letters:
            Game.used_letters.append(letter)
    update_used_letters()

    #check win/lose conditions
    Game.tries -= 1
    tries_var.set(f'Guess ({Game.tries} tries remain)')
    if new_word == Game.secret_word:
        stop_game()
        message_var.set('Congratulations! You correctly guessed the word!')
        return
    if Game.tries <= 0:
        stop_game()
        message_var.set(f'Game Over! The word was {Game.secret_word}')
        return
    word_entry.delete(0, 'end')

def letter_check(word):
    for index in range(Game.length):
        tag_index = str(Game.guesses - Game.tries + 1) + '.' + str(index)
        if word[index] in Game.secret_word:
            wordbox.tag_add('in_word', tag_index)
            #print(f'{word[index]} is in the word')
        if word[index] == Game.secret_word[index]:
            wordbox.tag_add('in_place', tag_index)

def stop_game():
    guess_btn.config(state='disabled')

#Option menu
options = tk.LabelFrame(root, text='Options',padx=10,pady=10)
label1 = tk.Label(options, text='Select a word length and click Begin')
word5_button = tk.Button(options, text='5 Letter Word', command=lambda: set_game(5))
word6_button = tk.Button(options, text='6 Letter Word', command=lambda: set_game(6))
word7_button = tk.Button(options, text='7 Letter Word', command=lambda: set_game(7))
game_type_label = tk.Label(options, textvariable=game_type_var)
begin_button = tk.Button(options, text='Begin Game', command=start_game)

#Display the menu
options.pack(padx=10,pady=10)
label1.grid(row=0,column=0,columnspan=3)
word5_button.grid(row=1,column=0,pady=10)
word6_button.grid(row=1,column=1)
word7_button.grid(row=1,column=2)
game_type_label.grid(row=2,column=0,columnspan=3)
begin_button.grid(row=3,column=1,pady=5)

#Game widgets
wordbox = tk.Text(root, height=5, width=10, font=('courier',20), bg='light gray', fg='black', relief='flat')
wordbox.delete(0.0, 'end')
#wordbox.insert(tk.END,'     ')
#Configure tags
wordbox.tag_config("in_word", font=wordbox.cget('font'), background='yellow')
wordbox.tag_config("in_place", font=wordbox.cget('font'), background='green')
wordbox.config(state='disabled')
entry_label = tk.LabelFrame(root, text='Type your guess here',)
word_entry = tk.Entry(entry_label, width=10, textvariable=entry_var, font=('calibre',20,'normal'))
used_letters_frame = tk.LabelFrame(root, text='Used Letters')
used_letters_label = tk.Label(used_letters_frame, textvariable=used_ltr_var, font=12)
tries_var.set(f'Guess ({Game.tries} tries remain)')
guess_btn=tk.Button(root, padx=30, textvariable=tries_var, command=submit, font=12, state='disabled')
#word_entry.bind('<Return>',guess_btn.invoke)
message_label = tk.Label(root, textvariable=message_var, font=16)

#display game widgets
wordbox.pack(side='top')
entry_label.pack()
word_entry.pack(padx=10, pady=10)
used_letters_frame.pack()
used_letters_label.pack(padx=10, pady=10)
guess_btn.pack()
message_label.pack()

set_game(5)

if __name__ == '__main__':
    root.mainloop()