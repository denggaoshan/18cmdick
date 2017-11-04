#coding=utf-8
import json
import codecs
import datetime
import CJNLP as cjn
import CJNLP

#读取结果文件内容为Dict格式
def get_json_list_from(filename='../DATA_T_RESULT.txt'):
    result = []
    f = codecs.open(filename,'r', 'utf-8')
    for line in f.readlines():
        #print line
        rj = json.loads(line)
        result.append(rj)
    f.close()
    return result

#生成一条新的实体
def create_ent(eventLevel=u"负向", name="", digest="", keywords=""):
    ent = { "name":name, "digest": digest, "keywords":keywords, "eventLevel":eventLevel}
    return ent
#根据实体集合生成JSON
def create_json_byEntitiesSet(entities):
    ents = []
    for e in entities:
        ents.append(create_ent(name=e.decode('utf-8')))
    return ents
#生成一条新的新闻记录
def create_newsRecord(newsId, ent_json):
    newsRecord = {"newsId":newsId, "entities":ent_json}
    return newsRecord

#得到识别命名实体后的数据 newsId ,entities
def get_process_data(data):
    result = []
    i = 1
    cjn.init_model()
    for news in data:
        print 'process news ', i
        i += 1
        ent_set = cjn.getQ(unicode.encode(news['body']))
        ent_json = create_json_byEntitiesSet(ent_set)
        record = create_newsRecord(news['newsId'], ent_json)
        result.append(record)
    cjn.release_model()
    return result

def save_submission(results, filename='sub[{0}].txt'.format(datetime.datetime.now().strftime('%m-%d#%H-%M'))):
    print 'save ', filename
    f = codecs.open(filename, "w", "utf-8")
    for i in range(len(results)):
        tr = json.dumps(results[i],ensure_ascii=False, separators=(',',':'))
        f.write(tr+"\r\n")
    f.close()

if __name__ == "__main__":
    test_json = get_json_list_from(filename="../DATA_TEST.txt")
    process_test_data = get_process_data(test_json)
    save_submission(process_test_data, 'test_entities.txt')

    train_json = get_json_list_from(filename='../DATA_T.txt')
    process_train_data = get_process_data(train_json)
    save_submission(process_train_data, 'train_entities.txt')

if __name__ == "__main1__":

    ch = []
    if ch == "":
        print 1