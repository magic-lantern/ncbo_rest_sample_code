from urllib import request
import json
import os
from pprint import pprint

REST_URL = "http://data.bioontology.org"
API_KEY = ""

def get_json(url):
    opener = request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read().decode())

# Get the available resources
resources = get_json(REST_URL + "/")

# Follow the ontologies link by looking for the media type in the list of links
media_type = "http://data.bioontology.org/metadata/Ontology"
found_link = ""
for link, link_type in resources["links"]["@context"].items():
    if media_type == link_type:
        found_link = link

# Get the ontologies from the link we found
ontologies = get_json(resources["links"][found_link])

# Get the name and ontology id from the returned list
ontology_output = []
for ontology in ontologies:
    ontology_output.append(ontology["name"] + "\n" + ontology["@id"] + "\n\n")

# Print the first ontology in the list
pprint(ontologies[0])

# Print the names and ids
print("\n\n")
for ont in ontology_output:
    print(ont)
