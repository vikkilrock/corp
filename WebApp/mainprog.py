from flask import Flask, render_template,request,session,flash
import sqlite3 as sql
import os
import random
import pandas as pd
PEOPLE_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/gohome')
def homepage():
    return render_template('home.html')

@app.route('/services')
def servicepage():
    return render_template('services.html')

@app.route('/coconut')
def coconutpage():
    return render_template('Coconut.html')

@app.route('/cocoa')
def cocoapage():
    return render_template('cocoa.html')

@app.route('/arecanut')
def arecanutpage():
    return render_template('arecanut.html')

@app.route('/paddy')
def paddypage():
    return render_template('paddy.html')

@app.route('/sugarcane')
def sugarcanepage():
    return render_template('sugercane.html')

@app.route('/wheat')
def wheatpage():
    return render_template('wheat.html')

@app.route('/pea')
def peapage():
    return render_template('pea.html')

@app.route('/mango')
def mangopage():
    return render_template('mango.html')

@app.route('/about')
def aboutpage():
    return render_template('about.html')


@app.route('/enternew')
def new_user():
   return render_template('signup.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['Name']
            phonno = request.form['MobileNumber']
            email = request.form['email']
            unm = request.form['Username']
            passwd = request.form['password']
            with sql.connect("agricultureuser.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO agriuser(name,phono,email,username,password)VALUES(?, ?, ?, ?,?)",(nm,phonno,email,unm,passwd))
                con.commit()
                msg = "Registered successfully  Please login"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("login.html", msg=msg)
            con.close()

@app.route('/userlogin')
def user_login():
   return render_template("login.html")

@app.route('/logindetails',methods = ['POST', 'GET'])
def logindetails():
    if request.method=='POST':
            usrname=request.form['username']
            passwd = request.form['password']

            with sql.connect("agricultureuser.db") as con:
                cur = con.cursor()
                cur.execute("SELECT username,password FROM agriuser where username=? ",(usrname,))
                account = cur.fetchall()

                for row in account:
                    database_user = row[0]
                    database_password = row[1]
                    if database_user == usrname and database_password==passwd:
                        session['logged_in'] = True
                        return render_template('home.html')
                    else:
                        flash("Invalid user credentials")
                        return render_template('login.html')

@app.route('/predictinfo')
def predictin():
   return render_template('info.html')


@app.route('/predict',methods = ['POST', 'GET'])
def predcrop():
    if request.method == 'POST':
        comment = request.form['comment']
        comment1 = request.form['comment1']
        #comment2 = request.form['comment2']
        data = comment
        data1 = comment1
        #data2 = int(comment2)
        # type(data2)
        print(data)
        print(data1)
        #print(data2)

        import pandas as pd

        dff = pd.read_csv("data/CropData.csv")
        #data = 'Mangalore'
        # input("Enter Location:")
        #data1 = 'Alluvial'
        # input("Enter Soil:")
        #data2 = 3
        # int(input("Enter Area:"))

        df1 = dff[dff['Location'].str.contains(data)]
        df2 = df1[df1['Soil'].str.contains(data1)]
        # print("df2:",df2)
        df2.to_csv('testnow.csv', header=False, index=False)

        if os.stat("testnow.csv").st_size == 0:
            print('empty file')
            return render_template('resultpred1.html')
        else:
            df2.to_csv('testnow.csv', header=True, index=False)
            data = pd.read_csv("data/CropData.csv")
            print('data', data)

            Type_new = pd.Series([])

            for i in range(len(data)):
                if data["Crops"][i] == "Coconut":
                    Type_new[i] = "Coconut"

                elif data["Crops"][i] == "Cocoa":
                    Type_new[i] = "Cocoa"

                elif data["Crops"][i] == "Coffee":
                    Type_new[i] = "Coffee"

                elif data["Crops"][i] == "Cardamum":
                    Type_new[i] = "Cardamum"

                elif data["Crops"][i] == "Pepper":
                    Type_new[i] = "Pepper"

                elif data["Crops"][i] == "Arecanut":
                    Type_new[i] = "Arecanut"

                elif data["Crops"][i] == "Ginger":
                    Type_new[i] = "Ginger"

                elif data["Crops"][i] == "Tea":
                    Type_new[i] = "Tea"

                else:
                    Type_new[i] = data["Crops"][i]

            data.insert(16, "Crop val", Type_new)
            data.drop(["Location", "Soil", "Crops"], axis=1,
                      inplace=True)
            data.to_csv("data/train.csv", header=False, index=False)
            data.head()

            avg1 = data['Rainfall'].mean()
            print('Rainfall avg:', avg1)
            avg2 = data['Ca'].mean()
            print('Ca avg:', avg2)
            avg3 = data['Humidity'].mean()
            print('Humidity:', avg3)

            avg4 = data['Mg'].mean()
            print('Mg:', avg4)
            avg5 = data['K'].mean()
            print('K:', avg5)
            avg6 = data['S'].mean()
            print('S:', avg6)
            avg7 = data['ph'].mean()
            print('ph:', avg6)
            avg8 = data['N'].mean()
            print('N:', avg8)
            avg9 = data['Lime'].mean()
            print('Lime:', avg9)
            avg10 = data['C'].mean()
            print('C:', avg10)
            avg11 = data['P'].mean()
            print('P:', avg11)
            avg12 = data['Moisture'].mean()
            print('Moisture:', avg12)

            avg13 = data['Ca'].mean()
            print('Ca:', avg13)
            testdata = {'Temperature': avg2,
                        'Humidity': avg3,
                        'ph': avg7,
                        'Rainfall': avg1,
                        'Ca': avg13,
                        'Mg': avg4,
                        'K': avg5,
                        'S': avg6,
                        'N': avg8,
                        'Lime': avg9,
                        'C': avg10,
                        'P': avg11,
                        'Moisture': avg12

                        }

            df7 = pd.DataFrame([testdata])
            df7.to_csv('data/test.csv', mode="w", header=False, index=False)

            import csv
            import math
            import operator

            def euclideanDistance(instance1, instance2, length):
                distance = 0
                for x in range(length):
                    distance += (pow((float(instance1[x]) - float(instance2[x])), 2))
                return math.sqrt(distance)

            def getNeighbors(trainingSet, testInstance, k):
                distances = []
                length = len(testInstance) - 1

                for x in range(len(trainingSet)):
                    dist = euclideanDistance(testInstance, trainingSet[x], length)
                    distances.append((trainingSet[x], dist))
                distances.sort(key=operator.itemgetter(1))
                neighbors = []
                for x in range(k):
                    neighbors.append(distances[x][0])
                return neighbors

            def getResponse(neighbors):
                classVotes = {}
                for x in range(len(neighbors)):
                    response = neighbors[x][-1]
                    if response in classVotes:
                        classVotes[response] += 1
                    else:
                        classVotes[response] = 1
                sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
                return sortedVotes[0][0]

            def getAccuracy(testSet, predictions):
                correct = 0
                for x in range(len(testSet)):
                    if testSet[x][-1] == predictions[x]:
                        correct += 1
                return (correct / float(len(testSet))) * 100.0

            trainingSet = []
            testSet = []
            with open('data/train.csv', 'r') as csvfile:
                lines = csv.reader(csvfile)
                dataset = list(lines)
                # print(dataset)



                for x in range(len(dataset) - 1):
                    for y in range(13):
                        dataset[x][y] = float(dataset[x][y])
                    trainingSet.append(dataset[x])

            with open('data/test.csv', 'r') as csvfile1:
                lines1 = csv.reader(csvfile1)
                # print(lines1)
                dataset1 = list(lines1)
                # print(dataset1)

                for p in range(len(dataset1)):
                    for q in range(13):
                        dataset[p][q] = float(dataset[p][q])
                    testSet.append(dataset1[p])

            print("trainingset:", trainingSet)
            print("testingset:", testSet)
            # print("1:",len(trainingSet))
            # print("2:",len(testSet))
            k = 1
            predictions = []
            for x in range(len(testSet)):
                neighbors = getNeighbors(trainingSet, testSet[x], k)
                response = getResponse(neighbors)
                print("\nNeighbors:", neighbors)
                print('\nResponse:', response)

                predictions.append(response)
                res12 = predictions
            accuracy = getAccuracy(testSet, predictions)
            # print('Accuracy: ' + repr(accuracy) + '%')
            dataset2 = pd.read_csv('testnow.csv')
            l = pd.unique(dataset2.iloc[:, 5])
            pred = random.choices(l, k=2)
            # ------------------2nd crop--------------------
            with open('data/train.csv', 'r') as csvfile:
                lines = csv.reader(csvfile)
                dataset = list(lines)
                # print(dataset)



                for x in range(len(dataset) - 1):
                    for y in range(13):
                        dataset[x][y] = float(dataset[x][y])
                    trainingSet.append(dataset[x])

            with open('data/test.csv', 'r') as csvfile1:
                lines1 = csv.reader(csvfile1)
                # print(lines1)
                dataset1 = list(lines1)
                # print(dataset1)

                for p in range(len(dataset1)):
                    for q in range(13):
                        dataset[p][q] = float(dataset[p][q])
                    testSet.append(dataset1[p])

            print("trainingset:", trainingSet)
            print("testingset:", testSet)
            # print("1:",len(trainingSet))
            # print("2:",len(testSet))
            k = 1
            predictions1 = []
            for x in range(len(testSet)):
                neighbors1 = getNeighbors(trainingSet, testSet[x], k)
                response1 = getResponse(neighbors1)
                print("\nNeighbors:", neighbors1)
                print('\nResponse:', response1)

                predictions1.append(response1)
                res121 = predictions1
            accuracy1 = getAccuracy(testSet, predictions1)
            df4 = dataset2[dataset2['Crops'].str.contains(pred[0])]
            df5 = dataset2[dataset2['Crops'].str.contains(pred[1])]
            # -------------------------------------------------
            import matplotlib.pyplot as plt

            # x = [0, 1, 2]
            # y = [accuracy, 0, 0]
            # plt.title('Accuracy')
            # plt.bar(x, y)
            # plt.show()

            # res11 = [lis[4] for lis in neighbors]
            # res13 = str(res11).strip('[]')
            # print(res13)
            list1 = []
            for i in os.listdir("C:/Users/olive/PycharmProjects/finalCrop1/WebApp/static"):
                list1.append(i)

            str1 = pred[0]
            str2 = ".jpg"
            str3 = str1 + str2

            for i in list1:
                if i in str3:
                     predimg = i

            str4 = pred[0]
            str5 = ".jpg"
            str6 = str4 + str5

            for i in list1:
                if i in str6:
                    predimg1 = i

            print('pred',pred)

            print("\nSuggested crop is:", pred[0])
            print("\nSuggested crop 2:", pred[1])

            list1 = []
            for i in os.listdir("C:/Users/olive/PycharmProjects/finalCrop1/WebApp/static/images"):
                list1.append(i)

            predimg = ''
            str1 = pred[0]
            str2 = ".jpg"
            str3 = str1 + str2

            for i in list1:
                if i in str3:
                    predimg = i

            predimg1 = ''
            str4 = pred[1]
            str5 = ".jpg"
            str6 = str4 + str5

            for i in list1:
                if i in str6:
                    predimg1 = i

            print(predimg)
            print(predimg1)
            full_filename1 = os.path.join(app.config['UPLOAD_FOLDER'], predimg)
            full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], predimg1)
        return render_template('resultpred.html', prediction=pred[0], prediction1=pred[1], image1=full_filename1, image2=full_filename2)




@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
