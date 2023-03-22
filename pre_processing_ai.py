import json
from pathlib import Path
####################################
import torch
####################################
from datastructures import path, AlphabetV2
PathAIData = path
####################################
from Assets.data.model import NeuralNet
from Assets.data.nltk_utils import bag_of_words, stem, tokenize
####################################
#p.write('Hello world!', interval=0.25)

def AI_Objectification(Sentence : str, min_prob : float):
    """
    "Sentence" = the sentence that will be tokenized and compared with the patterns of the Json file


    if it finds a correlation between the sentence given in input and the json file:
    
    return tag, prob hit, intent, pattern, responses, failed responses , info , stemmedphrase

    else:
        return None

    """


    #DATA FILES
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    with open(str(PathAIData) + "\Assets\Data\intents.json", 'r') as json_data:
        intents = json.load(json_data)
    FILE = str(PathAIData) + "\Assets\Data\data.pth"
    data = torch.load(FILE,encoding='utf-8')

    #DATA VARIABLES
    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    #MODEL INJECT 
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    #TOKENIZE | BAG OF WORDS INJECT
    for word in AlphabetV2.AllCallers:
        Sentence = Sentence.replace(word,'').strip()

    Sentence = tokenize(Sentence.lower())
    #print(all_words)
    X = bag_of_words(Sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    #OUTPUTS
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    PROB_HIT = str(prob.item())
    #print("Prob_Hit: " + str(prob.item()))

    if prob.item() > min_prob:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return intent["tag"], PROB_HIT, intent, intent["patterns"], intent["responses"], intent["Failed Responses"] , intent["accept info"], [stem(word) for word in Sentence]
    else:
        return str(None), str(PROB_HIT), str(None), str(None), str(None), str(None) , str(None), str(None)