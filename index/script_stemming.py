import utils.index_models as models
import nltk
#nltk.download('punkt')
import config_stemming as conf
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import re


stemmer = SnowballStemmer("english")
stopwords = nltk.corpus.stopwords.words('english')
#print(stopwords)


def stemming(text):
    tokens = word_tokenize(text)
    #tokens = [token.lower for token in tokens]
    #print(tokens)
    filtered_tokens =[]
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token.lower())
        if token in stopwords:
            filtered_tokens.remove(token)
   # print('* filtered tokens')
   # print(filtered_tokens)


    stems= [stemmer.stem(t) for t in filtered_tokens]
   # print('* print stems string')
    print(" ".join(stems))
    #models.connect_to_db(conf.DATABASE_FILENAME)
    #print("Saving new paper_text into papers_NR_NSW")
   # new_entry = models.Papers_NR_NSW.create(id=item.id,
                                          #  pdf_name=item.pdf_name,
                                            #paper_text=stems)
    #print("Number of rows modified: {0}".format(new_entry.save()))
    return " ".join(stems)
    #return "stemming for " + str(id)

def tokenize(paper_text):
    text = paper_text
    tokens = word_tokenize(text)
    print(tokens)

def tokenize_test():
    sample_sentence = "Hi, I am Maraise and trying NLTK. How are you doing today? The weather is nice today."
    print(sample_sentence)
    a = word_tokenize(sample_sentence)
    print (a)
    b = sent_tokenize(sample_sentence)
    print(b)
    #tokens = [ word for sent in nltk.sent_tokenize(paper_text)for word in nltk.word_tokenize(sent)]
   # tokens = ['hallo',  'hoi', 'alloha']
    #tokens = nltk.word_tokenize("hallo hoi ik ben maraise")
   # print('token_test')
    #print (pdf_name)
   # print (tokens)
    #return tokens


def load_data():
    models.connect_to_db(conf.DATABASE_FILENAME)
    return models.Papers_NR.select() #.where(models.Papers_NR.id <= "1")
    #return [q.paper_text for q in query]

    # print(len(query))
    # for item in query:
    #     paper_text = item.paper_text
    #     #id = item.id
    #    # print(item.pdf_name)
    #     #print(item.id)
    #     #print(item.paper_text)
    #     # new_entry = models.Papers_NR_NSW_STE.create(id=item.id,
    #     #                                         pdf_name=item.pdf_name,
    #     #                                        paper_text=item.paper_text)
    #     print("Number of rows modified: {0}".format(new_entry.save()))
    # return paper_text

def create_list_of_ids(first_id, n, max_id):
    ids = []
    last_id = first_id + n
    if first_id + n > max_id:
        last_id = max_id + 1
    for current_id in range(first_id, last_id):
            ids.append(current_id)
    return ids


def add_data(text):
    paper_text = text
    #new_paper_text = stemming(paper_text)
    models.connect_to_db(conf.DATABASE_FILENAME)
    last_id_query = models.Papers_NR_NSW_STE.select().order_by(models.Papers_NR_NSW_STE.id.desc()).limit(1)
    first_id = 1
    last_id = last_id_query[0].id
    increments = 10
    for i in range(first_id, last_id + 1, increments):
        papers_to_process = create_list_of_ids(i, increments, last_id)
        for paper_id in papers_to_process:
            paper_query = models.Papers_NR_NSW_STE.select().where(models.Papers_NR_NSW_STE.id == paper_id)
            paper_pdf_name = paper_query[0].pdf_name
            # is update the statement to use?
            new_entry = models.Papers_NR_NSW.update(id=paper_id,
                                                    pdf_name=paper_pdf_name,
                                                    paper_text=new_paper_text)
            print("Number of rows modified: {0}".format(new_entry.save()))
    models.close_connection()


def check_data():
    models.connect_to_db(conf.DATABASE_FILENAME)
    query = models.Papers_NR_NSW_STE.select().where(models.Papers_NR_NSW_STE.id <= "1")
    for item in query:
        print(item.pdf_name)
        print(item.paper_text)


    #paper_content = query[0].paper_text
   # paper_pdf_name = query[0].pdf_name
   # tokens = paper_content.strip().split()
   # print(tokens)
   #print(paper_content)
   # for row in tokens:
       # print(row)
       # print("*****")




def drop_papers_nr_nsw_table():
    models.connect_to_db(conf.DATABASE_FILENAME)
    models.Papers_NR_NSW_STE.drop_table()
    models.close_connection()

if __name__ == '__main__':
    drop_papers_nr_nsw_table()
    #load_data()
    papers = load_data()
    for paper in papers:
        stemmed_text = stemming(paper.paper_text)
        models.Papers_NR_NSW_STE.create(id=paper.id,
                                        pdf_name=paper.pdf_name,
                                        paper_text=stemmed_text)
    #edited_content = stemming(text)
    #drop_papers_nr_nsw_table()
    #add_data(text)
    #check_data()