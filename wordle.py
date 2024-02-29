'''
    Author:KuborKelp
    Name:Wordle
'''

class Wordle:
    def __init__(self,keyword:str,length:int,maxround:int):
        self.MAXROUND = maxround
        self.game_status = True
        self.keyword = keyword
        self.length = length
        self.round = 0
        self.word_history = [""]*self.MAXROUND #record the words that players has guessed
        self.status_history = [["N"]*self.length]*self.MAXROUND #record the words that players has guessed with the symbol in "T F G N"

        if not (len(keyword)==5 and keyword.isalpha()):
            print("Unable to set the word!")
    
    def next(self, word):
        if len(word) != self.length:
            return f"Check the length of the word.It should be {self.length}"
        elif word in self.word_history:
            return f"you have guessed the word:{word}"
        
        self.word_history[self.round] = word
        lst = []
        for i in range(0,self.length):
            if word[i] == self.keyword[i]:
                lst.append("T")
            elif word[i] in self.keyword and word.count(self.keyword[i]) <= self.keyword.count(self.keyword[i]):
                lst.append("G")
            else:
                lst.append("F")
        self.status_history[self.round] = lst
        self.round += 1
        if word == self.keyword:
            self.game_status = False
            return "Win!"
        print(self.word_history)
        print(self.status_history)
        return True


if __name__ == "__main__":
    print("Hello,Wordle!")
    game = None
    while True:
        if not game:
            x = input("enter 0 to exit \nenter 1 to start a game\n")
            if x == "0":
                game = None
                print("The game has been killed")
            else:
                game = Wordle(keyword="mamba",length=5,maxround=5)
        else:
            if game.round >= game.MAXROUND:
                game = None
                print("Boy,what can I say!")  
            else:
                word = input("Guess:")
                print(game.next(word=word))
                if not game.game_status: #you have won
                    game = None