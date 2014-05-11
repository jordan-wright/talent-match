import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_required

from ..models.talentInfo import Category, Skill
from ..models.userProfile import  ProviderSkill
from ..models.invitation import Invitation

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

# Project 5 - Steve - adding support for a more advanced search; reusing existing search result template if possible.
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

    users = User.query.join(Provider).join(ProviderSkill).join(Skill).join(Category).filter(Skill.categoryID == Category.id, Category.deleted != True, Skill.deleted != True, Skill.name.like("%" + query + "%")).paginate(page, POSTS_PER_PAGE, False)
    return render_template('search.html', query=query, users=users, gUser=g.user, advancedSearchData=advancedSearchData)

