from django.db import models

class Voter(models.Model):
    '''
    Store/represent the data from one runner at the Chicago Marathon 2023.
    BIB,First Name,Last Name,CTZ,City,State,Gender,Division,
    Place Overall,Place Gender,Place Division,Start TOD,Finish TOD,Finish,HALF1,HALF2
    '''
    # generic
    first_name = models.TextField()
    last_name = models.TextField()
    dob = models.DateField(auto_now=False, auto_now_add=False) # birth date

    # address
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.IntegerField()

    # voter info
    dor = models.DateField(auto_now=False, auto_now_add=False) # registration date
    party_affiliation = models.CharField(max_length=1)
    precinct_number = models.TextField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'
    

def parse_bool(s: str) -> bool:
    "Helper function to return if a string is True/False"
    return True if s == "TRUE" else False


def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    # delete all records as needed
    Voter.objects.all().delete()

    # open the file for reading
    filename = '/Users/willi/Downloads/newton_voters.csv'
    f = open(filename)
    f.readline()    # discard headers
    i = 0

    for line in f:

        i += 1
        line = line.strip()
        fields = line.split(',')

        try:

            # create a new instance of Result object with this record from CSV
            result = Voter(
                last_name=fields[1].strip(),
                first_name=fields[2].strip(),
                street_number=fields[3].strip(),
                street_name=fields[4].strip(),
                apartment_number=fields[5].strip(),
                zip_code=fields[6].strip(),
                dob=fields[7].strip(),
                dor=fields[8].strip(),
                party_affiliation=fields[9].strip(),
                precinct_number=fields[10].strip(),
                v20state=parse_bool(fields[11].strip()),
                v21town=parse_bool(fields[12].strip()),
                v21primary=parse_bool(fields[13].strip()),
                v22general=parse_bool(fields[14].strip()),
                v23town=parse_bool(fields[15].strip()),
                voter_score=fields[16].strip(),
            )
            result.save()
            # print(f'Created result: {result}')
        
        except Exception as e:
            print(f"Exception on line {i}: {str(e)}")
            print(f"Fields: {fields}")


"""
0 Voter ID Number
1 Last Name	
2 First Name	
3 Residential Address - Street Number	
4 Residential Address - Street Name	
5 Residential Address - Apartment Number	
6 Residential Address - Zip Code	
7 Date of Birth	
8 Date of Registration	
9 Party Affiliation	
10 Precinct Number	
11 v20state	
12 v21town	
13 v21primary	
14 v22general	
15 v23town	
16 voter_score"""