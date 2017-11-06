import csv
with open('longsword.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	spamwriter.writerow(['ax', 'ay', 'az', 'gx', 'gy', 'gz'])
	asdf = 1
	spamwriter.writerow([str(asdf), 'Lovely Spam', 'Wonderful Spam'])
