import datetime
import csv
import webapp2
import StringIO
import json

from models import ExecutiveDirectors


class MainHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = '/warm-directors'
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write("""Upload File: <input type="file" name="file"><br> """)
        self.response.out.write("""<input type="submit" name="submit" value="Submit">""")
        self.response.out.write("""</form></body></html>""")


class WarmDirectorsHandler(webapp2.RequestHandler):

    @staticmethod
    def read_csv():

        with open('assets/executive_directors_en.csv', newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='\'')

        return reader

    def post(self):
        #csv format: name,photo_link,place_of_birth,start_date,end_date,appointment,bio,ref_links,party
        uploaded_file = self.request.get('file')
        reader = csv.reader(uploaded_file.splitlines(), delimiter='\t')

        i = 0

        for row in reader:
            if i == 0:
                i += 1
                continue
            director = ExecutiveDirectors()
            director.directorName = row[0]
            director.directorPhotoKey = row[1]
            director.placeOfBirth = row[2]
            director.mandates = json.loads(row[3])
            director.appointment = int(row[4])
            director.biography = row[5]
            director.refLinks = json.loads(row[6])
            director.politicalPartyAffinity = row[7]
            director.put()

            i += 1
        self.response.out.write('done')


APP = webapp2.WSGIApplication([('/warm-directors', WarmDirectorsHandler),
                                  ('/upload', MainHandler)],
                              debug=True)