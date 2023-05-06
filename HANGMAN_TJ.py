import random

HANGMANPICS = ['''

  +---+
  |   |
      |
      |
      |
      |
=========''', '''

  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''

  +---+
  |   |
  O   |
  |   |
      |s
      |
=========''', '''

  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''

  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''

  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''

  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']
words = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()

# 매개변수로 주어진 word 단어 목록들중 하나를 랜덤으로 입력받아 단어를 선택하는 함수
def getRandomWord(wordlist):
    wordindex = random.randint(0, len(wordlist)-1)
    return words[wordindex]

# 매개변수로 행맨그림, 틀린단어, 맞춘단어, 맞춰야하는 단어 입력받기
def displaysBoard(HANGMANPICS, missedLetters, correctLetters, secretWord):
    # 현 그림의 틀린 단어 수만큼 행맨 그리기
    print(HANGMANPICS[len(missedLetters)])
    print()
    # 틀린 단어들에 한해 표기해주기
    print('틀린 단어 목록입니다 : ', end = ' ')
    for letter in missedLetters:
        print(letter, end = ' ')
    print()
    # 맞추어야 하는 단어 수만큼 _로 표기, 맞춘 단어에 한해 해당 글자로 표기
    blanks = ''
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks += secretWord[i]
        else:
            blanks += '_'
    for letter in blanks:
        print(letter, end = ' ')
    print()

# 맞추어야 하는 단어 맞나 틀리나 확인
def getGuess(alreadyGuessed):
    while True:
        print('Guess a letter.')
        guess = input().lower()
        # 알파벳 개수 한개가 아니면 다시 입력 요청
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. choose again plaase.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

# 게임 다시 작동시킬지 여부
def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

# 단어 맞춘 경우 찾은 단어 출력해 찾은 단어 출력
def checkCorrectAnswer(correctLetters, secretWord):
    foundAllLetters = True
    for i in range(len(secretWord)):
        if secretWord[i] not in correctLetters:
            foundAllLetters = False
            break
    return foundAllLetters

# 단어 틀리고 행맨 그림 다 그려지면 게임 종료
def checkWrongAnswer(missedLetters, secretWord):
    if len(missedLetters) == len(HANGMANPICS) - 1:
        return True
    return False

import os

# 게임 돌아가는 메인 함수 생성
def main():
    # 파일 경로에서 txt 불러와 파일 존재시 최고점수를 읽고, 없으면 최고점수를 0으로 지정
    if os.path.exists('hangman_score.txt'):
        with open('hangman_score.txt', 'r') as f:
            bestScore = int(f.read())
    else:
        bestScore = 0

    print('H A N G M A N by ................')
    missedLetters = ''
    correctLetters = ''
    gameSucceeded = False
    gameFailed = False
    secretWord = getRandomWord(words)
    # 현재 점수 지정
    currentScore = 0

    # 게임 반복 No전까지
    while True:
        displaysBoard(HANGMANPICS, missedLetters, correctLetters, secretWord)
        # 단어 맞추든 틀리든 표기하고 현재 점수도 표기해주기
        if gameSucceeded or gameFailed:
            # 현재 점수 확인하기 (맞춘 단어 수만큼)
            if gameSucceeded:
                print('Yes! The secret word is "' + secretWord + '"! You have won!')
                print(currentScore)
            else:
                print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
                print(currentScore)

            # 점수 비교해 더 높으면 값 변경 후 저장
            if currentScore > bestScore:
                bestScore = currentScore
                print(bestScore)
                with open('hangman_score.txt', 'w') as f:
                    f.write(str(bestScore))
            else:
                print(currentScore)

            # 변수 재설정
            if playAgain():
                missedLetters = ''
                correctLetters = ''
                gameSucceeded = False
                gameFailed = False
                secretWord = getRandomWord(words)
                currentScore = 0
                continue
            else:
                break

        # 맞춘 단어 확인
        guess = getGuess(missedLetters + correctLetters)
        if guess in secretWord:
            # 단어 맞출 때마다 점수 + 1
            currentScore += 1
            correctLetters = correctLetters + guess
            gameSucceeded = checkCorrectAnswer(correctLetters, secretWord)
        else:
            missedLetters = missedLetters + guess
            gameFailed = checkWrongAnswer(missedLetters, secretWord)

if __name__ == "__main__":
    main()