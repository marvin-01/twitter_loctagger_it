# twitter_loctagger_it
 This package allows you to map Italian Twitter users to a specific city or region in Italy.
 
 ## About
 This package is specifically intended to detect, extract, and geocode locations from the 'location' field, which is part of a user's profile. For example, if a user wrote "vivo a Sesto Calende", the algorithm would map this user to ***"Sesto Calende, Varese, VA,  Lombardia, Italia"***. Note that the 'location' field can be obtained by using the Twitter API as part of the user information.

## Installation
```
pip install twitter_loctagger_it
```

## How to use
1. Import the package as follows:
```python
from twitter_loctagger_it import geocode
```
2. The package requires as input a Python Series (this can also be a Pandas column) and returns a Pandas DataFrame with the original column along with the geocoded results.
```python
Location = geocoder.tag_location(df_input['location_original'])
df_output = Location()
df_output['id']=df_input['id']
```
For example, if we want to apply this to the following list of users (*df_input*)

| id        | location_original          |
|-----------|----------------------------|
|244950970  |Recanati,italy              |
|17774175	  |ancona,Italia               |
|91842195	  |Nel Paese dei Balocchi      |
|244754469  |monsampolo del tronto,marche|

The result (*df_output*) would be

| id        | location_original          |city                  |	province   	| province_code |	region      	| state |
|-----------|----------------------------|----------------------|-------------|---------------|--------------|-------|
|244950970  |Recanati,italy              |Recanati              |Macerata     | MC            |Marche        |Italia |
|17774175	  |fidenza                     |Fidenza               |Parma        |PR             |Emilia-Romagna|Italia |
|91842195	  |Nel Paese dei Balocchi      |                      |             |               |              |       |
|244754469  |monsampolo del tronto       |Monsampolo del Tronto |Ascoli Piceno|AP             |Marche        |Italia |
