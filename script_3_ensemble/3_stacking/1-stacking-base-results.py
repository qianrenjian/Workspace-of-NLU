#!/usr/bin/python3# -*- coding: utf-8 -*-# @Time    : 2019-02-27 09:40# @Author  : apollo2mars# @File    : 1-stacking-base-results.py# @Contact : apollo2mars@gmail.com# @Desc    :# 	stacking:# 	train base learner#   get base learner result#   get test set resultimport os, sys"""root path"""abs_path = os.path.abspath(os.path.dirname(__file__))base_dir = abs_path[:abs_path.find("Workspace-of-NLU") + len("Workspace-of-NLU")]sys.path.append(base_dir)from script_2_train.cnn import *from script_2_train.rnn import *from utils.build_model import *from utils.data_helper import *from model.bert.run_classification import train_eval_bert, predict_bert"""gpu settting"""os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # default: 0gpu_config = tf.ConfigProto()gpu_config.gpu_options.allow_growth = Truegpu_config.gpu_options.per_process_gpu_memory_fraction = 0.4os.environ["CUDA_VISIBLE_DEVICES"] = "0""""cnn """m_type = 'stacking'data_folder = 'data/THUCnews/stacking-3'_train_data_list = ['a_train.txt', 'b_train.txt', 'c_train.txt']_test_data_list = ['a_test.txt', 'b_test.txt', 'c_test.txt']assert len(_train_data_list) == len(_test_data_list)_test = 'test.txt'def train_cnn_model_k_flod():    m_control = 'train'    m_model = 'cnn'    for _train, _test in zip(_train_data_list, _test_data_list):        train_or_predict_cnn(m_type, m_control, m_model, data_folder, _train, _test)def get_cnn_results():    m_control = 'test'    m_model = 'cnn'    for _train, _test in zip(_train_data_list, _test_data_list):        train_or_predict_cnn(m_type, m_control, m_model, data_folder, _train, _test)    _test = 'test.txt'    for _train in _train_data_list:        train_or_predict_cnn(m_type, m_control, m_model, data_folder, _train, _test)def train_bert_model_k_fold():    m_type = 'stacking'    seq_len = 100    epoch = 5    for _train, _test in zip(_train_data_list, _test_data_list):        train_eval_bert(m_type, data_folder, _train, _test, seq_len, epoch)def get_bert_results():    """    load checkpoint and predict    """    m_type = 'stacking'    for _train, _test in zip(_train_data_list, _test_data_list):        predict_bert(m_type, data_folder, _train, _test)    _test = 'test.txt'    for _train in _train_data_list:        predict_bert(m_type, data_folder, _train, _test)def train_rnn_model_k_flod():    m_model = 'rnn'    for _train, _test in zip(_train_data_list, _test_data_list):        train_or_predict_cnn(m_type, 'train', m_model, data_folder, _train, _test)def get_rnn_results():    m_model = 'rnn'    for _train, _test in zip(_train_data_list, _test_data_list):        train_or_predict_rnn(m_type, 'test', m_model, data_folder, _train, _test)    _test = 'a_test.txt'    for _train in _train_data_list :        train_or_predict_rnn(m_type, 'test', m_model, data_folder, _train, _test)def get_bert_kash_results():    passdef get_fasttext_results():    passdef get_base_learner_results():    test_file = 'test-14k.txt'    m_type = 'base'    m_model = 'cnn'    train_or_predict_cnn(m_type, 'test', m_model, 'data', 'train-new.txt', test_file)    m_type = 'base'    m_model = 'rnn'    train_or_predict_cnn(m_type, 'test', m_model, 'data', 'train-new.txt', test_file)    m_type = 'base'    seq_len = 32    epoch = 5    train_eval_bert(m_type, 'data', 'train-new.txt', test_file, seq_len, epoch)    predict_bert(m_type, 'data', 'train-new.txt', test_file)if __name__ == '__main__':    """    train base learner    """    os.environ["CUDA_VISIBLE_DEVICES"] = '3'    # get_base_learner_results()    """    train all model just once    save checkpoint    """    # train_cnn_model_k_flod()    # train_bert_model_k_fold()    # train_rnn_model_k_flod()    # trian_capsule_model_k_fold()    # train_fasttext_model_k_fold()    """    use trained model to predict file    """    # get_cnn_results()    # get_bert_results()    get_rnn_results()    # get_bert_kash_result()    # get_bert_results()    # get_fasttext_results()