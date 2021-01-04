# techdegree-project-5
 Build a Personal Learning Journal with Flask

Reviewer Notes:

I am going for an Exceeds Expectations grade.
Pre-existing username is "user1" with a password of "password".


Project Overview
Create an interface for a learning journal web application. The main
(index) page lists journal entry titles and dates. Each journal entry
title links to a detail page that displays the title, date, time spent,
the journal entry, and resources related to the learning.

The application lets the user add or edit journal entries. When adding
or editing a journal entry, the application prompts the user for title,
date, time spent, what they learned, and resources to remember. The
results for these entries are stored in a database and displayed in a
blog style website. The HTML/CSS for this site has been supplied for
you.


Project Instructions
To complete this project, follow the instructions below. If you get
stuck, ask a question on Slack or in the Treehouse Community.

 10 steps
Peewee Model and Database Connection
Create a model class for adding and editing journal entries. Connect
to the database.

NOTE: When run, the database should already contain at least one
journal entry.

Routes for the Application
Create each of the following routes for your application

/ - Known as the root page, homepage, landing page but will act as
the Listing route.

/entries - Also will act as the Listing route just like /

/entries/new - The Create route

/entries/<id> - The Detail route

/entries/<id>/edit - The Edit or Update route

/entries/<id>/delete - Delete route

NOTE: Each route is of course prefixed with the running server address

Example: The route /entries would be mapped to: http://<address>:<port>/entries

Create the Listing route/view
Route: / and /entries

This view should render a listing page of all of the journal entries, where each
entry displays the following fields:

Title - should be a linked title, clicking it routes user to the detail page for
the clicked entry.
Date - Each entry should have a date created listed somewhere beneath the title.
Create the Detail route/view
Route: /entries/<id>

This view should render a detail page of a journal entry, it should display the
following fields on the page:

Title
Date
Time Spent
What You Learned
Resources to Remember.
NOTE: This page should contain a link/button that takes the user to the Edit
route for the Entry with this <id>.

Create the Add route/view
Create an add view with the route /entries/new that allows the user to add a
journal entry with the following fields:

Title - string
Date - date
Time Spent - integer
What You Learned - text
Resources to Remember - text
The page should present a new blank Entry form that allows the user to Create
a new entry that will be stored in the database.

Create the Edit route/view
Route: /entries/<id>/edit

Create an edit view with the route /entries/<id>/edit that allows the user to
edit the journal entry with an id of the <id> passed in:

Title
Date
Time Spent
What You Learned
Resources to Remember
Ideally, you should prepopulate each form field with the existing data on
load. So the form is filled out with the existing data so the User can
easily see what the value is and make edits to the form to make the
update.

NOTE: Updating an Entry should not result in a new Entry being created,
this behavior would not be seen as editing this would be adding a new
entry. To check this, you can simply make an edit and then reload the
listing page to see if a duplicate record was created.

Create the Delete route
Create a delete route to delete the journal post from the database. WHen the
delete button is clicked by the user, the post will be removed from the
database and they will be redirected to the homepage.

Use the supplied HTML/CSS
Use the supplied HTML/CSS to build and style your pages. Use CSS to style
headings, font colors, journal entry container colors, body colors.

You will want to create two folders in your project root for these files:

Create a templates which will hold your HTML template files to be used for
rendering pages.

Create a static folder which should hold your .css files that you can
reference from your HTML templates to style your pages.

Python Coding Style
Coding style or PEP 8 are guidelines for writing clean, readable code, to
keep yourself in the best practices of writing Python you should get into
a strong habit of checking out the most common PEP guidelines for writing
Python code so your code looks similar as professionals in the industry.

Make sure your code complies with the most common PEP 8 Guidelines

Review the following sections of the link above:

Code Layout
Indentation
Tabs or Spaces?
Maximum Line Length
Blank Lines
Imports
Include dependencies file
Anytime you have a project that you build that required you to pip install
<some package> so that you could use that package as an import into your
own project, such as pip install Flask or pip install flask-wtf these
become what are known as dependencies. These dependencies are required
to be able to run your project because of this you will always need to
ensure you provide a dependencies file in the root of your project folder.

A common convention is to have one of the following files, but NOT both:

Pipfile -- used commonly with Pipenv
requirements.txt -- used commonly with Virtualenv
Either is acceptable to use and depend on which method you use to install
your third-party packages into your Python virtual environment.

You can generate a requirements.txt file with command listed below, but
first, you will want to ensure that you are inside an activated python
virtual environment. Check out the Additional Resources for a related
video about Virtual Environments.

Command to generate dependencies file:

pip freeze > requirements.txt

NOTE: Ensure you are inside an activated Python Virtual Environment.

Extra Credit
To get an "exceeds" rating, complete all of the steps below:

 4 steps
Entry model tags
Allow your Entry to store tags

You can accomplish this with a few different approaches:

You can store a string field on the Entry model itself, though you will
have to process each tag when trying to save an entry with tags or find
an entry that contains the tag being searched for.

You can create your own Tag model and create a relationship field back
to an Entry so that: "Many" Tags can belong to "One" Entry also known
as a Many-to-One relationship or a ForeignKey.

Show Entry tags on listing page
Somewhere beneath each Entry being listed display the associated tags
for each Entry, they should be clickable (linked) so that clicking on
a tag takes you to a listing page of all the Entries who have the
same tag.

Show Entry tags on the detail page
On the detail page of an Entry, display the tags as clickable links
so that clicking on a tag takes you to a listing page of all the
Entries who have the same tag.

Protect routes (provide credentials for code review)
Protect these routes with authentication a User should only be able
to: Create, edit, and delete an entry if they are logged in.

/entries/new

/entries/<id>/edit

/entries/<id>/delete

NOTE: Something to keep in mind, in a scenario where you want your
app to support more than 1 user entering journal entries, you
would likely want to protect the entries from even being
modified unless that user is the creator of the entry.