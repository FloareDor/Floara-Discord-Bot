import discord
from discord.ext import commands
import pickle
import tensorflow
import numpy as np
import json
import nltk
import random
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from googletrans import Translator
trans = Translator()

physical_devices = tensorflow.config.list_physical_devices('GPU') 
tensorflow.config.experimental.set_memory_growth(physical_devices[0], True)

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes =pickle.load(open('classes.pkl', 'rb'))
search_limit = 50
model = load_model('chatbotmodel.h5')
print(words)
class chat_cog(commands.Cog):
    def __init__(self, client):
        self.client = client

    def clean_up_sentence(self,sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self,sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(words)
        for w in sentence_words:
            for i, word in enumerate(words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)
    def predict_class(self,sentence):
        bow = self.bag_of_words(sentence)
        res = model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]

        results.sort(key = lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent' : classes[r[0]], 'probability': str(r[1])})
        return return_list

    def get_response(self,intents_list, intents_json):
        ans = "I don't think I understand that"
        tag = intents_list[0]['intent']
        #print(tag)
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                print(float(intents_list[0]['probability']))
                if float(intents_list[0]['probability']) > 0.53:
                    ans = result
        return ans
    
    @commands.command()
    async def floara(self,ctx,*,arg):
        temp = str(arg)
        src_code = trans.detect(temp).lang
        # print(src_code)
        if src_code != 'en':
            temp = trans.translate(temp, src = src_code, dest = 'en').text
            message = str(temp)
            ints = self.predict_class(message)
            res = self.get_response(ints, intents)
            #res = trans.translate(res, src = 'en', dest = src_code).text
            await ctx.send(res)
        else:
            message = str(temp)
            ints = self.predict_class(message)
            res = self.get_response(ints, intents)
        #res = trans.translate(res, src = 'en', dest = src_code).text
            await ctx.send(res)
        print(temp)

#while True:
#   temp = input()
#   message = str(temp)
#   ints = predict_class(message)
#   result = get_response(ints, intents)
#   print(result)
