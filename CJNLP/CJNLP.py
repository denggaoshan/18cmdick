#coding=utf-8
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import SementicRoleLabeller
from pyltp import NamedEntityRecognizer
from pyltp import Parser
import os
import re
import datetime

modelPath='C:\Users\CJ\ltp_data'
Output = False
SentenceOutput = False

word_splitor = None
word_tagor = None
word_recognizer = None

def init_model():
    global word_splitor
    word_splitor = Segmentor()
    word_splitor.load(os.path.join(modelPath, 'cws.model'))
    global word_tagor
    word_tagor = Postagger()
    word_tagor.load(os.path.join(modelPath, 'pos.model'))
    global word_recognizer
    word_recognizer = NamedEntityRecognizer()
    word_recognizer.load(os.path.join(modelPath, 'ner.model'))  # 加载模型

def release_model():
    word_splitor.release()
    word_tagor.release()
    word_recognizer.release()

#分词
def segmentor(sentence='你好，你觉得这个例子从哪里来的？'):
    segmentor = Segmentor()  # 初始化实例
    model="cws.model"
    segmentor.load(os.path.join(modelPath, model))  # 加载模型
    words = segmentor.segment(sentence)  # 分词
    #默认可以这样输出
    if Output:
        print "##########分词#############"
        print '\t'.join(words)
    # 可以转换成List 输出
    words_list = list(words)
    segmentor.release()  # 释放模型
    return words_list
#词性标注
def posttagger(words):
    postagger = Postagger() # 初始化实例
    model = "pos.model"
    postagger.load(os.path.join(modelPath, model))  # 加载模型
    postags = postagger.postag(words)  # 词性标注
    if Output:
        print "##########词性标注#############"
        for word,tag in zip(words,postags):
            print word+'/'+tag
    postagger.release()  # 释放模型
    return postags

#分句，也就是将一片文本分割为独立的句子
def sentence_splitter(sentence='你好，你觉得这个例子从哪里来的？'):
    sents = SentenceSplitter.split(sentence)  # 分句
    clean_s = [x for x in list(sents) if x != ""]
    return clean_s

#命名实体识别
def ner(words, postags):
    recognizer = NamedEntityRecognizer() # 初始化实例
    model = "ner.model"
    recognizer.load(os.path.join(modelPath, model))  # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    if Output:
        print "##########命名实体识别#############"

        for word, ntag in zip(words, netags):
            print word + '/' + ntag,
    recognizer.release()  # 释放模型
    return netags

#依存语义分析
def parse(words, postags):
    parser = Parser() # 初始化实例
    model = "parser.model"
    parser.load(os.path.join(modelPath, model))  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    if Output:
        print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
    parser.release()  # 释放模型
    return arcs

#角色标注
def role_label(words, postags, netags, arcs):
    labeller = SementicRoleLabeller() # 初始化实例
    model = "srl"
    labeller.load(os.path.join(modelPath, model))  # 加载模型
    roles = labeller.label(words, postags, netags, arcs)  # 语义角色标注
    if Output:
        for role in roles:
            print role.index, "".join(
                ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])
    labeller.release()  # 释放模型

#得到单个句子内的组织实体
def get_org(sentence):
    words = segmentor(sentence)
    tags = posttagger(words)
    netags = ner(words, tags)
    entities = set()
    str_e =""
    for word,ntag in zip(words, netags):
        if ntag == 'B-Ni':
            str_e = word
        elif ntag == 'I-Ni':
            str_e += word
        elif ntag == 'E-Ni':
            str_e += word
            entities.add(str_e)
        elif ntag == 'S-Ni':
            str_e = word
            entities.add(str_e)
        else:
            str_e = ""
    return entities


def quick_get_org(sentence):
    #init_model()
    words = list(word_splitor.segment(sentence))
    postags = word_tagor.postag(words)
    netags = word_recognizer.recognize(words, postags)  # 命名实体识别
    #release_model()
    entities = set()
    str_e = ""
    for word,ntag in zip(words, netags):
        #print word,ntag
        if ntag == 'B-Ni':
            str_e = word
        elif ntag == 'I-Ni':
            str_e += word
        elif ntag == 'E-Ni':
            str_e += word
            entities.add(str_e)
        elif ntag == 'S-Ni':
            str_e = word
            entities.add(str_e)
        else:
            str_e = ""
    return entities

#去除句子内的标点和非中文
def get_chs(lines):
    def get_chinese(line):
        result = re.findall(ur"([\u4e00-\u9fa5]|[0-9])", line.decode('utf-8'))
        un = "".join(result)
        try:
            return unicode.encode(un)
        except:
            return ''
    result = []
    if SentenceOutput:
        print "##########清洗句子#############"
    for l in lines:
        chl = get_chinese(l)
        if SentenceOutput:
            print "before:"
            print l
            print "after:"
            print chl
        if chl != '':
            result.append(chl)
    return result

def get_entity_P(sentence):
    sts = sentence_splitter(sentence)
    chs = get_chs(sts)
    se = set()
    entities = get_org(" ".join(chs))
    return list(entities)

def getQ(sentence):
    sts = sentence_splitter(sentence)
    chs = get_chs(sts)
    if len(chs) == 0:
        return [""]
    se = set()
    #init_model()
    entities = quick_get_org(" ".join(chs))
    #release_model()
    return list(entities)

def fp(it):
    print "######"
    for i in it:
        print i

if __name__ == "__main__":
    Output = False
    starttime = datetime.datetime.now()

    sentence1 = "宁夏食品药品监督管理局2017年食品安全监督抽检（国抽部分）信息公示（第二十五期）。令人遗憾的是，青岛高科通信股份有限公司使用的小碗中沙门氏菌项目不合格。还有青岛市南区彤美老梁记快餐店使用的勺子中沙门氏菌项目不合格。"
    #sentence = "宁夏食品药品监督管理局2017年食品安全监督抽检（国抽部分）信息公示（第二十五期）"
    sentence2= "火锅调味料类:威海乳山市九品老灶火锅店使用的火锅底料中的可待因、吗啡项目不合格。 　　熟肉制品类:泰安开发区幸福家园酒店销售的酱鸡中苯甲酸项目不合格。曲阜市鑫盛清真园饭店销售的熟羊肉中亚硝酸盐项目不合格。济宁北湖省级旅游度假区王家羊肉馆销售的熟羊肉中亚硝酸盐项目不合格。临沂郯城县佳标羊肉馆销售的红烧肉中亚硝酸盐项目不合格。日照市东港区成记小厨特色小吃店销售的酱猪手中亚硝酸盐项目不合格。 　　油炸面制品类:菏泽银座集团股份有限公司菏泽成武分公司销售的手撕麻花中铝的残留量项目不合格。青岛崂山区王一家快餐店销售的油条中铝的残留量项目不合格。泰安市泰山景区李猛炒鸡店销售的油条中铝的残留量项目不合格。威海乳山市尚通餐厅销售的油条中铝的残留量项目不合格。临沂临沭县老山寨煲香鸡店销售的油条中铝的残留量项目不合格。日照市东港区小于糁馆销售的油条中铝的残留量项目不合格。日照市东港区麟州糁馆销售的油条中铝的残留量项目不合格。 　　对上述抽检中发现的不合格产品,生产经营企业所在地食药监部门已责令企业查清产品流向,召回、下架不合格产品,控制风险,立案调查,并分析原因进行整改"
    init_model()
    #func = getQ
    func = getQ
    le = func("null")
    fp(le)
    release_model()
    endtime = datetime.datetime.now()
    print (endtime - starttime).seconds,'s'