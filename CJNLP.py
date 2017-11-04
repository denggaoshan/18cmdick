#coding=utf-8
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import SementicRoleLabeller
from pyltp import NamedEntityRecognizer
from pyltp import Parser


modelPath='C:\Users\CJ\ltp_data'

import os
model="cws.model"
os.path.join(modelPath, model)

#分词
def segmentor(sentence='你好，你觉得这个例子从哪里来的？当然还是直接复制官方文档，然后改了下这里得到的。我的微博是MebiuW，转载请注明来自MebiuW！'):
    segmentor = Segmentor()  # 初始化实例
    model="cws.model"
    segmentor.load(os.path.join(modelPath, model))  # 加载模型
    words = segmentor.segment(sentence)  # 分词
    #默认可以这样输出
    print '\t'.join(words)
    # 可以转换成List 输出
    words_list = list(words)
    segmentor.release()  # 释放模型
    return words_list

def posttagger(words):
    postagger = Postagger() # 初始化实例
    model = "pos.model"
    postagger.load(os.path.join(modelPath, model))  # 加载模型
    postags = postagger.postag(words)  # 词性标注
    for word,tag in zip(words,postags):
        print word+'/'+tag
    postagger.release()  # 释放模型
    return postags

#分句，也就是将一片文本分割为独立的句子
def sentence_splitter(sentence='你好，你觉得这个例子从哪里来的？当然还是直接复制官方文档，然后改了下这里得到的。我的微博是MebiuW，转载请注明来自MebiuW！'):
    sents = SentenceSplitter.split(sentence)  # 分句
    print '\n'.join(sents)


#命名实体识别
def ner(words, postags):
    recognizer = NamedEntityRecognizer() # 初始化实例
    model = "ner.model"
    recognizer.load(os.path.join(modelPath, model))  # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    for word, ntag in zip(words, netags):
        print word + '/' + ntag
    recognizer.release()  # 释放模型
    return netags

#依存语义分析
def parse(words, postags):
    parser = Parser() # 初始化实例
    model = "parser.model"
    parser.load(os.path.join(modelPath, model))  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
    parser.release()  # 释放模型
    return arcs

#角色标注
def role_label(words, postags, netags, arcs):
    labeller = SementicRoleLabeller() # 初始化实例
    model = "srl"
    labeller.load(os.path.join(modelPath, model))  # 加载模型
    roles = labeller.label(words, postags, netags, arcs)  # 语义角色标注
    for role in roles:
        print role.index, "".join(
            ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])
    labeller.release()  # 释放模型



#分词
def segmentor(sentence='你好，你觉得这个例子从哪里来的？当然还是直接复制官方文档，然后改了下这里得到的。我的微博是MebiuW，转载请注明来自MebiuW！'):
    segmentor = Segmentor()  # 初始化实例
    model="cws.model"
    segmentor.load(os.path.join(modelPath, model))  # 加载模型
    words = segmentor.segment(sentence)  # 分词
    #默认可以这样输出
    print '\t'.join(words)
    # 可以转换成List 输出
    words_list = list(words)
    segmentor.release()  # 释放模型
    return words_list

def posttagger(words):
    postagger = Postagger() # 初始化实例
    model = "pos.model"
    postagger.load(os.path.join(modelPath, model))  # 加载模型
    postags = postagger.postag(words)  # 词性标注
    for word,tag in zip(words,postags):
        print word+'/'+tag
    postagger.release()  # 释放模型
    return postags

#分句，也就是将一片文本分割为独立的句子
def sentence_splitter(sentence='你好，你觉得这个例子从哪里来的？当然还是直接复制官方文档，然后改了下这里得到的。我的微博是MebiuW，转载请注明来自MebiuW！'):
    sents = SentenceSplitter.split(sentence)  # 分句
    print '\n'.join(sents)


#命名实体识别
def ner(words, postags):
    recognizer = NamedEntityRecognizer() # 初始化实例
    model = "ner.model"
    recognizer.load(os.path.join(modelPath, model))  # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    for word, ntag in zip(words, netags):
        print word + '/' + ntag
    recognizer.release()  # 释放模型
    return netags

#依存语义分析
def parse(words, postags):
    parser = Parser() # 初始化实例
    model = "parser.model"
    parser.load(os.path.join(modelPath, model))  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
    parser.release()  # 释放模型
    return arcs

#角色标注
def role_label(words, postags, netags, arcs):
    labeller = SementicRoleLabeller() # 初始化实例
    model = "srl"
    labeller.load(os.path.join(modelPath, model))  # 加载模型
    roles = labeller.label(words, postags, netags, arcs)  # 语义角色标注
    for role in roles:
        print role.index, "".join(
            ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])
    labeller.release()  # 释放模型


eitites = []
str_e = ""
import re

for word, ntag in word_ntags:
    if re.search(r'O', ntag):
        str_e = ""
    if re.search(r'Ni$', ntag):
        str_e += word
    if re.search(r'S', ntag):

    if ntag == 'B-Ni':
        str_e = word
    elif ntag == 'I-Ni':
        str_e += word
    elif ntag == 'E-Ni':
        str_e += word
        eitites.append(str_e)
    elif ntag == 'S-Ni':
        str_e = word
        entites.append(str_e)
    else:
        str_e = ""