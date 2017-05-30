# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import os
import shutil
import csv
import requests
import json
import nltk
import spacy
import numpy as np

def deleteAllFolders():
    directory="ML20MAugmentationTextsAPIsDataGrabberData"
    shutil.rmtree(directory, ignore_errors=True)

def createNecessaryFolders():
    operationSuccessful=False
    directory="ML20MAugmentationTextsAPIsDataGrabberData"
    if not os.path.exists(directory):
        os.makedirs(directory)
        subDirectory1=directory+"/dataFromTMDBAPI"
        os.makedirs(subDirectory1)
        subDirectory1a=subDirectory1+"/overviews"
        os.makedirs(subDirectory1a)
        subDirectory1b=subDirectory1+"/reviews"
        os.makedirs(subDirectory1b)
        subDirectory1c=subDirectory1+"/tokenizedTMDbMovieData"
        os.makedirs(subDirectory1c)
        #reviews as lists of strings
        subDirectory2=directory+"/dataFromOMDBAPI"
        os.makedirs(subDirectory2)
        subDirectory2a=subDirectory2+"/fullPlots"
        os.makedirs(subDirectory2a)
        subDirectory2b=subDirectory2+"/shortPlots"
        os.makedirs(subDirectory2b)
    else:
        subDirectory1=directory+"/dataFromTMDBAPI"
        if not os.path.exists(subDirectory1):
            os.makedirs(subDirectory1)
            subDirectory1a=subDirectory1+"/overviews"
            os.makedirs(subDirectory1a)
            subDirectory1b=subDirectory1+"/reviews"
            os.makedirs(subDirectory1b)
            subDirectory1c=subDirectory1+"/tokenizedTMDbMovieData"
            os.makedirs(subDirectory1c)
        else:
            subDirectory1a=subDirectory1+"/overviews"
            if not os.path.exists(subDirectory1a):
                os.makedirs(subDirectory1a)
            subDirectory1b=subDirectory1+"/reviews"
            if not os.path.exists(subDirectory1b):
                os.makedirs(subDirectory1b)        
            subDirectory1c=subDirectory1+"/tokenizedTMDbMovieData"
            if not os.path.exists(subDirectory1c):
                os.makedirs(subDirectory1c)
        subDirectory2=directory+"/dataFromOMDBAPI"
        if not os.path.exists(subDirectory2):
            os.makedirs(subDirectory2)
            subDirectory2a=subDirectory2+"/fullPlots"
            os.makedirs(subDirectory2a)            
            subDirectory2b=subDirectory2+"/shortPlots"
            os.makedirs(subDirectory2b)
        else:
            subDirectory2a=subDirectory2+"/fullPlots"
            if not os.path.exists(subDirectory2a):
                os.makedirs(subDirectory2a)
            subDirectory2b=subDirectory2+"/shortPlots"
            if not os.path.exists(subDirectory2b):
                os.makedirs(subDirectory2b)
    operationSuccessful=True
    return operationSuccessful
    

def getTMDbReviews(tmdbId,apiKey):
    requestString = "https://api.themoviedb.org/3/movie/%s/reviews?api_key=%s"% (tmdbId, apiKey)
    response = requests.get(requestString)
    if response.status_code == 200:
        movieReviewData=response.json()
        #print("movieReviewData: ",movieReviewData)
        movieReviews = ""
        if movieReviewData['total_results'] > 0:
            reviews = movieReviewData['results']
           #print("len(reviews): ",len(reviews))
           #print("reviews: ",reviews)            
            for review in reviews:
               #print("review: ",review)
                reviewFormatted = str.replace(review['content'], '\n', '')
                reviewFormatted = str.replace(reviewFormatted, '\r', '')
                movieReviews+=" "
                movieReviews+=reviewFormatted.lower()
                #print("movieReviews: ",movieReviews)
            return movieReviews
        else:
            return movieReviews
    else:
       #print("API %s error" % response.status_code)
       pass

def loadMoviesLinks():
    moviesLinksList = []
    tmdbIdDict={}
    with open("ml-20m/links.csv", "r") as file:
        reader = csv.reader(file, delimiter = ',')
        for row in reader:
            if row[0].isdigit() and int(row[0]) > 0:
                moviesLinksList.append(row)
               #print("row: ",row)
    for tempMoviesLinksListRow in moviesLinksList:
        #print("tempMoviesLinksListRow: ",tempMoviesLinksListRow)
        tempMovieIdIndex=eval(tempMoviesLinksListRow[0])
        tempTmdbIdIndex=tempMoviesLinksListRow[2]
        tmdbIdDict[tempMovieIdIndex]=tempTmdbIdIndex
    return moviesLinksList,tmdbIdDict

def getTMDbMovieData(tmdbId,apiKey):
    movie = {}
    requestString = "https://api.themoviedb.org/3/movie/%s?api_key=%s"% (tmdbId, apiKey)
    response = requests.get(requestString)
    if response.status_code == 200:
        movie_data=response.json()
        #print("movie_data: ",movie_data)
        #print()
        movie['id'] = movie_data['id']
        movie['title'] = movie_data['title']
        #movie['plot'] = movie_data['overview'].lower()
        movie['overview'] = movie_data['overview'].lower()
        movie['reviews'] = getTMDbReviews(tmdbId,apiKey)
        return movie
    else:
       #print("API %s error" % response.status_code)
        movie['id'] = ""
        movie['title'] = ""
        movie['overview'] = ""
        movie['reviews'] = ""
    return movie

def getOMDbMovieData(imdbId):
    omdbId="tt"+imdbId
    requestString = "http://www.omdbapi.com/?i=%s&plot=full"% (omdbId)
    response = requests.get(requestString)
    if response.status_code == 200:
        movie_data = response.json()
        movie = {}
        movie['id'] = movie_data['imdbID']
        movie['title'] = movie_data['Title']
        movie['fullPlot'] = movie_data['Plot'].lower()
    else:
       #print("There was an API %s error" % response.status_code)
       pass
    requestString = "http://www.omdbapi.com/?i=%s&plot=short"% (omdbId)
    response = requests.get(requestString)
    if response.status_code == 200:
        movie_data = response.json()
        movie['shortPlot'] = movie_data['Plot'].lower()
        return movie
    else:
       #print("There was an API %s error" % response.status_code)
       pass



def saveTMDbMovieDataRecord(movieId,TMDbMovieDataRecord):
    print("movieId: ",movieId)
    print("TMDbMovieDataRecord: ",TMDbMovieDataRecord)
    tempFileName="ML20MAugmentationTextsAPIsDataGrabberData/dataFromTMDBAPI/overviews/"+str(movieId)
    tempFile = open(tempFileName,'w',  encoding="utf-8")
    tempFile.write(TMDbMovieDataRecord["overview"])
    tempFile.close
    tempFileName="ML20MAugmentationTextsAPIsDataGrabberData/dataFromTMDBAPI/reviews/"+str(movieId)
    tempFile = open(tempFileName,'w', encoding="utf-8")
    tempFile.write(TMDbMovieDataRecord["reviews"])
    tempFile.close


def saveOMDbMovieDataRecord(movieId,OMDbMovieDataRecord):
    tempFileName="ML20MAugmentationTextsAPIsDataGrabberData/dataFromOMDBAPI/fullPlots/"+str(movieId)
    tempFile = open(tempFileName,'w')
    tempFile.write(OMDbMovieDataRecord["fullPlot"])
    tempFile.close
    tempFileName="ML20MAugmentationTextsAPIsDataGrabberData/dataFromOMDBAPI/shortPlots/"+str(movieId)
    tempFile = open(tempFileName,'w')
    tempFile.write(OMDbMovieDataRecord["shortPlot"])
    tempFile.close

def saveTMDbMovieDataRecordTokensFromAll(movieId,tokenizedTMDbMovieData):
    tempFileName="ML20MAugmentationTextsAPIsDataGrabberData/dataFromTMDBAPI/overviews/"+str(movieId)+"_TokensFromAll"
    pass

def saveOMDbMovieDataRecordTokensFromAll(movieId,tokenizedOMDbMovieData):
    pass


def saveTokenizedTMDbMovieDataRecord(movieId,tokenizedTMDbMovieData):
    #print("movieId: ",movieId)
    tempFileName="ML20MAugmentationTextsAPIsDataGrabberData/dataFromTMDBAPI/tokenizedTMDbMovieData/"+str(movieId)
    tempFile = open(tempFileName,'w', encoding='utf-8')
    tempFile.write(repr(tokenizedTMDbMovieData))
    tempFile.close
    tempFileName+="_featuresList"
    tempFile = open(tempFileName,'w', encoding='utf-8')
    featuresList=[]
    tempKeysList=tokenizedTMDbMovieData.keys()
    for tempKeysListItem in tempKeysList:
       #print("tempKeysListItem: ",tempKeysListItem)
       #print("tokenizedTMDbMovieData[tempKeysListItem]: ",tokenizedTMDbMovieData[tempKeysListItem])
        if not(tokenizedTMDbMovieData[tempKeysListItem]==[]):
            tempValueList=tokenizedTMDbMovieData[tempKeysListItem]
            for tempValueListItem in tempValueList:
                featuresListNewItem=list(tempKeysListItem)
                featuresListNewItem.append(tempValueListItem)
               #print("featuresListNewItem: ",featuresListNewItem)
                featuresList.append(featuresListNewItem)
    tempFile.write(repr(featuresList))
    tempFile.close


def doSentenceTokenization(document):
    sentences=nltk.sent_tokenize(document)
    return sentences

def tokenizeMovieData(movieData):
    tokenizedMovieData={}
    tempMovieDataKeys=set(movieData.keys())
    #print("tempMovieDataKeys: ",tempMovieDataKeys)
    tempMovieDataKeys.remove("title")
    tempMovieDataKeys.remove("id")
    #print("tempMovieDataKeys: ",tempMovieDataKeys)    
    for tempKey in tempMovieDataKeys:
        tempSetOfTokensFromNAll=set()
        tempSetOfTokensFromNSubj=set()
        movieDataStr=str(movieData[tempKey])
       #print("TMDbMovieDataStr: ",TMDbMovieDataStr)
        tempSentencesList=doSentenceTokenization(movieDataStr)
        for tempSentence in tempSentencesList:
            veryTempSetOfTokensFromNSubj=set()
            veryTempSetOfTokensFromNAll=set()
            #print("tempSentence: ",tempSentence)
            # tempSentence = 'London is a big city in the United Kingdom.'
            doc = nlp(tempSentence)
            entityRecognizedWords=set()
            for ent in doc.ents :
                #print(ent.text)
                ## dodaje frazy z entity recognition, gdyż potem będą odrzucane
                veryTempSetOfTokensFromNAll.add(ent.text)
                for word in ent.text.split():
                    entityRecognizedWords.add(word)

                #print("recognized" + ent.text)

            ########### a co z stopwords?????????????
            for possibleNoun in doc:
                if (possibleNoun.is_stop==False)and(possibleNoun.text not in nltk.corpus.stopwords.words("english")):
                    if possibleNoun.text in entityRecognizedWords:
                        #print("odrzucone " + possibleNoun.text)
                        continue
                    veryTempSetOfTokensFromNAll.add(possibleNoun.text)
                    if possibleNoun.dep_=="nsubj":
                        veryTempSetOfTokensFromNSubj.add(possibleNoun.text)
#==============================================================================
#                else:
#                    #print("a stopword: ",possibleNoun.text)
#                     if possibleNoun.is_stop:
#                        #print("it is a spacy stopword.")
#                     if possibleNoun.text in nltk.corpus.stopwords.words("english"):
#                        #print("it is a nltk stopword.")
# 
#==============================================================================

            tempSetOfTokensFromNSubj.update(veryTempSetOfTokensFromNSubj)
            tempSetOfTokensFromNAll.update(veryTempSetOfTokensFromNAll)
        tempListOfTokensFromNSubj=list(tempSetOfTokensFromNSubj)
        tempListOfTokensFromNAll=list(tempSetOfTokensFromNAll)
       #print("tempListOfTokens: ",tempListOfTokens)
        tokenizedMovieData[(tempKey,"nsubj")]=tempListOfTokensFromNSubj
        tokenizedMovieData[(tempKey,"all")]=tempListOfTokensFromNAll
    return tokenizedMovieData


deleteAllFolders()
foldersOK=createNecessaryFolders()
#print("foldersOK: ",foldersOK)

moviesLinksList,tmdbIdDict=loadMoviesLinks()
#nltk.download()
apiKey = "3435d02bdf0a3873406a88ea6917e4e9"
OMDBapiKey="c7927ea2" #przedawnil sie


nlp=spacy.load('en')


tmdbMoviesDataList=[]
omdbMoviesDataList=[]


#for tempMovieIdTempListFileLine in tempMovieIdTempListFile:
#   tempMovieIdTempList.append(eval(tempMovieIdTempListFile[1]))
tempMovieIdTempListFile=open("ml-20m/ratings.csv",'r')
tempMovieIdTempList=[]
reader = csv.reader(tempMovieIdTempListFile, delimiter = ',')
for rowNumber in range(99):
    row=reader.__next__()
    if row[0].isdigit() and int(row[0]) > 0:
        tempMovieIdTempListItem=eval(row[1])
        #print("tempMovieIdTempListItem: ",tempMovieIdTempListItem)
        tempMovieIdTempList.append(tempMovieIdTempListItem)
tempMovieIdTempListFile.close()

firstMovieIdIndex=551
lastMovieIdIndex=551+1
#tempMovieIdTempList=list(range(firstMovieIdIndex,lastMovieIdIndex))


#for tempMovieIdIndex in range(firstMovieIdIndex,lastMovieIdIndex):
for tempMovieIdIndex in tempMovieIdTempList:
    #print("tempMovieIdIndex: ",tempMovieIdIndex)
    movieId=tempMovieIdIndex
    #print("moviesLinksList[tempMovieIdIndex]: ",moviesLinksList[tempMovieIdIndex])
   #print("movieId: ",movieId)
    #imdbId=moviesLinksList[tempMovieIdIndex][1]
    #tmdbId=moviesLinksList[tempMovieIdIndex][2]
    tmdbId=tmdbIdDict[tempMovieIdIndex]
    TMDbMovieData=getTMDbMovieData(tmdbId,apiKey)
   #print("TMDbMovieData: ",TMDbMovieData)
    saveTMDbMovieDataRecord(movieId,TMDbMovieData)
    tokenizedTMDbMovieData=tokenizeMovieData(TMDbMovieData)
   #print("tokenizedTMDbMovieData: ",tokenizedTMDbMovieData)
    tmdbMoviesDataList.append(TMDbMovieData)
    saveTokenizedTMDbMovieDataRecord(movieId,tokenizedTMDbMovieData)
    
    
#==============================================================================
#     OMDbMovieData=getOMDbMovieData(imdbId)
#    #print("OMDbMovieData: ",OMDbMovieData)
#     omdbMoviesDataList.append(OMDbMovieData)
#     tokenizedOMDbMovieData=tokenizeMovieData(OMDbMovieData)
#    #print("tokenizedOMDbMovieData: ",tokenizedOMDbMovieData)
#     saveOMDbMovieDataRecord(movieId,OMDbMovieData)
# 
#==============================================================================
   #print("TMDB and OMDB data successfully grabbed for (ML) movieId: ",tempMovieIdIndex)
   #print()
#tmdbIdsList=[tempMoviesLinksListElement[2] for tempMoviesLinksListElement in moviesLinksList[:3]]
#tmdbMoviesDataList = getTMDbMoviesData(tmdbIdsList,apiKey)





