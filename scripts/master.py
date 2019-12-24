import format


if __name__ == '__main__':
    with open('articles.json') as json_file:
        data = json.load(json_file)
        writeCSV(data)

            