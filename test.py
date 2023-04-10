# anaconda にて cd フォルダ名と入力
# dir を入力
import random
# 文字色を変える記述
from termcolor import colored
# windows環境でanaconda promptでのcolorライブラリの文字化けを防ぐ記述
import colorama
colorama.init()
from mondai_list import minpou,gyouseihou,keihou,kenpou
from random import randint

m_list=[minpou,gyouseihou,keihou,kenpou]
color_list=["black","red","green","yellow","blue","magenda","cyan","white","reset"]



count = 0
seikai = 0
template = '第'+str(count)+'問\n' + '*'*15 + '\n{}\n解答\n' + '*'*15

while True:
    subject = m_list[randint(0,3)]
    count += 1
    template = '第'+str(count)+'問\n' + '*'*15 + '\n{}\nyes or no?\n' + '*'*15
     
# 英単語を表示する
    word = random.choice(list(subject.keys()))
    
    print(colored(template.format(word),'yellow'))
    # d.keys()
    # 自分が入力する
    answer = input('解答:')

    # 自分が入力した日本語と、答えがあっているかを確認する
    if answer == '0' or answer == '０':
        print('終了します')
        break
        
    #elif answer == d[word][0] or answer == d[word][1]:
    elif answer in subject[word]:
        print(colored('正解','green'))
        print("解説: "+colored(subject[word][2],'cyan'))
        seikai += 1
    else:
        print(colored('不正解','red'))
        print("解説: "+(colored(subject[word][2],'cyan')))
    input("")
    
    if count > 9:
        print('スコア:%s/10'%(seikai))
        
    
        if seikai > 9:
            print('perfect!!')
        elif seikai > 5 and seikai < 10:
            print('good!')
        else:
            print('oh...')
        break