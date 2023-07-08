import os
import PyPDF2
import spacy
import string
import nltk
import string
from nltk.stem.wordnet import WordNetLemmatizer

import openai
import requests

### text extraction ###

# function to extract text from pdf
def extract_text_from_pdf(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_number in range(num_pages):
        page_obj = pdf_reader.pages[page_number]
        text += page_obj.extract_text()
    pdf_file.close()
    return text

# set path
pdf_file_path = '/Users/USER/Desktop/projects/NeuralNavigate/NeuralNavigate---Server/data/raw/BoundaryValueCaching.pdf'

# extract text from pdf
text = extract_text_from_pdf(pdf_file_path)


### text preprocessing and segmentation ###

nltk.download('punkt')

def preprocess_text(text):
    # lowercase text
    text = text.lower()

    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # tokenize text
    words = nltk.word_tokenize(text)

    return words

words = preprocess_text(text)


### NLU and knowledge extraction ###

# split the text into sentences (i.e. "segments")
sentences = text.split('. ')

# preprocess each sentence with the model
for sentence in sentences[:3]:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Explain the following text in simple terms: " + sentence,
        max_tokens=100, temperature=0
    )

print(response.choices[0].text.strip())


### topic identification ###



# nlp = spacy.load("en_core_web_sm")

# # Entity Recognition before cleaning
# entities = []
# for doc in documents:
#     spacy_doc = nlp(doc)
#     entities.append([(entity.text, entity.label_) for entity in spacy_doc.ents])

# # You can print the entities of each document if you wish
# for i, doc_entities in enumerate(entities):
#     print(f"Entities in document {i+1}:")
#     for entity, label in doc_entities:
#         print(f"{entity} ({label})")

# # Text preprocessing
# stop = set(stopwords.words('english'))
# exclude = set(string.punctuation)
# lemma = WordNetLemmatizer()

# def clean(doc):
#     stop_free = " ".join([word for word in doc.lower().split() if word not in stop])
#     punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
#     normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
#     return normalized

# documents_clean = [clean(doc).split() for doc in documents]