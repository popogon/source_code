# 古いコードです

import random
# 文字色を変える記述
from termcolor import colored
# windows環境でanaconda promptでのcolorライブラリの文字化けを防ぐ記述
import colorama
colorama.init()
# 問題のファイルをインポート
from mondai_list import list_1,list_2
from random import randint

# 出題をランダムにする
m_list=[list_1,list_2]
color_list=["black","red","green","yellow","blue","magenda","cyan","white","reset"]



count = 0
seikai = 0
template = '第'+str(count)+'問\n' + '*'*15 + '\n{}\n解答\n' + '*'*15

while True:
    subject = m_list[randint(0,1)]
    count += 1
    template = '第'+str(count)+'問\n' + '*'*15 + '\n{}\nyes or no?\n' + '*'*15
     
# 問題を表示する
    word = random.choice(list(subject.keys()))
    
    print(colored(template.format(word),'yellow'))
    # d.keys()
    # 自分が入力する
    answer = input('解答:')

    # 0で終了
    if answer == '0' or answer == '０':
        print('終了します')
        break
        
    # 解答の正否を判定
    elif answer in subject[word]:
        print(colored('正解','green'))
        print("解説: "+colored(subject[word][2],'cyan'))
        seikai += 1
    else:
        print(colored('不正解','red'))
        print("解説: "+(colored(subject[word][2],'cyan')))
    input("")
    
    # 採点結果を表示
    if count > 9:
        print('スコア:%s/10'%(seikai))
        
    
        if seikai > 9:
            print('perfect!!')
        elif seikai > 5 and seikai < 10:
            print('good!')
        else:
            print("Let's review")
        break
