from flask import Flask, render_template, request, redirect, url_for, session
import openai
from gpt import gpt_interior, gpt_feature, gpt_number
from clip_code import *
from other_code import *
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        if "start" in request.form:
            return redirect(url_for("search"))
        else:
            global interior, features, number,device
            input_number = request.form["number"]
            device = request.form["device"]
            input_text = request.form["keyword"]
            interior = gpt_interior(input_text,input_number)
            features = gpt_feature(input_text,interior)
            number = gpt_number(input_text,interior)
            return render_template('index.html',interior=",".join(interior),features=",".join(features),number=number)

@app.route("/search",methods=['GET',"POST"])
def search():
    global interior, features, number,device
    if request.method == "GET":
        return render_template('search_en.html',interior=interior,features=features,number=number)
    else:
        names, urls, uids = squeeze(interior)
        selected_name, selected_uid = get_uid(interior, features, names,urls, uids,device)
        install_obj(selected_uid)
        names = save_img(selected_uid, "./data.json")
        return render_template('search_en.html',interior=interior,features=features,number=number,selected_name=selected_name,selected_uid=selected_uid,selected_names=names,selected_zip=zip(selected_uid,names))

if __name__ == "__main__":
    app.run(debug=True)