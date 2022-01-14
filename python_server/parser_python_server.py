from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from lxml import etree
from bs4 import BeautifulSoup
import json
import requests
import random

swedish_prepositions = ["om","ovanför","tvärsöver","efter","mot","bland","runt","som","på","vid","före","bakom","nedan","under","bredvid","mellan","bortom","men","av","trots","ner","under","förutom","för","från","i","inuti","in i","nära","nästa","av","på","mittemot","ut","utanför","över","per","plus","runt","sedan","än","genom","tills","till","mot","under","olik","tills","upp","via","med","inom","utan","enligt","nära","inuti","nära","bredvid","utanför","före","utöver","framför","ovanpå"]

#set up our python server
app = Flask(__name__)
CORS(app)
@app.route("/", methods=['POST'])
def main():

    #we get the content of the wikipedia page from the frontend
    pagetext = BeautifulSoup(request.json['pagetext'], 'html.parser')

    #we look through the html/xml tags and get the text from it, making sure to preserve the structure
    xml_tags = pagetext.find_all('p')
    sentences_list = list()
    for xml_tag_element in xml_tags:
        xml_tag_text = str(xml_tag_element.get_text())
        sentences_list.append(xml_tag_text)
    
    #'gappyboi' is an arbitrary string which is used to track the gaps between paragraphs; needs to be a unique string
    joined_text = 'gappyboi ' + ' gappyboi '.join(sentences_list) + ' gappyboi'

    #we ping the sparv/språkbanken server to get pos tags related to the text from the wikipedia article
    url = 'https://ws.spraakbanken.gu.se/ws/sparv/v2/?settings={"positional_attributes":{"dependency_attributes":[],"lexical_attributes":["pos"],"compound_attributes":[]}}'
    pos_tagged = requests.post(url, data={"text": joined_text})
    
    #we will process the data we get from sparv and organise it in two correlated lists
    #one list contains the pos tags, the other contains the words themselves
    pos_tags_list = list()
    words_list = list()
    sparv_response_pos_tagged = etree.fromstring(pos_tagged.content)
    for child in sparv_response_pos_tagged[1][0][0]:
        for grandchild in child:
            pos_tags_list.append(json.loads(str(grandchild.attrib).replace("'", '"'))["pos"])
            words_list.append(str(grandchild.text))
    
    #we need to structure the pos tags/text in the same way that it fits into the wikipedia website, so we can replace the text appropriately
    pos_tags_list_of_lists = list() 
    words_list_of_lists = list()
    previous_gap = 0
    dropdown_box_index = 0
    for i in range(len(pos_tags_list)):
        #we check if the pos tag is a preposition, we can replace it with our dropdown box
        dropdown_box_id = "dropdown" + str(dropdown_box_index)
        if pos_tags_list[i] == "PP":
            real_pp = [words_list[i]]
            random_pps = random.choices(swedish_prepositions, k=3)
            all_pps = random_pps + real_pp
            random.shuffle(all_pps)
            correct_answer_colour = ['green' if pp == real_pp[0] else 'red' for pp in all_pps]
            words_list[i] = f"""<span>
                    <select class="dropdownmenu" id="{dropdown_box_id}" onchange="$(document.getElementById('{dropdown_box_id}')).css('color', this.value)">
                        <option value="blue"> </option>
                        <option value="{correct_answer_colour[0]}">{all_pps[0]}</option>
                        <option value="{correct_answer_colour[1]}">{all_pps[1]}</option>
                        <option value="{correct_answer_colour[2]}">{all_pps[2]}</option>
                        <option value="{correct_answer_colour[3]}">{all_pps[3]}</option>
                    </select>
                </span>
            """
            dropdown_box_index += 1
        if words_list[i] == "gappyboi": #here we separate the sections originally in our html code
            pos_tags_list_of_lists.append(pos_tags_list[previous_gap+1:i])
            words_list_of_lists.append(words_list[previous_gap+1:i])
            previous_gap = i
        

    #we go through the original html/xml and replace it with the text that we get back from sparv. We do this to ensure that there is a correlation between our pos tags and text
    xml_tags = pagetext.find_all('p')
    i = 0
    for xml_tag_element in xml_tags:
        new_soup = BeautifulSoup('<p>'+' '.join(words_list_of_lists[i]).replace(' ,',',').replace(' .','.').replace('( ', '(').replace(' )',')')+'</p>', 'html.parser')
        xml_tag_element.replace_with(new_soup)
        i += 1
    
    print("Request done.")

    #we give back the modified html/xml, with the quiz, to the frontend to display it
    return {"myresponse": str(pagetext)}
