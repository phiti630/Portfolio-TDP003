# -*- coding: utf-8 -*-
from flask import Flask, request, url_for, render_template, redirect
import data
app = Flask(__name__)
app.debug = False

if not app.debug:
    import logging
    logging.basicConfig(filename='portfolio.log', format='%(levelname)s : %(message)s', level=logging.INFO)

db = data.load('data.json')

@app.route('/')
def start_page():
    """Simple start page containing not more than the global layout and a relatively welcoming text."""
    return render_template("layout.html", title = "Portfolio - start", text =u"Detta är startsidan för vår portfolio")

@app.route('/list', methods=['POST', 'GET'])
def projectlist():
    """The list page, showing a list of all the projects in the database."""
    #The following try/except, two if-clauses and assignment makes sure to sort the list based on the key given in the text field on the page.
    try:
        sort_key = request.args['key'].lower()
    except:
        sort_key = 'project_name'

    project_list = []

    if sort_key == "techniques":
        return redirect(url_for('technique_list'))
    
    if sort_key not in db[0].keys():
        sort_key = 'project_name'

    sorted_db = sorted(db, key=lambda k: k[sort_key])
    #Loop through the sorted database and create a simplified list with only the data necessary for this page
    for project in sorted_db:
        project_list.append({'id': project['project_no'], 'name': project['project_name'], 'description':project['short_description']})

    return render_template("list.html", title="Portfolio - projektlista", projects = project_list)


@app.route('/results', methods=['GET'])
def search_results():
    """Both the result page for searches and the page for advanced searches. The global quicksearch-form leads here with a simple search performed. The "Avancerad sökning"-link also leads here (with an empty search resulting in a list of all projects performed)"""
    available_fields = []
    available_techniques = data.get_techniques(db)
    args = {}
    #Get all keys from the first project in db, so the page can list all available fields.
    for key in db[0].keys():
        available_fields.append(key)

    for argument in ['sort_by', 'sort_order', 'search']:
        try:
            val = request.args[argument].encode('utf-8')
        except:
            if argument == 'sort_by':
                val = 'start_date'
            elif argument == 'sort_order':
                val = 'desc'
            else:
                val = None
        args.update({argument: val})
    #The for-loops above and below this comment parses all search arguments from the url and saves them to the args-dict.
    for argument in ['techniques', 'search_fields']:
        try:
            val = request.args.getlist(argument)
        except:
            val = None
        if val == [] and argument == 'search_fields':
            val = None
        args.update({argument: val})
    #Makes a search with the given parameters and saves the resulting list to results
    results = data.search(db, args['sort_by'], args['sort_order'], args['techniques'], args['search'], args['search_fields'])
    
    return render_template("search.html", title = u"Portfolio - sökning", projects = results, fields=available_fields, techniques=available_techniques)

@app.route('/techniques')
def technique_list():
    """The page listing projects based on techniques. Gets technique-info from the db with get_technique_stats() and sends it to the page for listing."""
    tech_list = data.get_technique_stats(db)
    return render_template('techniques.html', title = u'Portfolio - Tekniker', techniques = tech_list)



@app.route('/project/<project_id>')
def view_project(project_id):
    """The page for specific projects. Shows the project with the ID given in the URL, renders an error page if the ID is invalid."""
    project = None
    try:
        project =  data.get_project(db, int(project_id))
    except:
        pass

    if project == None:
        return render_template("invalid_id.html")
    return render_template("project.html", title = project['project_name'], project = project)


if __name__ == "__main__":
    app.run()
