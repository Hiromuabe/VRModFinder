from flask import Flask, render_template, request, redirect, url_for, session
import openai
from gpt import gpt_interior, gpt_feature, gpt_number,gpt_translate,gpt_translate_ja
from clip_code import *
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "GET":
        return render_template('index_ja.html')
    else:
        if "start" in request.form:
            return redirect(url_for("search"))
        else:
            global interior, features, number
            input_text = request.form["keyword"]
            input_text = gpt_translate(input_text)
            interior = gpt_interior(input_text)
            features = gpt_feature(input_text,interior)
            number = gpt_number(input_text,interior)
            ja_interior = gpt_translate_ja(",".join(interior))
            
            ja_features = gpt_translate_ja(",".join(features))
            return render_template('index_ja.html',interior=ja_interior,features=ja_features,number=number)

@app.route("/search",methods=['GET',"POST"])
def search():
    global interior, features, number
    if request.method == "GET":
        return render_template('search.html',interior=interior,features=features,number=number)
    else:
        names, urls, uids = squeeze(interior)
        selected_name, selected_uid = get_uid(interior, features, names,urls, uids)
        install_obj(selected_uid)
        return render_template('search.html',interior=interior,features=features,number=number,selected_name=selected_name,selected_uid=selected_uid)


    
if __name__ == "__main__":
    app.run(debug=True)