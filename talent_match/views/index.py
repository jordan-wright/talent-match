import logging

# Project 5 - Steve - added math imports for Haversine distance calculation
from math import radians, cos, sin, asin, sqrt

from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_required

# Project 5 - Steve - adding this directly so we can reuse it for the advanced search (manual, in-memory pagination.
from flask.ext.sqlalchemy import Pagination

# Project 5 - Steve - fixed imports based on model restructuring.
from ..models.talentInfo import Category, Skill
from ..models.userProfile import  ProviderSkill
from ..models.invitation import Invitation
# Project 5 - Steve adding use of ZipCode to latitude/longitude lookup.
from ..models.zipCode import USZipCodeToLatitudeLongitude

from ..forms import SearchForm, AdvancedSearchForm

from talent_match import db
from config import POSTS_PER_PAGE
from talent_match.models.userProfile import User, Provider

logger = logging.getLogger(__name__)

app = Blueprint('index', __name__, template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def index():
    if g.user.is_authenticated():
	    pending_invites = db.session.query(Invitation).filter(Invitation.receivingUserID == g.user.id, Invitation.accepted == None).count()
	    return render_template('index.html', invite_count=pending_invites)
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/<int:page>', methods = ['GET', 'POST'])
@login_required
def search(page = 1): #, setquery = ''):
    logger.info('hi steve')
    form = SearchForm(csrf_enabled=False)

    query = form.query.data or request.values.get('query')
    users = User.query.join(Provider).join(ProviderSkill).join(Skill).join(Category).filter(Skill.categoryID == Category.id, Category.deleted != True, Skill.deleted != True, Skill.name.like("%" + query + "%")).paginate(page, POSTS_PER_PAGE, False)

    ##
    ## Project 5 - Steve - Populating user feedback information.
    ##
    if (users and users.total > 0):
        for x in users.items:
            x.feedbackSummary = x.getFeedbackSummary()

    return render_template('search.html', query=query, users=users, gUser=g.user, mainUrl='/search')

##
## Project 5 - Steve - adding support for a more advanced search.
##
## This method collects information necessary for an advanced search then ships it along
## to the actual query/result implementation in the makeAdvancedSearch() function, below.
##
@app.route('/search/advanced', methods=['GET', 'POST'])
@login_required
def advancedSearchPrep():
    form = AdvancedSearchForm(csrf_enabled=False)

    if form.validate_on_submit():
        logger.info('Collected information for an advanced search; marshalling data to the query URL now')
        logging.info(form.data)

        # Decode the supplied search parameters.
        query = form.query.data

        originZip = form.originZip.data
        distanceFrom = form.distanceFrom.data
        volunteerOnly = form.volunteerOnly.data
        filterOutPastRejections = form.filterOutPastRejections._formfield
        sortByDistance = form.sortByDistance._formfield
        sortByProviderRating = form.sortByProviderRating._formfield

        # Assemble the query string to pass it into the real advanced search.
        # This is by-hand process today.
        # Note that, for our input set, we may not have to URL escape anything.  However, this is
        # something that may need to be added.
        queryString = '?query=' + query
        queryString += '&originZip=' + str(originZip)
        queryString += '&distanceFrom=' + str(distanceFrom)
        queryString += '&volunterOnly=' + str(volunteerOnly)
        queryString += '&filterOutPastRejections=' + str(False)  ## this may not be supported initially
        queryString += '&sortByDistance=' + str(sortByDistance)
        queryString += '&sortByProviderRating=' + str(sortByProviderRating)

        ## Now that we have collected the user advanced search parameters, redirect them to actually have the
        ## search performed:
        return redirect("/search/advanced/query" + queryString)
    else:
        logger.info('Gathering information for an advanced search.')
        logger.info(form)
        logger.info(form.data)
        return render_template('advanced_search2.html', search=None, users=None, gUser=g.user, form=form, advancedSearch=True)

##
## Project 5 - Steve - adding support for a more advanced search.
##
## This method uses information collected by  advancedSearchPrep(), above, to perform an advanced search.
## With time and technology restrictions, the advanced search is being performed in memory.
##
## Assistance on the Haversine algorithm in Python was obtained from:
##
##
@app.route('/search/advanced/query', methods=['GET', 'POST'])
@app.route('/search/advanced/query/<int:page>', methods = ['GET', 'POST'])
def makeAdvancedSearch(page = 1):
    query = request.values.get('query')
    originZip = request.values.get('originZip')
    if (originZip and len(originZip) > 0):
        originZip = int(originZip)
    else:
        originZip = '75252'     # Dallas
    distanceFrom = request.values.get('distanceFrom')
    if (distanceFrom and len(distanceFrom) > 0):
        distanceFrom = int(distanceFrom)
    else:
        distanceFrom = 300      # 300 mile default
    # All boolean values will default to False unless provided.
    volunteerOnly = request.values.get('volunteerOnly') == 'True'
    filterOutPastRejections = request.values.get('filterOutPastRejections') == 'True'
    sortByDistance = request.values.get('sortByDistance') == 'True'
    sortByProviderRating = request.values.get('sortByProviderRating') == 'True'

    queryString = '?query=' + query
    queryString += '&originZip=' + str(originZip)
    queryString += '&distanceFrom=' + str(distanceFrom)
    queryString += '&volunterOnly=' + str(volunteerOnly)
    queryString += '&filterOutPastRejections=' + str(filterOutPastRejections)  ## this may not be supported initially
    queryString += '&sortByDistance=' + str(sortByDistance)
    queryString += '&sortByProviderRating=' + str(sortByProviderRating)

    if (not query):
        query = 'HTML5'

    advancedSearchData =  dict(url='/search/advanced/query', queryString=queryString)

    users = None
    if (volunteerOnly) :
        # We can at least filter down to just volunteers via SQL
        users = User.query.join(Provider).join(ProviderSkill).join(Skill).join(Category).filter(Skill.categoryID == Category.id, Category.deleted != True, Skill.deleted != True, Skill.name.like("%" + query + "%"), ProviderSkill.will_volunteer==True).all()
    else:
        # Everything else is complex enough that we will calculate it manually.
        # We have to do most of this anyway in memory since SQLite does not easily support mathematical calculations.
        users = User.query.join(Provider).join(ProviderSkill).join(Skill).join(Category).filter(Skill.categoryID == Category.id, Category.deleted != True, Skill.deleted != True, Skill.name.like("%" + query + "%")).all()

    # Step 1: build the complete list.
    completeAndFilteredList = []
    if (users and users.total > 0):
        # Calculate feedback
        for x in users:
            # Construct the feedback information.
            x.feedbackSummary = x.getFeedbackSummary()

            # Calculate distance
            if (sortByDistance):
                usZipCodeOrigin = USZipCodeToLatitudeLongitude.query(zipCode=originZip).first()
                usZipCodeUserLocation = USZipCodeToLatitudeLongitude.query(zipCode=x.zipCode).first()
                if (usZipCodeOrigin) and (usZipCodeUserLocation):
                    x.distance = haversine(usZipCodeOrigin.latitude, usZipCodeOrigin.longitude,
                                         usZipCodeUserLocation.latitude, usZipCodeUserLocation.longitude)
                    if (x.distance) <= (distanceFrom * 1.15):   # including a fudge factor on the distance marker
                        completeAndFilteredList.append(x)

    # Step 2: sort the list.

    # Step 3: paginate the list.
    # Basically, we have to replace this:
    #   .paginate(page, POSTS_PER_PAGE, False)
    # since we are unable to perform the calculations directly in our database.


    return render_template('search.html', query=query, users=users, gUser=g.user, advancedSearchData=advancedSearchData)


## Assistance on the Haversine algorithm in Python was obtained from:
## http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # 6367 km is the radius of the Earth
    # km = 6371 * c
    mi = 3956 * c
    return mi
