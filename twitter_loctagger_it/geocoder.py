import pandas as pd, re, unidecode, os

class tag_location(object):
    
    """
    Assign an Italian city/region to each twitter user from the 'location field',
    part of a user profile.
    
    :param location: List of 'location' fields.
    :type location: List / Series object
    """
    
    def __init__(self, df):
        df['location_clean'] = clean_list(df.iloc[:,0]); df['id']=df.index
        df_istat = pd.read_excel(rel_path('istat.xlsx'),names=['city_string','city','province',\
                                 'province_code','region','geographic_ripartition','state'],
                                 na_filter = False).apply(lambda x: x.str.lower())
                               
        df_regions = pd.read_excel(rel_path('regions.xlsx'),names=['region_string',\
                                  'region','state']).apply(lambda x: x.str.lower())

        #Generate comparison sets of cities and regions (without accents and without "-")
        df_istat.city_string=df_istat.city_string.apply(lambda x: unidecode.unidecode(x))\
                     .apply(lambda x: re.sub("-",' ', x)).apply(lambda x: x.strip())
        df_regions.region_string=df_regions.region_string.apply(lambda x: unidecode.unidecode(x))\
                      .apply(lambda x: re.sub("-",' ', x)).apply(lambda x: x.strip())
        df_state = [['italy','italia'],['italia','italia']]
        df_state = pd.DataFrame(df_state, columns=['state_string', 'state'])

        duplicate_cities = set(['paternò','paterno','san teodoro','castro','peglio',\
                                'corvara','livo','samone'])
        mistakable_cities = set(['paese','alto','venezia','aosta','rio','lago','re','vita',\
                                 'camino','san paolo','viale','montagna','scala','ne',\
                                 'bella','campana','barbara','ponte','floresta'])
        cities = set(df_istat.city_string.tolist())-duplicate_cities-mistakable_cities
        regions = set(df_regions.region_string.tolist())-set(['lunigiana'])
        state = set(["italia","italy"])
        
        self.location=df['location_clean'];self.df=df;self.cities=cities;self.regions=regions
        self.state=state;self.df_istat=df_istat;self.df_regions=df_regions
        self.df_state=df_state
        
    def __call__(self, separate=True, words=1):
        #City
        comma_sep = self.location.str.split(',').to_list()        
        self.df["city_der"] = self.main_loop(comma_sep, self.cities)
        all_separate = self.all_separate_func(comma_sep)
        for i in range (4,0,-1):
            sep_words = self.x_by_x(all_separate, i)
            self.df['city_der_'+str(i)] = self.main_loop(sep_words, self.cities)
        
        #Region
        for i in range (3,0,-1):
            sep_words = self.x_by_x(all_separate, i)
            self.df['region_der_'+str(i)] = self.main_loop(sep_words, self.regions)
        
        #State
        self.df['state_derived'] = self.main_loop(sep_words, self.state)    
        
        self.df["city_derived"]=self.df["city_der"]
        self.df=self.df.mask(self.df=='')
        self.df["city_derived"]=self.df["city_derived"].combine_first(self.df["city_der_4"])
        self.df["city_derived"]=self.df["city_derived"].combine_first(self.df["city_der_3"])
        self.df["city_derived"]=self.df["city_derived"].combine_first(self.df["city_der_2"])
        self.df["city_derived"]=self.df["city_derived"].combine_first(self.df["city_der_1"])
        self.df["region_derived"]=self.df["region_der_3"]
        self.df["region_derived"]=self.df["region_derived"].combine_first(self.df["region_der_2"])
        self.df["region_derived"]=self.df["region_derived"].combine_first(self.df["region_der_1"])
        
        
        #---------------------------------------------------------------------#
        venezia = self.df.copy()
        venezia.loc[venezia['region_derived'] == 'venezia giulia', "location_original"] = ''
        venezia.loc[venezia['region_derived'] == 'friuli venezia giulia', "location_original"] = ''
        venezia.loc[venezia['region_derived'] == 'regione friuli venezia giulia', "location_original"] = ''
        venezia = venezia.fillna("") 
        comma_sep = venezia['location_original'].str.split(',').to_list()
        all_separate = self.all_separate_func(comma_sep)
        self.df['city_der_venice'] = self.main_loop(all_separate, set(['venezia']))
        self.df=self.df.mask(self.df=='')
        self.df["city_derived"]=self.df["city_derived"].combine_first(self.df["city_der_venice"])
        
        aosta = self.df.copy()
        aosta.loc[aosta['region_derived'] == 'aosta valley', "location_original"] = ''
        aosta = aosta.fillna("") 
        comma_sep = aosta['location_original'].str.split(',').to_list()
        all_separate = self.all_separate_func(comma_sep)
        self.df['city_der_aosta'] = self.main_loop(all_separate, set(['aosta']))
        self.df=self.df.mask(self.df=='')
        self.df["city_derived"]=self.df["city_derived"].combine_first(self.df["city_der_aosta"])
        #---------------------------------------------------------------------#
        
        
        self.df = pd.merge(self.df,self.df_istat, left_on="city_derived", right_on="city_string", how='left')
        self.df = pd.merge(self.df,self.df_regions, left_on="region_derived", right_on="region_string", how='left')
        self.df = pd.merge(self.df,self.df_state, left_on="state_derived", right_on="state_string", how='left')
        self.df["region"]=self.df["region_x"].combine_first(self.df["region_y"])
        self.df["state"]=self.df["state"].combine_first(self.df["state_x"])
        self.df["state"]=self.df["state"].combine_first(self.df["state_y"])
        
        self.df = self.df.fillna("")
        self.df = self.df[['id','location_original','location_clean','city_derived','region_derived',\
                           'state_derived','city','province','province_code',\
                           'region_string','region','geographic_ripartition','state']]
        return self.df
        
    def main_loop(self, users, comp_set):
            temp=[""]*len(users)
            for i in range(len(users)):
                for a in range(len(users[i])):
                    if isinstance(users[i][a], list):
                        for e in range(len(users[i][a])):
                            if users[i][a][e] in comp_set:
                                temp[i]=users[i][a][e]
                    else:
                        if users[i][a] in comp_set:
                            temp[i]=users[i][a]
            return temp

    def all_separate_func(self, users):
        temp=[""]*len(users)
        for i in range(len(users)):
            z=[]
            for a in range(len(users[i])):
                z.append(users[i][a].split(" "))
            temp[i]=z
        return temp

    def x_by_x(self, all_separate, x):
        temp=[""]*len(all_separate)
        for i in range(len(all_separate)):
            z=[]
            for a in range(len(all_separate[i])):
                w=[]
                if len(all_separate[i][a])>=x:
                    for e in range(len(all_separate[i][a])-(x-1)):
                        w.append(" ".join(all_separate[i][a][e:e+x]))
                else:
                    w.append(" ".join(all_separate[i][a]))
                z.append(w)
            temp[i]=z
        return temp

def rel_path(filename):
    """Return the path of this filename relative to the current script
    """
    return os.path.join(os.getcwd(), os.path.dirname(__file__), filename)

def clean_list(list_locations):
    """
    Return list without emojis, all lower case, and without any characters other
    than those specified in 'pattern'
    """
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642" 
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
                          "]+", flags=re.UNICODE)
    pattern_1 = r"[^a-z', ]+"
    pattern_2 = r'(\s+via+\s+[a-z]+)|(\s+viale+\s+[a-z]+)'
    pattern_3 = r',+via+\s+[a-z]+'
    list_locations = list_locations.apply(lambda x: re.sub(emoji_pattern,'', x))\
                                   .apply(lambda x: unidecode.unidecode(x))\
                                   .apply(lambda x: x.lower())\
                                   .apply(lambda x: re.sub(pattern_1,' ', x))\
                                   .apply(lambda x: re.sub(pattern_2,' ', x))\
                                   .apply(lambda x: re.sub(pattern_3,', ', x))\
                                   .apply(lambda x: " ".join(x.split()))\
                                   .apply(lambda x: re.sub(", ",',', x))\
                                   
    return list_locations