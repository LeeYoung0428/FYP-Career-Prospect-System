from flask import Flask, render_template, request, flash, send_file
from flask_mysqldb import MySQL
from flask_paginate import Pagination
from main import match_job
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
import io
from mysql_manager import MySQLManager
from scibert import SciBERT

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'publications_db'
app.config['MYSQL_PORT'] = 3307
app.config['SECRET_KEY'] = 'something only you know'

isMatched = False
global_id = "id"
result = "result"
mysql = MySQL()
mysql.init_app(app)
scibert = SciBERT()
plt.rcParams.update({'figure.max_open_warning': 0})


def prepare_result(query):
    mysql_m = MySQLManager()
    df_combined = match_job(query, scibert)
    meanimage_list = []
    varimage_list = []
    for index in df_combined.index:
        meanimage_list.append('image_base64("img_bytes"): ' + str(index))
        varimage_list.append('image_base64("img_bytes"): ' + str(index))
    global result
    result = save_result(df_combined.copy(), meanimage_list, varimage_list)
    mysql_m.delete_candidate()
    for i in result.index:
        record = {}
        record["photo"] = result["Photo"][i]
        record["author"] = result["Candidate"][i]
        record["university"] = result["university"][i]
        record["doc_count"] = str(result["Docs"][i])
        record["avg_sim"] = str(result["AVG_SIM"][i])
        record["mean"] = str(result["Average_Similarity"][i])
        record["meanimage"] = result["Image(Avg)"][i]
        record["var"] = str(result["Variance"][i])
        record["varimage"] = result["Image(Var)"][i]
        record["related_count"] = str(result["Related"][i])
        mysql_m.insert_candidate(record)
    print("Candidate data inserted", flush=True)
    return True


def save_result(df, mean_image_list, var_image_list):
    mean_list = []
    var_list = []
    docs_list = []
    avg_mean_list = []
    related_list = []
    for i in df.index:
        mean_tuple = (df["mean_2018"][i], df["mean_2019"][i], df["mean_2020"][i], df["mean_2021"][i])
        avg_mean = sum(mean_tuple) / len(mean_tuple)
        avg_mean_list.append(avg_mean) 
        mean_list.append(mean_tuple) 
        var_list.append((df["var_2018"][i], df["var_2019"][i], df["var_2020"][i], df["var_2021"][i]))
        docs_list.append(sum((df["docs_2018"][i], df["docs_2019"][i], df["docs_2020"][i], df["docs_2021"][i])))
        related_list.append(sum((df["r_2018"][i], df["r_2020"][i], df["r_2021"][i])))
    df.drop(["mean_2018", "mean_2019", "mean_2020", "mean_2021"], axis=1, inplace=True)
    df.drop(["var_2018", "var_2019", "var_2020", "var_2021"], axis=1, inplace=True)
    df.drop(["docs_2018", "docs_2019", "docs_2020", "docs_2021"], axis=1, inplace=True)
    df.drop(["r_2018", "r_2020", "r_2021"], axis=1, inplace=True)
    df.rename(columns={'photo': 'Photo'}, inplace=True)
    df.rename(columns={'author': 'Candidate'}, inplace=True)
    df["Average_Similarity"] = mean_list
    df["Image(Avg)"] = mean_image_list
    df["Variance"] = var_list
    df["Image(Var)"] = var_image_list
    df["Docs"] = docs_list
    df["Related"] = related_list 
    df["AVG_SIM"] = avg_mean_list
    return df


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/<author>/<heights>/visualize')
def visualize(author, heights):
    heights_list = str(heights)[1:-1].split(',')
    for i in range(4):
        heights_list[i] = float(heights_list[i])
    labels = ['2018', '2019', '2020', '2021']  # this is the years
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    sns.set_style(style="whitegrid")
    ax.plot(labels, heights_list)
    ax.set_title(author.title(), fontsize=16, weight="bold")
    FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='img/png')

#search job and company
@app.route('/job', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        terms = request.args.get('term')
        term = terms.split()
        print(term)
        conn = mysql.connection
        cursor = conn.cursor()

        if terms == 'all' or len(terms) == 0:
            cursor.execute("SELECT ID, NAME, COMPANY, DESCRIPTION from job")
            conn.commit()
            data = cursor.fetchall()
            # cursor.close()
            return render_template("job.html", data=data, terms=terms)

        for r in range(len(term)):
            cursor.execute(
                "SELECT ID, NAME, COMPANY, DESCRIPTION from job WHERE CATEGORY LIKE %s OR NAME LIKE %s OR DESCRIPTION LIKE %s",
                (("%" + term[r] + "%",), ("%" + term[r] + "%",), ("%" + term[r] + "%",)))
            conn.commit()
            data1 = cursor.fetchall()
            data = data1 + data1

        if len(data) == 0:
            flash('No related job found. Please try again.')
            return render_template("job.html", terms=terms)
    return render_template("job.html", data=data, terms=terms)


@app.route('/job/match/<id>/show-in-pagination', methods=['POST', 'GET'])
def show(id):
    entries = 1
    limit = 1
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT NAME from job WHERE ID = %s", [id])
    conn.commit()
    jobnamea = cursor.fetchall()
    jobnamea = jobnamea[0]
    jobnamej = ''.join([str(x) for t in jobnamea for x in t])
    jobname = jobnamej

    cursor.execute("SELECT LINK from job WHERE ID = %s", [id])
    conn.commit()
    joblinka = cursor.fetchall()
    joblinka = joblinka[0]
    joblinkj = ''.join([str(x) for t in joblinka for x in t])
    joblink = joblinkj

    cursor.execute("SELECT DESCRIPTION from job WHERE ID = %s", [id])
    conn.commit()
    description = cursor.fetchall()
    description = description[0]
    descriptionj = ''.join([str(x) for t in description for x in t])
    de = descriptionj
    
    global global_id
    global isMatched
    if (not isMatched) or global_id != id:
        isMatched = prepare_result(de)
    if isMatched:
        global_id = id
    #######################################################################    
    cursor.execute("SELECT CANDIDATE from candidate")
    conn.commit()
    user = cursor.fetchall()

    cursor.execute("SELECT AVERAGE_SIMILARITY from candidate")
    conn.commit()
    avg_sim = cursor.fetchall()

    cursor.execute("SELECT VARIANCE from candidate")
    conn.commit()
    variance = cursor.fetchall()

    #######################################################################
    if request.method == "POST":
        query = request.form['query']
        if query != "":
            isMatched = prepare_result(query)
        if isMatched:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM candidate WHERE  Avg_sim > 0.2")
            conn.commit()
            total = cursor.fetchall()
            total_count = total[0][0]
            message = ""
            if total_count <= 0:
                message = "All author’s average similarity lower than 0.2"

            page = request.args.get('page', 1, type=int)
            offset = page * limit - limit
            cursor.execute("SELECT * from candidate WHERE Avg_sim > 0.2 LIMIT %s OFFSET %s", (limit, offset))
            conn.commit()
            dataa = cursor.fetchall()
            #######################################################################
            pagination = Pagination(page=page, per_page=limit, offset=offset, total=total_count, record_name='user',
                                    css_framework='bootstrap3')
            return render_template("try.html", entries=entries, jobname=jobname, joblink=joblink, user=user, id=id,
                                   dataa=dataa, pagination=pagination, message=message)

    if request.method == 'GET':

        entries = request.args.get('entries')
        conn = mysql.connection
        cursor = conn.cursor()

        if entries == '5':
            limit = 5

        if entries == '10':
            limit = 10

        if entries == '25':
            limit = 25

        if entries == '50':
            limit = 50

        if entries == 'all':
            limit = 323

        cursor.execute("SELECT COUNT(*) FROM candidate WHERE  Avg_sim > 0.2")
        conn.commit()
        total = cursor.fetchall()
        total_count = total[0][0]
        message = ""
        if total_count <= 0:
            message = "All author’s average similarity lower than 0.2"

        page = request.args.get('page', 1, type=int)
        offset = page * limit - limit
        #####################################################################
        cursor.execute("SELECT * from candidate WHERE Avg_sim > 0.2 LIMIT %s OFFSET %s ", (limit, offset))
        conn.commit()
        dataa = cursor.fetchall()

        #######################################################################
        pagination = Pagination(page=page, per_page=limit, offset=offset, total=total_count, record_name='user',
                                css_framework='bootstrap3')
        return render_template("try.html", entries=entries, jobname=jobname, joblink=joblink, user=user, id=id,
                               dataa=dataa, pagination=pagination, message=message)


@app.route('/expert', methods=['POST', 'GET'])
def show1():
    entries = 1000
    limit = 1000
    ts = 0.7
    conn = mysql.connection
    cursor = conn.cursor()
    
    if request.method == "POST":
        query = request.form['query']
        if query != "":
            isMatched = prepare_result(query)
        if isMatched:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM candidate WHERE  Avg_sim > 0.2")
            conn.commit()
            total = cursor.fetchall()
            total_count = total[0][0]
            message = ""
            if total_count <= 0:
                message = "All author’s average similarity lower than 0.2"

            page = request.args.get('page', 1, type=int)
            offset = page * limit - limit
            cursor.execute("SELECT * from candidate WHERE Avg_sim > 0.2 LIMIT %s OFFSET %s", (limit, offset))
            conn.commit()
            dataa = cursor.fetchall()
            #######################################################################
            pagination = Pagination(page=page, per_page=limit, offset=offset, total=total_count, record_name='user',
                                    css_framework='bootstrap3')
            return render_template("searchpage.html", entries=entries, id=id, ts=ts,
                                   dataa=dataa, pagination=pagination, message=message)

    if request.method == 'GET':
        message = ""
        
        cursor.execute("SELECT COUNT(*) FROM candidate WHERE  Avg_sim > 0.2")
        conn.commit()
        total = cursor.fetchall()
        total_count = total[0][0]
        message = ""
        if total_count <= 0:
            message = "All author’s average similarity lower than 0.2"
        
        page = request.args.get('page', 1, type=int)
        offset = page * limit - limit
        #####################################################################
        cursor.execute("SELECT * from candidate WHERE Avg_sim > 0.2 LIMIT %s OFFSET %s ", (limit, offset))
        conn.commit()
        dataa = cursor.fetchall()

        #######################################################################
        pagination = Pagination(page=page, per_page=limit, offset=offset, total=total_count, record_name='user',
                                css_framework='bootstrap3')
        return render_template("searchpage.html", entries=entries, id=id, ts=ts,
                               dataa=dataa, pagination=pagination, message=message)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)
