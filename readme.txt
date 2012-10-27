=== Portfolio - TDP003 ===
Authors: Alexander Kazen and Philip Tingberg
Current URL: localhost


=== Description ===

This is a simple portfolio-system for viewing and searching for projects in a
given database. The system is tailored for text-based browsers such as lynx.


=== Startup ===

To start the system, make sure python and flask is installed and simply run "server.py"
with python2. The server will start on port 5000 and will be accessible at
127.0.0.1:5000.


=== Usage ===

Going to the start page will present you with a simple page with a few
choices. All pages in the system will have a global layout containing a simple
menu in the top and a quicksearch-form in the bottom. 

The different links in the menu are:

    -- "Start" --
Will, as the name implies, take you to the front page of the system.

    -- "Lista" --
This page shows a list of all the projects in the database as well as a text
field where you can choose what to sort the list by. Valid options to sort by
is the keys to the different fields in the project database, as described
further on in the section about the database. All projects in the list are
links to their respective project pages.

    -- "Tekniker" --
This page will show a list of all techniques found in the database, with
sublists for all techniques with all projects using that technique. All
projects in the list are links to their respective project pages.
    

    -- "Avancerad sökning" --
Making a search in the quicksearch-section will lead to the same page as the 
"Avancerad sökning"-link in the menu. This page contains a text field and a 
few sets of checkboxes and radio buttons for more specific searches. Below 
this is a list of all serch results for the current search. All projects in
the list are links to their respective project pages.

=== The database ===

All projects in the system are saved to a file called "data.json". The syntax
of the file is that of a list of dictionaries in python. Adding projects to
the system must be done manually to this file. A project should contain the
same keys as the following example:

  {
    "start_date": "2009-09-05",
    "short_description": "no",
    "course_name": "OK\u00c4NT",
    "long_description": "no no no",
    "group_size": 2,
    "academic_credits": "WUT?",
    "lulz_had": "many",
    "external_link": "YY",
    "small_image": "X",
    "techniques_used": [
      "python"
    ],
    "project_name": "python data-module test script",
    "course_id": "TDP003",
    "end_date": "2009-09-06",
    "project_no": 1,
    "big_image": "XXX"
 } 


=== Logging ===
All requests made to the server will be logged to the file portfolio.log. 
    
