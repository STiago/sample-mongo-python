from mongoengine import *
import pymongo
from lxml import etree
import datetime

# DB connection
#db = pymongo.Connection()
db = connect('example')
db.drop_database('example')

# Candidates
class candidates(Document):
    id_candidates = StringField(min_value=1, unique=True)
    name = StringField(required = True)
    profession = StringField(required = True)
    recruiter = StringField(required = True)
    addr = EmbeddedDocumentField(address)
    grades = ListField(EmbeddedDocumentField(selection_process))
    
# Selection process
class selection_process(EmbeddedDocument):
    grade = StringField(max_length=1)
    phone_test = IntField()
    task_score = IntField()
    face_to_face = IntField()
    date = DateTimeField()

# Address
class address(EmbeddedDocument):
    number = IntField()
    street = StringField()
    city = StringField()
    zipcode = IntField()
    geoloc = GeoPointField()

# Insertion
def insert_candidate(n_name, city, profession, recruiter):
    api_base_url = 'http://maps.googleapis.com/maps/api/geocode/xml?address='

    requeriments = api_base_url + name + city
    tree = etree.parse(requeriments)

    addressXML = tree.xpath('//address_component')
    locationXML = tree.xpath('//location')

    numbXML = int(addressXML[0].xpath('//long_name/text()')[0])
    stXML = addressXML[1].xpath('//long_name/text()')[1]
    ctXML = addressXML[2].xpath('//long_name/text()')[2]
    zcodeXML = int(addressXML[6].xpath('//long_name/text()')[6])
    geolocXML = [float(locationXML[0].xpath('//lat/text()')[0]), float(locationXML[0].xpath('//lng/text()')[0])]

    myaddress = address(number=numbXML, street=stXML, city=ctXML, zipcode=zcodeXML, geoloc=geolocdXML)
    doc = candidates(name=n_name, id_candidates=candidates.objects.count() + 1, profession=profession, recruiter=recruiter, address=myaddress)
    doc.save()

# Fill DB
insert_candidate("Victoria Santiago", "London", "Software Engineer", "OHO-G")
insert_candidate("James Clark", "Oxford", "Software Developer", "SPL-A")
insert_candidate("Mike Silver", "London", "Software Engineer", "SEARCH-P")
insert_candidate("Marie Degutierre", "Paris", "Software Engineer", "NPM-C")
insert_candidate("Elisa", "London", "Software Engineer", "IDPP-G")
insert_candidate("Francisco Torres", "Madrid", "DevOps Engineer", "IDPP-G")

# Queries
print ("\nAll the candidates:")
for q in candidates.objects[:]:
    print (q.id_candidates, q.name, q.addr.street, q.addr.number, q.addr.zipcode, q.addr.city, q.addr.geoloc)

print ("\nName:")
q = candidates.objects(name="Victoria Santiago")
print (q[0].name)

print ("\nProfession:")
for q in candidates.objects(profession__ne="Software Engineer"):
    print (q.name)

print ("\nRecruiter:")
for q in candidates.objects(recruiter__ne="OHO-G"):
    print (q.recruiter)

print ("\nLocation:")
for q in candidates.objects(address__coord__within_distance=[(37.18, -3.60), 0.01]):
    print(q.name, q.addr.geoloc)



