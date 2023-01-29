# twitter_loctagger_it
 This package allows you to map Italian Twitter users to a specific city or region in Italy.
 
 ## About
 This package is specifically intended to detect, extract, and geocode locations from the *"location"* field, which is part of a user's profile. For example, if a user wrote *"vivo a Sesto Calende"*, the algorithm would map this user to ***"Sesto Calende, Varese, VA,  Lombardia, Italia"***. Note that the *"location"* field can be obtained by using the Twitter API as part of the user information.

## Installation
```
pip install twitter_loctagger_it
```

## How to use
1. Import the package as follows:
```python
from twitter_loctagger_it import geocode
```
2. Run the following command:
```python
df_output = geocoder.tag_location(df_input)()
```
Note: the package requires as input a Pandas Series (with the Twitter ID as the index) and returns a Pandas DataFrame with the geocoded results.

## Example
As I mentioned above, this package requires as input a Series object (`df_input`) which looks like this

| id        | location_original          |
|-----------|----------------------------|
|244950970  |Recanati,italy              |
|17774175	  |ancona,Italia               |
|91842195	  |Nel Paese dei Balocchi      |
|244754469  |monsampolo del tronto,marche|

where the column *location_original* contains the self-reported location for each users, while the index is the list of the corresponding user ids.

Then, by running the command above, the result (`df_output`) would be

| id        | location_original          |city                  |	province   	| province_code |	region      	| geographic_ripartition | state |
|-----------|----------------------------|----------------------|-------------|---------------|--------------|------------------------|-------|
|244950970  |Recanati,italy              |Recanati              |Macerata     | MC            |Marche        |         Centro         |Italia |                
|17774175	  |fidenza                     |Fidenza               |Parma        |PR             |Emilia-Romagna|         Nord-Est       |Italia |
|91842195	  |Nel Paese dei Balocchi      |                      |             |               |              |                        |       |
|244754469  |monsampolo del tronto       |Monsampolo del Tronto |Ascoli Piceno|AP             |Marche        |         Centro         |Italia |

## Caveats
The main issue is with cities which generate false positives. For example, if a user reported a nonsensical location such as *"seconda stella a destra"*, this could possibly be matched to ***"Stella, Savona, SV,  Liguria, Italia"***. To avoid this issue, I looked for all the cities that could match nonsensical patterns and I decided to simply remove them from the list of cities to be matched. Note that these tend to be very small cities that in my case only generated false positives. In general, I tried to keep a balance between avoiding false positives as much as possible while not losing too much level of detail.

The second issue instead regards duplicate names, i.e. cities present in more than one region. In Italy, the list is the following: *"Paterno, San Teodoro, Castro, Peglio, Corvara, Livo, Samone"*. Again, I decided to remove these from the possible matches.

Finally, there are cases in which users write multiple cities in the *"location"* field, where one is possibly their home-town and the others cities they subsequently moved to. In case in which a user moved abroad, i.e. he/she writes something like *"Roma, London"*, then it would be matched to the Italian city only and the other one would simply be ignored. Instead, if all cities are in Italy, then the user would be matched to one of the cities and, since there are no strict patters in which users would write down the sequence of cities, the choice would be as good as random.
