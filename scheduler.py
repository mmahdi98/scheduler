import pandas as pd
from datetime import date, timedelta
from prettytable import PrettyTable
import sys
topic = 'topics.csv'
word = 'words.csv'
if len(sys.argv) == 3:
    topic = sys.argv[1]
    word = sys.argv[2]
df_topic = pd.read_csv(topic)
df_word = pd.read_csv(word)
topic_list = [1, 7, 16, 35, 70, 150, 360]
word_list = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
today = date.today()

def add(name, df, l):
    if name in df['name'].tolist():
        return False, df
    d = {'name':name, 'stage':'1', 'created':str(today)}
    for i in l:
        d[str(i)] = str(today + timedelta(days=i))
    df = df.append(d, ignore_index=True)
    return True, df

def modify(name, df, stage, l):
    if name not in df['name'].tolist() or int(stage) not in l:
        return False, df
    df.loc[df['name'] == name, 'stage'] = stage
    return True, df

def df_table(df):
    table = PrettyTable()
    table.field_names = df.columns.tolist()
    for i in df.values:
        table.add_row(i.tolist())
    return table.get_string()

def get_today(df):
    tmp = pd.DataFrame(columns=df.columns.tolist())
    for i in range(len(df)):
        col = str(df.loc[i]['stage'])
        d = date(*tuple(map(int, df.loc[i][col].split('-'))))
        if d <= today:
            tmp = tmp.append(df.loc[i], ignore_index=True)
    return tmp

while True:
    a = input('\n\t[11] show today\'s topics\t\t[12] add a topic\t\t[13] modify a topic\t\t[14] save topics\t[15] show all topics\
               \n\t[21] show today\'s words \t\t[22] add a word \t\t[23] modify a word \t\t[24] save words \t[25] show all word\
               \n\t[0]  quit\n>')
    if a == '11':
        print(df_table(get_today(df_topic)))
    elif a == '21':
        print(df_table(get_today(df_word)))
    elif a == '12':
        flg, d = add(input('enter name\n>>'), df_topic, topic_list)
        if not flg:
            print('ERROR, name is found')
        else:
            df_topic = d
    elif a == '22':
        flg, d = add(input('enter name\n>>'), df_word, word_list)
        if not flg:
            print('ERROR, name is found')
        else:
            df_word = d
    elif a == '13':
        flg, d = modify(input('enter name\n>>'), df_topic, input('enter stage\n>>'), topic_list)
        if not flg:
            print('ERROR, name or stage not found')
        else:
            df_topic = d
    elif a == '23':
        flg, d = modify(input('enter name\n>>'), df_word, input('enter stage\n>>'), word_list)
        if not flg:
            print('ERROR, name or stage not found')
        else:
            df_word = d
    elif a == '14':
        df_topic.to_csv(topic, encoding='utf-8', index=False)
    elif a == '24':
        df_word.to_csv(word, encoding='utf-8', index=False)
    elif a == '15':
        print(df_table(df_topic))
    elif a == '25':
        print(df_table(df_word))
    elif a == '0':
        break
    else:
        continue