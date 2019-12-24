import json

with open('articles.json') as json_file:
    data = json.load(json_file)
    print data
    #for p in data['people']:
     #   print('Subtitle: ' + p['subtitle'])
      #  print('')