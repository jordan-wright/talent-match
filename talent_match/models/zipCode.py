from talent_match import db
from modelUtils import modelToString

__author__ = 'Steve'

##
# Added for Project 4 - adding a table to store the lookup from US ZIP code to a latitude and longitude.
# This lookup is used as part of the calculation to determine distance for an activity.
##
# Note:
# - ZIP Code data was obtained from http://download.geonames.org/export.  The filed numbering has been reordered
# for convenience.
# - The data files are included in the "talent_match/data" directory.
# - We are limited to US ZIP codes for this project.
##
# Conversion command to build zipCodeData.txt -
# gawk -F "\t" '{ printf("%s\t%s\t%s\t%s\t%s\n",$2,$10,$11,$3,$5); }' US.txt > zipCodeData.txt
##


class USZipCodeToLatitudeLongitude(db.Model):
    __tablename__ = 'us_zipcode_to_latitude_longitude'
    id = db.Column(
        db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    # Note: one ZIP code may map to multiple locations (cities)
    # We will only use the first one.  This is approximate enough for our
    # needs.
    zipCode = db.Column(db.INTEGER, nullable=False, index=True)

    # SQLite does not natively support the Numeric type.
    # Instead we may use an integer-based approach with a fixed precision.
    #latitude = db.Column(db.NUMERIC, nullable=False)
    #longitude = db.Column(db.NUMERIC, nullable=False)
    latitudeTimes1000 = db.Column(db.INTEGER, nullable=False)
    longitudeTimes1000 = db.Column(db.INTEGER, nullable=False)

    # Alternatively, we can store the latitude/longitude values as floats.
    latitude = db.Column(db.FLOAT, nullable=False)
    longitude = db.Column(db.FLOAT, nullable=False)

    # Location (city) and state abbreviation are being included for internal
    # testing and debugging.
    stateAbbreviation = db.Column(db.String(10), nullable=True)
    locationName = db.Column(db.String(120), nullable=True)

    def __init__(self):
        pass

    def __repr__(self):
        return modelToString(self)
