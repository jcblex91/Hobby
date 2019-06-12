import bitly_api
import csv

API_USER = "o_3kr02js6o"
API_KEY = "R_4218fa246fd84fdd818aadeb2d28728e"

b = bitly_api.Connection(API_USER, API_KEY)

#Generated lins.csv file
with open('links.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['LongUrl','TinyUrl'])

# Reading sheet.csv file
with open('sheet.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        response = b.shorten(uri = row)
        with open('links.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow([str(row),str(response['url'])])

