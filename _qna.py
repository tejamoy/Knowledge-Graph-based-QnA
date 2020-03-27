import spacy
import pandas as pd
import json, re
from _getentitypair import GetEntity
from _complex import Complexx

class QuestionAnswer:
    """docstring for QuestionAnswer."""

    def __init__(self):
        super(QuestionAnswer, self).__init__()
        self.complex = Complexx()
        self.nlp = spacy.load('en_core_web_sm')

    def findanswer(self, question, numberOfPairs):
        p = self.complex.question_pairs(question)
        pair = p[0]

        f = open("database.json","r", encoding="utf8")
        listData = f.readlines()

        loaded = json.loads(listData[0])
        relQ = []
        relationQ = self.nlp(pair[1])

        for i in relationQ:
            relationQ = i.lemma_
            relQ.append(relationQ)

        objectQ = pair[3]
        subList = []
        timeQ = str(pair[4]).lower()
        placeQ = str(pair[5]).lower()
        # print(timeQ, placeQ)

        relationQ = " ".join(relQ)
        # print(relationQ)

        if pair[0] in ('who'):

            for i in loaded:
                relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
                relationSSS = " ".join([relation.lemma_ for relation in self.nlp(loaded[str(i)]["relation"])])

                relationS = [i.lemma_ for i in relationS]
                relationS = relationS[0]
                # print(relationSSS)

                if relationS == relationQ:
                    objectS = loaded[str(i)]["target"]
                    objectS = re.sub('-', ' ', objectS)

                    if objectS == objectQ:
                        if str(pair[4]) != "":
                            timeS = [str(time).lower() for time in self.nlp(loaded[str(i)]["time"])]
                            if timeQ in timeS:
                                answer_subj = loaded[str(i)]["source"]
                                subList.append(answer_subj)
                elif str(relationSSS) == str(relationQ):
                    objectS = loaded[str(i)]["target"]
                    objectS = re.sub('-', ' ', objectS)

                    if objectS == objectQ:
                        if str(pair[4]) != "":
                            timeS = [time for time in self.nlp(loaded[str(i)]["time"])]
                            if timeQ in timeS:
                                answer_subj = loaded[str(i)]["source"]
                                subList.append(answer_subj)
                        else:
                            answer_subj = loaded[str(i)]["source"]
                            subList.append(answer_subj)


            answer_subj = ",".join(subList)
            if answer_subj == "":
                return "None"
            else:
                return answer_subj

        elif pair[2] in ('what'):
            subjectQ = pair[0]
            subList = []

            for i in loaded:
                subjectS = loaded[str(i)]["source"]
                if subjectQ == subjectS:
                    relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
                    relationS = [i.lemma_ for i in relationS]
                    relationS = relationS[0]

                    if relationQ == relationS:
                        placeS = [str(place).lower() for place in self.nlp(loaded[str(i)]["place"])]
                        # print(placeQ, placeS)
                        if placeQ in placeS:
                            answer_obj = loaded[str(i)]["target"]
                            subList.append(answer_obj)

            answer_obj = ",".join(subList)
            if answer_obj == "":
                return "None"
            else:
                return answer_obj

        elif pair[2] in ('where'):
            subjectQ = pair[0]
            # print(relationQ, subjectQ)
            # print(pair[2])
            for i in loaded:
                subjectS = loaded[str(i)]["source"]
                # print(subjectQ, subjectS, numberOfPairs)
                if subjectQ == subjectS:
                    relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
                    relationS = [i.lemma_ for i in relationS]
                    relationS = relationS[0]
                    # print(relationS)

                    if relationQ == relationS:
                        answer_obj = loaded[str(i)]["place"]
                        return answer_obj

        elif pair[4] in ('when'):
            subjectQ = pair[0]
            print(subjectQ)
            # print(relationQ, subjectQ)
            # print(pair[2])
            for i in loaded:
                # if i.dep_ in ('obj'):
                # print(loaded[str(i)], "HERE we go")
                subjectS = loaded[str(i)]["source"]
                # print(type(subjectQ), type(subjectS), numberOfPairs)
                if subjectQ == subjectS:
                    relationS = [relation for relation in self.nlp(loaded[str(i)]["relation"])]
                    relationS = [i.lemma_ for i in relationS]
                    relBuffer = relationS
                    # print(relationS[0], relationS[1])

                    # print(relBuffer[1])

                    if len(relBuffer) < 2:
                        relationS = relBuffer[0]
                    else:
                        if str(relBuffer[1]).lower() == 'to':
                            relationS = " ".join(relationS)
                        else:
                            relationS = relationS[0]
                            extraIN = relBuffer[1].lower()

                    # print(loaded[str(i)]["date"], "Heloooo")

                    # print(relationQ, relationS)
                    if relationQ == relationS:
                        if loaded[str(i)]["time"] != '':
                            answer_obj = loaded[str(i)]["time"]
                        elif extraIN == "in" or extraIN == "on":
                            answer_obj = loaded[str(i)]["target"]
                        return answer_obj