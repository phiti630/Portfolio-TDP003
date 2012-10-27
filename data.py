#-*- coding: utf-8 -*-
__package__= None
import json
from operator import itemgetter

def load(filename):
    """Loads JSON formatted project data from a file and returns a list.

load reads objects from a UTF-8 encoded JSON file, and returns a list of projects.

On errors, None is returned.

Parameters:

        filename (string) - The filename containing project data.

Returns: list
    All the project data from the read file, or None. """

    try:
        with open(filename) as data:
            return json.load(data)
    except:
        return None
    
def get_project_count(db):
    """Retrieves the number of projects in a project list.

Parameters:

        db (list) - A list as returned by load.

Returns: number
    The number of projects in the list. """

    count = 0
    for element in db:
        count += 1
    return count

def get_project(db, id):
    """Fetches the project with the specified id from the specified list.

If the specified project id does not exist, None is returned.

Parameters:

        db (list) - A list as returned by load.
        id (number) - The ID number of the wanted project.

Returns: dict
    All project data for the specified project, or None. """
    
    for element in db:
        if element['project_no'] == id:
            return element
    return None

def get_techniques(db):
    """Fetches a list of all the techniques from the specified project list.

Parameters:

        db (list) - A list as returned by load.

Returns: list
    An alphabetically sorted list containing the names of all techniques in db. """

    techniques = []
    for element in db:
        for technique in element['techniques_used']:
            if technique not in techniques:
                techniques.append(technique)
    
    return sorted(techniques)

def get_technique_stats(db):
    """Collects and returns statistics for all techniques in the specified project list.

The key of each entry in the returned dictionary is the technique name, and the value is a list of dictionaries for each of the projects using the technique.

Each of those dictionaries representing a project has the keys:

    id (int): Project number
    name (string): Name of the project

Parameters:

        db (list) - A list as returned by load.

Returns: dict
    Technique stats (see above). """
    
    techniques = {}
    for element in db:
        for technique in element['techniques_used']:
            if technique not in techniques:
                temp_dict = {technique: [{u'id': element['project_no'], 
                    u'name': element['project_name'], u'description': element['short_description']}]}
                techniques.update(temp_dict)
            else:
                temp_dict = {u'id': element['project_no'],
                        u'name': element['project_name'], u'description': element['short_description']}
                techniques[technique].append(temp_dict)
            techniques[technique] = sorted(techniques[technique], key=itemgetter('name'))

    return techniques

def search(db, sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None):
    """Fetches and sorts projects matching criteria from the specified list.

Parameters:

        db (list) - A list as returned by load.
        sort_by (string) - The name of the field to sort by.
        sort_order (string) - The order to sort in. 'asc' for ascending, 'desc' for descending.
        techniques (list) - List of techniques that projects must have to be returned. An empty list means this field is ignored
        search (string) - Free text search string.
        search_fields (list) - The fields to search for search in. If search_fields is empty, no results are returned. If search_fields is None, all fields are searched.

Returns: list
    A list containing dictionaries for all the projects conforming to the specified search criteria."""

    results = []
    for element in db:
        match = True
        #Searches the techniques-field if parameter techniques not equals None
        if techniques != None:
            for technique in techniques:
                if technique not in element['techniques_used']:
                    match = False
                    break
        
        #Free text search in the specified fields if parameter search not equals None
        if search != None:
            if search_fields != None:
                fieldsearch = False
                if len(search_fields) == 0:
                    break
                for field in search_fields:
                    try:
                        if search.decode('utf-8').upper() in element[field].upper():
                            fieldsearch = True
                            break
                    except:
                        if search.decode('utf-8') in str(element[field]):
                            fieldsearch = True
                            break                        
                if fieldsearch == False:
                    match = False
            else:
                fieldsearch = False
                for field in element:
                    try:
                        if search.decode('utf-8').upper() in element[field].upper():
                            fieldsearch = True
                            break
                    except:
                        if search.decode('utf-8') in str(element[field]):
                            fieldsearch = True
                            break
                if fieldsearch == False:
                    match = False

        if match == True:
            results.append(element)

    if sort_order == 'desc':
        return sorted(results, key=itemgetter(sort_by), reverse=True)

    if sort_order == 'asc':
        return sorted(results, key=itemgetter(sort_by), reverse=False)

    return None
