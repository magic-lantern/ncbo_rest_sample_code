from urllib import request, parse
import json
import os
from pprint import pprint

REST_URL = "http://data.bioontology.org"
API_KEY = ""

def get_json(url):
    opener = request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read().decode())

def print_annotations(annotations, get_class=True):
    for result in annotations:
        class_details = get_json(result["annotatedClass"]["links"]["self"]) if get_class else result["annotatedClass"]
        print("Class details")
        print("\tid: " + class_details["@id"])
        print("\tprefLabel: " + class_details["prefLabel"])
        print("\tontology: " + class_details["links"]["ontology"])

        print("Annotation details")
        for annotation in result["annotations"]:
            print("\tfrom: " + str(annotation["from"]))
            print("\tto: " + str(annotation["to"]))
            print("\tmatch type: " + annotation["matchType"])

        if result["hierarchy"]:
            print("\n\tHierarchy annotations")
            for annotation in result["hierarchy"]:
                class_details = get_json(annotation["annotatedClass"]["links"]["self"])
                pref_label = class_details["prefLabel"] or "no label"
                print("\t\tClass details")
                print("\t\t\tid: " + class_details["@id"])
                print("\t\t\tprefLabel: " + class_details["prefLabel"])
                print("\t\t\tontology: " + class_details["links"]["ontology"])
                print("\t\t\tdistance from originally annotated class: " + str(annotation["distance"]))

        print("\n\n")

text_to_annotate = "The patient is status post previous median sternotomy.  The heart size is normal.  There is enlargement of the central pulmonary arteries which rapidly taper suggesting the possibility of pulmonary artery hypertension.  There is apparent bilateral upper lobe emphysema as well as minimal linear scarring in both upper lobes.  No confluent areas of consolidation are observed in either lungs, and there is no evidence of pleural effusion.  Degenerative changes are noted within the spine."

# Annotate using the provided text
annotations = get_json(REST_URL + "/annotator?text=" + parse.quote(text_to_annotate))

# print out annotation details
print_annotations(annotations)

# Annotate with hierarchy information
annotations = get_json(REST_URL + "/annotator?max_level=3&text=" + parse.quote(text_to_annotate))
print_annotations(annotations)

# Annotate with prefLabel, synonym, definition returned
annotations = get_json(REST_URL + "/annotator?include=prefLabel,synonym,definition&text=" + parse.quote(text_to_annotate))
print_annotations(annotations, False)
