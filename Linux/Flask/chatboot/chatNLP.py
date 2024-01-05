# new ai chatbot with nlp
import spacy
nlp = spacy.load("en_core_web_sm")

from nltk.metrics import jaccard_distance
document = """

Hello to, my name is Snow from TechLabs. How can I help you?

The RobotLab is where we run workshops and trials of implementations on our humanoid robots.

Dennis Biström is an IT-Lecturer at Arcada UAS where he teaches full stack web programming and data managing, visualization and engineering.
Denise Biström is an IT-Lecturer at Arcada UAS where he teaches full stack web programming and data managing, visualization and engineering.
Denny's Biström is an IT-Lecturer at Arcada UAS where he teaches full stack web programming and data managing, visualization and engineering.

Krista  is a PhD trainer, project manager and researcher at the Department of Business Management. 

Kuvaja-Adolfsson is an IT Engineer and previous practical nurse from Sweden with a new found passion in IT. 
Christopher is an IT Engineer and previous practical nurse from Sweden with a new found passion in IT. 

Arcada is a multi-professional University of Applied Sciences in Finland.

Thank you for asking robot, I m just a computer program, so I don't have feelings, but I'm here and ready to help you with any questions or information you might need. How can I assist you today?
 
"""


class ReadingComprehensionSolverSpacy:
    def __init__(self, corpus) -> None:
        self.nlp = spacy.load('en_core_web_sm')
        self.set_corpus(corpus)

    def __str__(self) -> str:
        return "spaCy"
    
    def set_corpus(self, document) -> None:
        self.document = document
        self.sentences = [sent.text for sent in self.nlp(document).sents]
    
    def preprocess(self, text) -> list:
        return [token.lemma_.lower().strip() for token in self.nlp(text) if not token.is_stop and not token.is_punct and not token.is_space]
    
    def solve(self, question) -> str:
        # Process the question
        question_tokens = self.preprocess(question)

        # Score the similarity between the question and each sentence
        scores = []
        for sentence in self.sentences:
            sentence_tokens = self.preprocess(sentence)
            score = 1 - jaccard_distance(set(sentence_tokens), set(question_tokens))
            scores.append(score)
        
        # The sentence with the highest similarity
        top_index = scores.index(max(scores))
        top_sentence = self.sentences[top_index]
        return top_sentence



rcs = ReadingComprehensionSolverSpacy(document)
def askRobot(questions):
    for question in questions:
        return rcs.solve(question)