import spacy
import random
from spacy.tokens import Doc
from spacy.training import Example

nlp = spacy.load("ru_core_news_md")
train_data = []
with open('train_data.csv', mode='r', encoding='utf-8') as f:
    for line in f:
        words, entities = line.split(',')[0].split(), line.split(',')[1].split()
        train_data.append([words, entities])

optimizer = nlp.initialize()
for itn in range(100):
    random.shuffle(train_data)
    for raw_text, entity_offsets in train_data:
        print(raw_text)
        print(entity_offsets)
        doc = nlp.make_doc(' '.join(raw_text))
        example = Example.from_dict(doc, {"entities": entity_offsets})
        nlp.update([example], sgd=optimizer)

ruler = nlp.add_pipe("entity_ruler", before='ner')
month_patterns = [{'label': 'DATE', 'pattern': [{'IS_DIGIT': True}, {'LOWER': 'мая'}]},
            {'label': 'DATE', 'pattern': [{'IS_DIGIT': True}, {'LOWER': 'января'}]},
            {'label': 'DATE', 'pattern': [{'IS_DIGIT': True}, {'LOWER': 'февраля'}]},
            {'label': 'DATE', 'pattern': [{'IS_DIGIT': True}, {'LOWER': 'марта'}]},
            {'label': 'DATE', 'pattern': [{'IS_DIGIT': True}, {'LOWER': 'апрель'}]},
            {'label': 'DATE', 'pattern': [{'IS_DIGIT': True}, {'LOWER': 'июня'}]},
            {'label': 'DATE', 'pattern': [{'IS_DIGIT': True}, {'LOWER': 'июля'}]},
            {'label': 'DATE', 'pattern': [{'IS_DIGIT': True}, {'LOWER': 'августа'}]},
            {'label': 'DATE', 'pattern': [{'IS_DIGIT': True}, {'LOWER': 'сентября'}]},
            {'label': 'DATE', 'pattern': [{'IS_DIGIT': True}, {'LOWER': 'октября'}]},
            {'label': 'DATE', 'pattern': [{'IS_DIGIT': True}, {'LOWER': 'ноября'}]},
            {'label': 'DATE', 'pattern': [{'IS_DIGIT': True}, {'LOWER': 'декабрь'}]}
            ]

time_patterns = [{'label' : 'TIME', 'pattern': [{'IS_DIGIT':True}, {'LOWER': 'утра'}]},
                {'label' : 'TIME', 'pattern': [{'IS_DIGIT':True}, {'LOWER': 'вечера'}]}]

ruler.add_patterns(month_patterns)
ruler.add_patterns(time_patterns)
nlp.to_disk("./final_output")
