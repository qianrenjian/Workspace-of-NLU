# convert label data to train data
from  sys import maxsize
import os
import argparse
import pandas as pd
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--input_excel', type=str)
args = parser.parse_args()

convert_dict = {'p-e-volume': '冰箱容量', 'p-e-door': '冰箱门款', 'p-e-conditioning': '冰箱控温', 'p-e-sound': '冰箱运转音', 'p-e-screen': '冰箱显示', 'p-e-energy': '冰箱能效', 'p-c-price': '商品价格', 'p-c-quality': '商品质量', 'p-c-color': '商品颜色', 'p-c-appearance': '商品外观', 'p-c-marketing': '商品营销', 'p-c-brand': '商品品牌', 'p-c-others': '商品其他', 'cs-c-price': '客服价格政策问题', 'cs-c-refund': '客服退款问题', 'cs-c-gift': '客服赠品问题', 'cs-c-return': '客服换货问题', 'cs-c-maintanence': '客服维修问题', 'cs-c-installment': '客服安装问题', 'cs-c-others': '客服其他', 'l-c-delivery': '物流配送', 'l-c-return': '退货服务', 'l-c-refund': '退换服务', 'l-c-others': '物流其他', 's-c-maintanence': '维修服务', 's-c-installment': '安装服务', 's-c-others': '售后其他', 'general': '其他'}


def str2slotlist(input_str:str):
    input_str = input_str.replace('\t', '')
    input_str = input_str.replace('"', '')
    input_str = input_str.replace("'", '')
    input_str = input_str.strip('[]')
    split_list = input_str.split(',')
    split_list = [ item.strip('{}') for item in split_list]
    
    assert len(split_list)%4 == 0, print(len(split_list))
    
    return_list = []
    dict_tmp = {}
    for idx, item in enumerate(split_list): 
        assert len(item.split(':')) == 2
        key = item.split(':')[0].strip()
        value = item.split(':')[1].strip()
        #if len(key) == 0:
        #    continue
        dict_tmp[key] = value 
        if idx%4 == 3:
            new_dict = dict_tmp.copy()
            return_list.append(new_dict)

    return return_list

"""
read origin excel
"""
def read_train_data():
    df_correct_1 = pd.read_csv('train_csv/train_909.csv', usecols=['correct'])
    df_slots_1 = pd.read_csv('train_csv/train_909.csv', usecols=['slots'])
    
    df_correct_2 = pd.read_csv('train_csv/train_976.csv', usecols=['correct'])
    df_slots_2 = pd.read_csv('train_csv/train_976.csv', usecols=['slots'])
    
    df_correct_3 = pd.read_csv('train_csv/train_1055.csv', usecols=['correct'])
    df_slots_3 = pd.read_csv('train_csv/train_1055.csv', usecols=['slots'])
    
    df_correct_4 = pd.read_csv('train_csv/train_1056.csv', usecols=['correct'])
    df_slots_4 = pd.read_csv('train_csv/train_1056.csv', usecols=['slots'])
    
    text_list_1 = [item[0] for item in df_correct_1.values]
    slot_list_1 = [item[0] for item in df_slots_1.values]
    
    text_list_2 = [item[0] for item in df_correct_2.values]
    slot_list_2 = [item[0] for item in df_slots_2.values]
    
    text_list_3 = [item[0] for item in df_correct_3.values]
    slot_list_3 = [item[0] for item in df_slots_3.values]
    
    text_list_4 = [item[0] for item in df_correct_4.values]
    slot_list_4 = [item[0] for item in df_slots_4.values]
    
    text_list = text_list_1+text_list_2+text_list_3+text_list_4
    slot_list = slot_list_1+slot_list_2+slot_list_3+slot_list_4
    
    assert len(text_list) == len(slot_list)

    return text_list, slot_list

def read_test_data():
    #df_correct_1 = pd.read_csv('test_csv/test_1043.csv', usecols=['correct'])
    #df_slots_1 = pd.read_csv('test_csv/test_1043.csv', usecols=['slots'])
    
    df_correct_2 = pd.read_csv('test_csv/test_1168.csv', usecols=['correct'])
    df_slots_2 = pd.read_csv('test_csv/test_1168.csv', usecols=['slots'])
    
    #text_list_1 = [item[0] for item in df_correct_1.values]
    #slot_list_1 = [item[0] for item in df_slots_1.values]
    
    text_list_2 = [item[0] for item in df_correct_2.values]
    slot_list_2 = [item[0] for item in df_slots_2.values]
    
    text_list = text_list_2
    slot_list = slot_list_2
    
    assert len(text_list) == len(slot_list)

    return text_list, slot_list

def check_data(text_list, slot_list):
    text_list_check = []
    slot_list_check = []

    sentiment_slot_list = ['sentiment-positibve', 'sentiment-negative', 'sentiment-moderate']

    for text, slots in zip(text_list, slot_list):

        if type(slots) is not str:
            continue
        if len(slots) == 2:
            continue

        slots = str2slotlist(slots)
        for slot in slots:
            if slot['domain'] == '' or slot['slotname'] == '':
                print("##6", slot)
                break
            if slot['domain'] == 'sentiment' and slot['slotname'] not in sentiment_slot_list:
                print("##1", slot)
                break 
            if slot['domain'] != 'sentiment' and slot['slotname'] in sentiment_slot_list:
                print("##2", slot)
                break
        else:
            text_list_check.append(text)
            slot_list_check.append(slots.copy())
    
    return text_list_check, slot_list_check
    

def match_aspect_sentiment(aspect_slot_list, sentiment_slot_list):
    aspect_polarity = []

    for aspect_slot in aspect_slot_list:
        aspect_index = round(1/2 * (int(aspect_slot['start']) + int(aspect_slot['end'])))
       
        min_gap = maxsize
        best_match_polarity = "" 
        for sentiment_slot in sentiment_slot_list:
            sentiment_index = round(1/2 * (int(sentiment_slot['start']) + int(sentiment_slot['end'])))
            if abs(aspect_index - sentiment_index) < min_gap:
                min_gap = abs(aspect_index - sentiment_index) 
                # print(sentiment_slot['slotname'])
                try:
                    best_match_polarity = sentiment_slot['slotname'].split('-')[1]
                except IndexError:
                    print("#4", sentiment_slot)

        #print('best match polarity', best_match_polarity)
        if best_match_polarity == 'positibve':
            best_match_polarity = 1
        elif best_match_polarity == 'negative':
            best_match_polarity = -1
        elif best_match_polarity == 'moderate':
            best_match_polarity = 0
        else:
            raise Exception()
        aspect_polarity.append(best_match_polarity)

    return aspect_polarity 

def write_data(output_dir, line, aspect_slot_list, aspect_polarity, mode):
    #print(line)
    #print(aspect_slot_list)
    #print(aspect_polarity)
    #print(mode) 


    with open(os.path.join(output_dir, str(mode) + '-category.txt'), encoding='utf-8', mode='a') as f:
        for slot, polarity in zip(aspect_slot_list, aspect_polarity):
            f.write(line + '\n')
            f.write(convert_dict[slot['slotname']] + '\n')
            #print("slotname", slot['slotname'])
            f.write(str(polarity) + '\n') 
    
    #print("Done:1") 
    with open(os.path.join(output_dir, str(mode) + '-term.txt'), encoding='utf-8', mode='a') as f:
        for slot, polarity in zip(aspect_slot_list, aspect_polarity):
            term = line[int(slot['start']):int(slot['end'])+1]
            replace_line = line.replace(term, "$T$", 1)
            f.write(replace_line + '\n')
            f.write(term + '\n')
            #print("term", term)
            f.write(str(polarity) + '\n') 
    #print("Done:2")
    
def get_clf_data(text_list, slot_list, mode):

    assert len(text_list) == len(slot_list)
    for line, slots in zip(text_list, slot_list):
        if line is 'nan':
            continue
    
        aspect_slot_list = []
        sentiment_slot_list = []

        for slot in slots: # 遍历所有slot，分别找到aspect slot 和 sentiment slot
            if slot['domain'] == 'sentiment':
                sentiment_slot_list.append(slot)
            else:
                aspect_slot_list.append(slot)                      
        
        if len(aspect_slot_list) == 0 or len(sentiment_slot_list) == 0:
            continue
        else: # A^{m} S^{n} m>0 n>0
            # 当前规则，选取最近的sentiment 作为 aspect 对应的情感词，并表明该aspect 的极性
            aspect_polarity = match_aspect_sentiment(aspect_slot_list, sentiment_slot_list)             
            write_data(output_dir, line, aspect_slot_list, aspect_polarity, mode) 

output_dir = "clf"

if os.path.exists(output_dir) is False:
    os.mkdir(output_dir)
else:
    shutil.rmtree(output_dir)
    os.mkdir(output_dir)


train_text_list, train_slot_list = read_train_data()
test_text_list, test_slot_list = read_test_data()

train_text_list, train_slot_list = check_data(train_text_list, train_slot_list)
test_text_list, test_slot_list = check_data(test_text_list, test_slot_list)

get_clf_data(train_text_list, train_slot_list, mode='train')
get_clf_data(test_text_list, test_slot_list, mode='test')

