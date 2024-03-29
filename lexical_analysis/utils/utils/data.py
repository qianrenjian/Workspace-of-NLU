import sys, pickle, os, random
import numpy as np, re



def data_normalizer(char_in):
    char_out = char_in
    if char_in.isdigit():
        char_out='<number>'
    if char_in in ['零','一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '半']:
        char_out='<number>'
    return char_out

# process the raw data into training and testing format B- I-
def phrase_normalizer(sentence):
    # 凌晨/黎明/清晨/早上/早晨/上午/中午/下午/晚/晚儿/晚上/傍晚/夜里/上半夜/下半夜/半夜/深夜/午夜
    pattern = '[,.?，。！？]'
    sentence = re.sub(pattern, '', sentence)
    sentence = re.sub(' ', '@', sentence)
    return sentence

def read_corpus(corpus_path):
    """
    读取已经处理好格式的数据
    read corpus and return the list of samples
    :param corpus_path:
    :return: data
    """
    data = []
    with open(corpus_path, encoding='utf-8') as fr:
        lines = fr.readlines()
    sent_, tag_ = [], []
    for idx, line in enumerate(lines):
        if line != '\n':
            # print(line)
            if len(line.strip().split(' ')) == 2:
                [char, label] = line.strip().split()
                sent_.append(char)
                tag_.append(label)
            else:
                # print('###' + line)
                pass
        else:
            data.append((sent_, tag_))
            sent_, tag_ = [], []

    return data


def vocab_build(vocab_path, corpus_path, min_count):
    """
    :param vocab_path:
    :param corpus_path:
    :param min_count:
    :return:
    """
    data = read_corpus(corpus_path)
    word2id = {}
    for sent_, tag_ in data:
        for word in sent_:
            if word.isdigit():
                word = '<NUM>'
            elif ('\u0041' <= word <='\u005a') or ('\u0061' <= word <='\u007a'):
                word = '<ENG>'
            if word not in word2id:
                word2id[word] = [len(word2id)+1, 1]
            else:
                word2id[word][1] += 1
    low_freq_words = []
    for word, [word_id, word_freq] in word2id.items():
        if word_freq < min_count and word != '<NUM>' and word != '<ENG>':
            low_freq_words.append(word)
    for word in low_freq_words:
        del word2id[word]

    new_id = 1
    for word in word2id.keys():
        word2id[word] = new_id
        new_id += 1
    word2id['<UNK>'] = new_id
    word2id['<PAD>'] = 0

    print(len(word2id))
    with open(vocab_path, 'wb') as fw:
        pickle.dump(word2id, fw)


def sentence2id(sent, word2id):
    """
    :param sent:
    :param word2id:
    :return:
    """
    sentence_id = []
    for word in sent:
        if word not in word2id:
            word = '<UNK>'
        sentence_id.append(word2id[word])
    return sentence_id


def read_dictionary(vocab_path):
    """

    :param vocab_path:
    :return:
    """
    vocab_path = os.path.join(vocab_path)
    with open(vocab_path, 'rb') as fr:
        word2id = pickle.load(fr)
    print('vocab_size:', len(word2id))
    return word2id


def random_embedding(vocab, embedding_dim):
    """

    :param vocab:
    :param embedding_dim:
    :return:
    """
    embedding_mat = np.random.uniform(-0.25, 0.25, (len(vocab), embedding_dim))
    embedding_mat = np.float32(embedding_mat)
    return embedding_mat


def pad_sequences(sequences, pad_mark=0):
    """

    :param sequences:
    :param pad_mark:
    :return:
    """
    max_len = max(map(lambda x : len(x), sequences))
    seq_list, seq_len_list = [], []
    for seq in sequences:
        seq = list(seq)
        seq_ = seq[:max_len] + [pad_mark] * max(max_len - len(seq), 0)
        seq_list.append(seq_)
        seq_len_list.append(min(len(seq), max_len))
    return seq_list, seq_len_list


def batch_yield(data, batch_size, vocab, tag2label, shuffle=False):
    """

    :param data:
    :param batch_size:
    :param vocab:
    :param tag2label:
    :param shuffle:
    :return:
    """
    if shuffle:
        random.shuffle(data)#[<class 'tuple'>: (['薯', '片'], ['B-BAIKE_ITEM', 'I-BAIKE_ITEM'])] list of tuples

    seqs, labels = [], []
    for (sent_, tag_) in data:
        sent_ = sentence2id(sent_, vocab)
        try:
            label_ = [tag2label[tag] for tag in tag_]
        except KeyError:
            # print(tag_)
            continue

        if len(seqs) == batch_size:
            yield seqs, labels
            seqs, labels = [], []

        seqs.append(sent_)
        labels.append(label_)

    if len(seqs) != 0:
        yield seqs, labels

