import string
import random

n = 10000000
first_names = ['Alex', 'Jaleel', 'Gaurav', 'Lynn', 'Barzan', 'Qijun', 'Yitian',
                'Fangzhou', 'Chien-Wei', 'Ryan', 'Kevin', 'Ahmad', 'Mengmeng',
                'Dong-Hyeon', 'Preeti', 'Zhizhong', 'Muhammed', 'Sheng',
                'Yicong', 'Dezhou', 'Junming', 'Isaac', 'Abraham', 'Charles',
                'Cheng-Yi', 'Joshua', 'Dong', 'Fang-Yi', 'Hertina', 'Yang',
                'Mason', 'Kiarash', 'James', 'Ye', 'Jiang']
last_names = ['Lancaster', 'Salhi', 'Madan', 'Garrett', 'Mozafari', 'Jiang',
                'Chen', 'Xing', 'Huang', 'Wawrzaszek', 'Eykholt', 'Tajik', 'Jie',
                'Park', 'Ramaraj', 'Zhang', 'Uluyol', 'Xie', 'Zhang', 'Jiang',
                'Liu', 'Bowen', 'Addisie', 'Welch', 'Lee', 'Cheng', 'Yoon', 'Yu',
                'Kurnia', 'Wright', 'Rahbar']
year_standings = ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth']
companies = ['Microsoft', 'Snapchat', 'Facebook', 'Google', 'AirBNB', 'Twilio',
                'Amazon', 'Wolverine Trading', 'Cisco', 'Oracle', 'IBM',
                'Intel', 'Twitter', 'Apple', 'Qualcomm', 'Sony', 'Disney',
                'Symantec', 'Indeed', 'RetailMeNot', 'Etsy', 'Fitbit', 'GoPro',
                'Tesla', 'Ford', 'Visa', 'Discover', 'SanDisk', 'Palantir']
favorite_classes = ['EECS583', 'EECS584', 'EECS586', 'EECS595', 'EECS281', 
                    'EECS280', 'EECS376', 'EECS484', 'EECS485', 'EECS494', 
                    'EECS482', 'EECS582', 'EECS475', 'EECS575', 'EECS370'
                    'EECS183', 'ECON409', 'CLCIV372', 'ART101', 'HIST101']
majors = ['CSE', 'EE', 'HIST', 'ART', 'CLCIV', 'BME', 'CS', 'ME', 'IOE', 'NERS',
            'AERO', 'BIO', 'CHEM', 'ECON', 'FIN', 'BUS', 'CHEME', 'MSE', 'N/A']
tuition_types = ['In State', 'Out Of State', 'International']
birth_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 
                'Oct', 'Nov', 'Dec']
genders = ['M', 'F']

outfile = open("StudentTable-" + str(n) + ".json", 'w+')

for i in range(n):
    string = "{\"StudentID\":" + str(i) + ","
    string = string + "\"FirstName\":\"" + random.choice(first_names) + "\","
    string = string + "\"LastName\":\"" + random.choice(last_names) + "\","
    string = string + "\"Gender\":\"" + random.choice(genders) + "\","
    string = string + "\"GPA\":" + "{0:.2f}".format(random.uniform(1.5, 4.0)) + ","
    string = string + "\"Year\":\"" + random.choice(year_standings) + "\","
    string = string + "\"Major\":\"" + random.choice(majors) + "\","
    string = string + "\"TuitionType\":\"" + random.choice(tuition_types) + "\","
    string = string + "\"FavoriteClass\":\"" + random.choice(favorite_classes) + "\","
    string = string + "\"Company\":\"" + random.choice(companies) + "\","
    string = string + "\"StartingSalary\":" + str(random.randint(80,130)*1000) + ","
    string = string + "\"BirthMonth\":\"" + random.choice(birth_months) + "\","
    string = string + "\"BirthDay\":" + str(random.randint(1,28)) + ","
    string = string + "\"BirthYear\":" + str(random.randint(1988,1998)) + ","
    string = string + "\"RandInt\":" + str(random.randint(1,n))
    string = string + "}\n"
    outfile.write(string)

outfile.close()
