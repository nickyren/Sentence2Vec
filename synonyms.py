# -*- coding=utf-8 -*-
import pandas as pd

def permutation(data):
    if len(data) == 1:  # 当data中只剩（有）一个词及其同义词的列表时，程序返回
        return data[0]
    else:
        head = data[0]
        tail = data[1:]  # 不断切分到只剩一个词的同义词列表
    tail = permutation(tail)
    permt = []
    for h in head:  # 构建两个词列表的同义词组合
        for t in tail:
            if isinstance(t, str):  # 传入的整个data 的最后一个元素是一个一维列表，其中每个元素为str
                permt.extend([[h] + [t]])
            elif isinstance(t, list):
                permt.extend([[h] + t])
    return permtpan

def load_synonyms(file_path):
    synonyms = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            synonyms.append(line.strip().split(' '))
    return synonyms

def get_syno_sents_list(synonyms,input_sentence):
    perm_sent_list = []
    # print(synonyms)
    for seged_sentence in input_sentence:
        candidate_synonym_list = []  # 每个元素为句子中每个词及其同义词构成的列表
        for word in seged_sentence:
            word_synonyms = []  # 初始化一个词的同义词列表
            for syn in synonyms:  # 遍历同义词表，syn为其中的一条
                if word in syn:  # 如果句子中的词在同义词表某一条目中，将该条目中它的同义词添加到该词的同义词列表
                    # syn.remove(word)
                    word_synonyms.extend(syn)
            candidate_synonym_list.append(word_synonyms)  # 添加一个词语的同义词列表
        perm_sent = permutation(candidate_synonym_list)  # 将候选同义词列表们排列组合产生同义句
        perm_sent_list.append(perm_sent)
    return perm_sent_list

# 数据库属性字段扩展成问题（问句）
def attr_extend():
    file_path = './InputData/query-hive625.xlsx'
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    df = df.drop_duplicates()
    df = df.fillna('')
    total_data = []
    tong_yong_list = ['是什么']
    wen_ti_ci_list = ['是什么意思','不懂什么是']
    gong_neng_list = ['有没有','是否支持']
    zao_yin_list = ['有多大','是多少','是多少分贝','是多少db']
    shi_ti_list = ['有多大','是多大','是多少','多少']
    deng_ji_list = ['是几级','多高']
    mian_ji_list = ['多少平','几平米','多少平方']
    lei_xing_fang_shi_list = ['是什么','是怎么样的']
    cai_zhi_list = ['是什么','是不锈钢么','是陶瓷吗']
    fu_jian_list = ['有没有','带','配']
    for index in df.index:
        tong_yong = df.loc[index]["通用"]
        wen_ti_ci = df.loc[index]["问题词"]
        xian_cheng = df.loc[index]["现成"]
        gong_neng = df.loc[index]["功能"]
        zao_yin = df.loc[index]["噪音"]
        shi_ti = df.loc[index]["实体"]
        deng_ji = df.loc[index]["能效等级"]
        mian_ji = df.loc[index]["面积"]
        lei_xing_fang_shi = df.loc[index]["leixing"]
        cai_zhi = df.loc[index]["材质"]
        fu_jian = df.loc[index]["附件"]
        for a in tong_yong_list:
            if str(tong_yong) != '':
                total_data.extend([str(tong_yong) + a])
        for b in wen_ti_ci_list:
            if str(wen_ti_ci) !='':
                total_data.extend([str(wen_ti_ci) + b])
        if str(xian_cheng) != '':
            total_data.extend([xian_cheng])
        for c in gong_neng_list:
            if str(gong_neng) != '':
                total_data.extend([c + gong_neng])
        for d in zao_yin_list:
            if str(zao_yin) != '':
                total_data.extend([zao_yin + d])
        for e in shi_ti_list:
            if str(shi_ti) != '':
                total_data.extend([shi_ti + e])
        for f in deng_ji_list:
            if str(deng_ji) != '':
                total_data.extend([deng_ji + f])
        for g in mian_ji_list:
            if str(mian_ji) != '':
                total_data.extend([mian_ji + g])
        for h in lei_xing_fang_shi_list:
            if str(lei_xing_fang_shi) != '':
                total_data.extend([lei_xing_fang_shi + h])
        for i in cai_zhi_list:
            if str(cai_zhi) != '':
                total_data.extend([cai_zhi + i])
        for j in fu_jian_list:
            if str(fu_jian) != '':
                total_data.extend([j + fu_jian])
    fw = open('./OutputData/pharse_extend.txt','w',encoding='utf-8')
    for item in total_data:
        fw.write(''.join(item)+'\n')

if __name__ == '__main__':
    test_sentence_file_path = './OutputData/seg_file1.txt'
    file_path = './OutputData/pass_similar.txt'
    no_entend_sentence = []
    with open(test_sentence_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            no_entend_sentence.append(line.strip().split(' '))
    synonyms = load_synonyms(file_path)
    syns = get_syno_sents_list(synonyms,no_entend_sentence)
    for syn in syns:
        for s in syn:
            fw = open('./OutputData/final_result1.txt', 'a', encoding='utf-8')
            fw.write(''.join(s)+'\n')
    attr_extend()
