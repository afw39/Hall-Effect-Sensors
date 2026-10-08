# Creating JSON config file in Python

apparently there are two methods to write in the json file
1. using `json.dumps()`
2. using `json.dump()`

1. `json.dumps()` takes python object as parameter.
- first, need to import json module. `json.dumps()` method serialises (conversion of data into series of bytes)
python object into JSON formatted string and `write()` method writes that formatted JSON string to the file
`tutswiki.json`

```
import json

artcicle_info = {
    "domain" : "tutswiki",
    "language" : "python",
    "date" : "11/09/2020",
    "topic" : "config file"
}
myJSON = json.dumps(article_info)

with open("tutswiki.json", "w") as jsonfile:
    jsonfile.write(myJSON)
    print("write successful")
```

the 'w' creates the file in the current working directory if it doesn't already exist

so from this code, the file: "tutswiki.json" is created:

{
    "domain" : "tutswiki",
    "langauge" : "python",
    "date" : "11/09/20202",
    "topic": "config file"
}

2. using `json.dump()`, has no serialising of python object to JSON string. Instead, it stores the python object as
JSON formatted data into the JSON file, takes python object and file pointer as parameters

```
import json

article_info = {
    "domain": "tutswiki",
    "language": "python",
    "date": "11/09/2020",
    "topic": "config file"
}
with open("tutswiki.json", "w") as jsonfile:
    json.dump(article_info, jsonfile)
```

this cretes the file "tutswiki.json" (exactly the same as above)

# Reading a key from JSON config file

we can rad a JSON file using `json.load()` method which deserialises the JSON object to python object, dictionary. 
This method takes file pointer as its parameters.
```
import json

with open("tutswiki.json", "r") as jsonfile:
    data = json.load(jsonfile)
    print("Read successful")
print(data)
```
then this will output the contents of the file (same as above)

NOTE: if want to deserialise a JSON string to a python object directly instead of reading from a file, we use
json.loads() method which takes a JSON string as a parameter, e.g.
```
import json

s = "{\"domain\": \"tutswiki\", \"language\": \"python\"}"
data = json.loads(s)
print(data)
```
output is same again, except has "Process finished with exit code 0"

# Updating a key in JSON config file

Let's say that we want to update the date to `12/09/2020`. First, we will read the data, update the required values,
and then finally write to the file as done below

```
import json

article_info = {
    "domain": "tutswiki",
    "language": "python",
    "date": "11/09/2020",
    "topic": "config file"
}

with open("tutswiki.json", "r") as jsonfile:
    data = json.load(jsonfile) # reading the file
    print("read successful")
    jsonfile.close()

data['date'] = '12/09/2020' # updating, before it was 11/09/2020
print("date updated from 11/09/2020 to 12/09/2020")
with open("tutswiki.json, "w") as jsonfile:
    myJSON = json.dump(data, jsonfile)  # writing to the file
    print("write successful")
    jsonfile.close()
```
The output of this is the print statements, and the file has the new date in it


