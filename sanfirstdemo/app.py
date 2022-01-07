from flask import Flask,render_template,request
import os
import pandas as pd
# from ex.some import multiword_tokenize
#from pyrebase import pyrebase
from firebase import Firebase
import nltk
nltk.download('punkt')
import csv
import glob
import zipfile
from os.path import basename
from flask import jsonify 
app = Flask(__name__,template_folder='Templates')
app.static_url_path = app.config.get('STATIC_FOLDER')
from nltk import word_tokenize
from nltk.tokenize import MWETokenizer
from simplet5 import SimpleT5
# set the absolute path to the static folder
app.static_folder = app.root_path + app.static_url_path


#app.config["UPLOAD_PATH"] = "E:/"
a = pd.read_csv('Updated Standard streets (2).csv')
a['Unnamed: 0']=a['Unnamed: 0'].str.lower()
a['Unnamed: 1']=a['Unnamed: 1'].str.lower()
dict(zip(a['Unnamed: 0'], a['Unnamed: 1']))
dict1 = a.set_index('Unnamed: 0').to_dict()['Unnamed: 1']

def multiword_tokenize(text, mwe):
    # Initialize the MWETokenizer
    print(mwe)
    protected_tuples = [word_tokenize(word) for word in mwe]
    protected_tuples_underscore = ['_'.join(word) for word in protected_tuples]
    tokenizer = MWETokenizer(protected_tuples)
    # Tokenize the text.
    tokenized_text = tokenizer.tokenize(word_tokenize(text))
    # Replace the underscored protected words with the original MWE
    for i, token in enumerate(tokenized_text):
        if token in protected_tuples_underscore:
            tokenized_text[i] = mwe[protected_tuples_underscore.index(token)]
    return tokenized_text

config={
  "apiKey": "AIzaSyD2Kc5Vu_ZvRq0wqffWfo7Y8QytJNTdnFA",
  "authDomain": "address-normalization-1979b.firebaseapp.com",
  "projectId": "address-normalization-1979b",
  "storageBucket": "address-normalization-1979b.appspot.com",
  "messagingSenderId": "58619810635",
  "appId": "1:58619810635:web:5265955af2a30fcf470ece",
  "measurementId": "${config.measurementId}",
  "databaseURL":""

}
#firebase=pyrebase.initialize_app(config)
firebase = Firebase(config)
sotrage=firebase.storage()
# sotrage.child('files/').put(st)
model = SimpleT5()
model.from_pretrained(model_type="t5",model_name="t5-base")
model.load_model('t5','gs://address-normalization-1979b.appspot.com/static/simplet5-epoch-0-train-loss-0.0439',use_gpu=False)


@app.route("/upload_file",methods=["GET","POST"])
def upload_file():
    if request.method == 'POST':
        fi=[]
        for f in request.files.getlist('file_name'):
        #f=request.files['file_name']
            #f.save(os.path.join(app.config['UPLOAD_PATH'],f.filename))
                print(app.static_folder,)
            # f.save('static')
            # print(f.filename,"filename")
            # sotrage.child('files/'+f.filename)
            # sotrage.child(f.filename).put(f)
            # print(sotrage.child('files/'+f.filename).get_url(cc.))
                mwe = ['new york','new hampshire','new jersey','new mexico','north carolina','north dakota','south carolina','south dakota','rhode island','west virginia','post office box']

                folpath = 'static/'
                s = []

            # for fpath in glob.glob("{0}/*".format(folpath),recursive=True):
                
                #print(fpath)
                # s.append(fpath)
            # print(s,"dggfdgd")
            # for i in s:
                #print(i)
                # hj= i.split("/")[1]
                #print(hj)
                hj1 = f.filename.split(".")[0]
                #print(hj1)
                
                if f.filename[-3:] == "csv":
                    dg = []
                    data = pd.read_csv(f,index_col=None)
                    #print(data.head())
                    data = data.rename(columns={data.columns[0]: 'Standard Streets'})
                    conv1 = data['Standard Streets'].tolist()
                    c = []

                    for i in conv1:
            
                        abc = model.predict(i)
                        abc1 = str(abc)[1:-1]
                        a = abc1.lower()
                        a = multiword_tokenize(a, mwe)

                        for i in a:

                            for k,v in dict1.items():
                                if k == i:
                                    y=a.index(i)
                                    a[y]=v
                        #print(a)

                        finalresult = "" 

                        for elements in a: 
                            finalresult += str(elements) + " " 

                        finalresult = finalresult.title()
                        #print(result)



                        #c.append(finalresult)
                        dg.append(finalresult)
                    df = pd.DataFrame(dg)
                    #print(df,"ddfff")
                    df.to_csv(f.filename+"_finalresult.csv",index=False,header=False)
                    fi.append(f.filename+'_finalresult.csv')
                    # sotrage.child(f.filename).put()
                        
                    #print((dg))
                        #dg.append(finalresult)

                    #print(data['Standard Streets'])
                    #data1 = (data.head())
                    #print(data1)
                    
                elif f.filename[-4:]=="json":
                    cg = []
                    data = pd.read_json(f)
                    #print(data)
                    
                    data = data.rename(columns={data.columns[0]: 'Standard Streets'})
                    conv1 = data['Standard Streets'].tolist()
                    c= []
                    for i in conv1:
                        
            
                        abc = model.predict(i)
                        abc1 = str(abc)[1:-1]
                        a = abc1.lower()
                        a = multiword_tokenize(a, mwe)

                        for i in a:

                            for k,v in dict1.items():
                                if k == i:
                                    y=a.index(i)
                                    a[y]=v
                        #print(a)

                        finalresult = "" 

                        for elements in a: 
                            finalresult += str(elements) + " " 

                        finalresult = finalresult.title()
                        #print(result)

                    
                        cg.append(finalresult)
                    df = pd.DataFrame(cg)
                    
                    df.to_json(f.filename+"_finalresultjson.json",orient='records',lines=True)
                    fi.append(f.filename+"_finalresultjson.json")
                      
                    #print((cg))
                        

                    #print(data.head())
                elif f.filename[-3:] == "xml":
                    eg = []
                    data = pd.read_xml(f)
                    data = data.rename(columns={data.columns[0]: 'Standard Streets'})
                    conv1 = data['Standard Streets'].tolist()
                    c = []
                    
                    for i in conv1:
                        abc = model.predict(i)
                        abc1 = str(abc)[1:-1]
                        a = abc1.lower()
                        a = multiword_tokenize(a, mwe)

                        for i in a:

                            for k,v in dict1.items():
                                if k == i:
                                    y=a.index(i)
                                    a[y]=v
                        #print(a)

                        finalresult = "" 

                        for elements in a: 
                            finalresult += str(elements) + " " 

                        finalresult = finalresult.title()
                        #print(result)

                        #print(i)
                        


                        eg.append(finalresult)
                    df = pd.DataFrame(eg,columns=['x'])
                    
                    
                    df.to_xml(f.filename+"_finalresultxml.xml")
                    fi.append(f.filename+"_finalresultxml.xml")

                folspath = 'static/'
                sss=  []

                for fspath in glob.glob("{0}/*".format(folspath),recursive=True):
    
                    print(fspath,'hai')
                    sss.append(fspath)
                print(sss,'haiiii')

                with zipfile.ZipFile('rr.zip', 'w') as zipF:
                    for file in fi:
                        zipF.write(file,compress_type=zipfile.ZIP_DEFLATED)
                print(zipF,'hai')
                sotrage.child('files.zip').put('rr.zip')
                ll=sotrage.child('files.zip').get_url('')
                
                

                        
                    #print((eg))



    # write the header
    # writer.writerow(header)

    # write multiple rows
                #writer.writerow(finalresult)
        
        # print(sotrage.child('zip').get_url())
        return render_template("upload-files.html",msg="Files has been uploaded sucessfully",ll=ll)
    return render_template("upload-files.html",msg="Please Choose a files")
    #return jsonify({"msg":"Files has been uploaded sucessfully","ll":'static/final.zip'})



if __name__== '__main__':
    app.run(debug=True)


# apiKey: "AIzaSyD1R6J8eAFBZ59vmqC2HKsKJJoX_OaexJ4",
#   authDomain: "filestorage-2ff36.firebaseapp.com",
#   projectId: "filestorage-2ff36",
#   storageBucket: "filestorage-2ff36.appspot.com",
#   messagingSenderId: "593499132447",
#   appId: "1:593499132447:web:3e3bffab7d1ced08d57b2a",
#   measurementId: "${config.measurementId}"



app.route("/downloadfile/<path:filename>", methods = ['GET'])
def download_file(filename):
    print(filename)
    return render_template('files.html',value=filename)

if __name__== '__main__':
    app.run(debug=True)

