#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'><img src='../Pierian_Data_Logo.png'/></a>
# ___
# <center><em>Copyright by Pierian Data Inc.</em></center>
# <center><em>For more information, visit us at <a href='http://www.pieriandata.com'>www.pieriandata.com</a></em></center>

# # Capstone Project
# ## Overview
# 
# If you are planning on going out to see a movie, how well can you trust online reviews and ratings? *Especially* if the same company showing the rating *also* makes money by selling movie tickets. Do they have a bias towards rating movies higher than they should be rated?
# 
# ### Goal:
# 
# **Your goal is to complete the tasks below based off the 538 article and see if you reach a similar conclusion. You will need to use your pandas and visualization skills to determine if Fandango's ratings in 2015 had a bias towards rating movies better to sell more tickets.**
# 
# ---
# ---
# 
# **Complete the tasks written in bold.**
# 
# ---
# ----
# 
# ## Part One: Understanding the Background and Data
# 
# 
# **TASK: Read this article: [Be Suspicious Of Online Movie Ratings, Especially Fandango’s](http://fivethirtyeight.com/features/fandango-movies-ratings/)**

# ----
# 
# **TASK: After reading the article, read these two tables giving an overview of the two .csv files we will be working with:**
# 
# ### The Data
# 
# This is the data behind the story [Be Suspicious Of Online Movie Ratings, Especially Fandango’s](http://fivethirtyeight.com/features/fandango-movies-ratings/) openly available on 538's github: https://github.com/fivethirtyeight/data. There are two csv files, one with Fandango Stars and Displayed Ratings, and the other with aggregate data for movie ratings from other sites, like Metacritic,IMDB, and Rotten Tomatoes.
# 
# #### all_sites_scores.csv

# -----
# 
# `all_sites_scores.csv` contains every film that has a Rotten Tomatoes rating, a RT User rating, a Metacritic score, a Metacritic User score, and IMDb score, and at least 30 fan reviews on Fandango. The data from Fandango was pulled on Aug. 24, 2015.

# Column | Definition
# --- | -----------
# FILM | The film in question
# RottenTomatoes | The Rotten Tomatoes Tomatometer score  for the film
# RottenTomatoes_User | The Rotten Tomatoes user score for the film
# Metacritic | The Metacritic critic score for the film
# Metacritic_User | The Metacritic user score for the film
# IMDB | The IMDb user score for the film
# Metacritic_user_vote_count | The number of user votes the film had on Metacritic
# IMDB_user_vote_count | The number of user votes the film had on IMDb

# ----
# ----
# 
# #### fandango_scape.csv

# `fandango_scrape.csv` contains every film 538 pulled from Fandango.
# 
# Column | Definiton
# --- | ---------
# FILM | The movie
# STARS | Number of stars presented on Fandango.com
# RATING |  The Fandango ratingValue for the film, as pulled from the HTML of each page. This is the actual average score the movie obtained.
# VOTES | number of people who had reviewed the film at the time we pulled it.

# ----
# 
# **TASK: Import any libraries you think you will use:**

# In[3]:


# IMPORT HERE!

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:





# ## Part Two: Exploring Fandango Displayed Scores versus True User Ratings
# 
# Let's first explore the Fandango ratings to see if our analysis agrees with the article's conclusion.
# 
# **TASK: Run the cell below to read in the fandango_scrape.csv file**

# In[4]:


fandango = pd.read_csv("fandango_scrape.csv")


# **TASK: Explore the DataFrame Properties and Head.**

# In[5]:


fandango.head()


# In[6]:


fandango.info()


# In[7]:


fandango[[ 'STARS', 'RATING', 'VOTES']]


# **TASK: Let's explore the relationship between popularity of a film and its rating. Create a scatterplot showing the relationship between rating and votes. Feel free to edit visual styling to your preference.**

# In[8]:


# CODE HERE
plt.figure(figsize=(12,4), dpi =150)
sns.scatterplot(data = fandango, x='RATING', y="VOTES")


# In[ ]:





# **TASK: Calculate the correlation between the columns:**

# In[9]:


# CODE HERE

fandango.corr(numeric_only=True)
 


# In[ ]:





# **TASK: Assuming that every row in the FILM title column has the same format:**
# 
#     Film Title Name (Year)
#     
# **Create a new column that is able to strip the year from the title strings and set this new column as YEAR**

# In[10]:


# CODE HERE
title = 'Film Title Name (Year)'
title.split('(')[-1].replace(')','')


# In[11]:


fandango['YEAR']= fandango['FILM'].apply(lambda title:title.split('(')[-1].replace(')',''))


# **TASK: How many movies are in the Fandango DataFrame per year?**

# In[12]:


fandango


# In[13]:


#CODE HERE

fandango['YEAR'].value_counts()


# In[14]:


fandango['count']=fandango['YEAR'].value_counts()


# In[ ]:





# In[ ]:





# **TASK: Visualize the count of movies per year with a plot:**

# In[16]:


#CODE HERE
sns.countplot(data= fandango, x='YEAR')


# In[17]:


sns.histplot(data =fandango, x='YEAR', y='count')


# **TASK: What are the 10 movies with the highest number of votes?**

# In[18]:


#CODE HERE
fandango.nlargest(10, 'VOTES')
fandango = fandango.drop('count', axis = 1)


# In[19]:


fandango


# In[20]:


fandango[fandango['VOTES'] == 0]
  
    


# In[ ]:





# **TASK: How many movies have zero votes?**

# In[21]:


#CODE HERE
len(fandango[fandango['VOTES'] == 0])


# In[ ]:





# **TASK: Create DataFrame of only reviewed films by removing any films that have zero votes.**

# In[22]:


#CODE HERE
fan_reviewed = fandango[fandango['VOTES'] > 0]


# In[23]:


fan_reviewed


# ----
# 
# **As noted in the article, due to HTML and star rating displays, the true user rating may be slightly different than the rating shown to a user. Let's visualize this difference in distributions.**
# 
# **TASK: Create a KDE plot (or multiple kdeplots) that displays the distribution of ratings that are displayed (STARS) versus what the true rating was from votes (RATING). Clip the KDEs to 0-5.**

# In[24]:


#CODE HERE
plt.figure(figsize=(10,4), dpi =150)
sns.kdeplot(data = fan_reviewed, x ='RATING', clip= [0,5], fill = True, label = 'True_Rating')
sns.kdeplot(data = fan_reviewed, x ='STARS', clip= [0,5], fill = True, label = 'STARS_DISPLAYED')
plt.legend(loc=(1.05,0.5))


# In[ ]:





# **TASK: Let's now actually quantify this discrepancy. Create a new column of the different between STARS displayed versus true RATING. Calculate this difference with STARS-RATING and round these differences to the nearest decimal point.**

# In[25]:


#CODE HERE


# In[26]:


fan_reviewed['STARS_DIFF']= fan_reviewed ['STARS']-fan_reviewed ['RATING']


# In[27]:


fan_reviewed['STARS_DIFF'] = fan_reviewed ['STARS_DIFF'].round(2)


# In[28]:


fan_reviewed


# In[ ]:





# **TASK: Create a count plot to display the number of times a certain difference occurs:**

# In[29]:


plt.figure(figsize=(12,4),dpi=150)
sns.countplot(data=fan_reviewed, x='STARS_DIFF', palette = 'magma')


# In[ ]:





# **TASK: We can see from the plot that one movie was displaying over a 1 star difference than its true rating! What movie had this close to 1 star differential?**

# In[30]:


#CODE HERE
fan_reviewed[fan_reviewed['STARS_DIFF']==1]


# In[ ]:





# ## Part Three: Comparison of Fandango Ratings to Other Sites
# 
# Let's now compare the scores from Fandango to other movies sites and see how they compare.
# 
# **TASK: Read in the "all_sites_scores.csv" file by running the cell below**

# In[31]:


all_sites = pd.read_csv("all_sites_scores.csv")


# **TASK: Explore the DataFrame columns, info, description.**

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ### Rotten Tomatoes
# 
# Let's first take a look at Rotten Tomatoes. RT has two sets of reviews, their critics reviews (ratings published by official critics) and user reviews. 
# 
# **TASK: Create a scatterplot exploring the relationship between RT Critic reviews and RT User reviews.**

# In[326]:


# CODE HERE
plt.figure(figsize=(10,4),dpi=150)
sns.scatterplot(data= all_sites, y ='RottenTomatoes_User', x = 'RottenTomatoes')
plt.ylim(0,100)
plt.xlim(0,100)


# In[209]:





# Let's quantify this difference by comparing the critics ratings and the RT User ratings. We will calculate this with RottenTomatoes-RottenTomatoes_User. Note: Rotten_Diff here is Critics - User Score. So values closer to 0 means aggrement between Critics and Users. Larger positive values means critics rated much higher than users. Larger negative values means users rated much higher than critics.
# 
# **TASK: Create a new column based off the difference between critics ratings and users ratings for Rotten Tomatoes. Calculate this with RottenTomatoes-RottenTomatoes_User**

# In[43]:


#CODE HERE
all_sites['Rotten_Diff']= all_sites['RottenTomatoes'] - all_sites['RottenTomatoes_User']


# In[211]:





# Let's now compare the overall mean difference. Since we're dealing with differences that could be negative or positive, first take the absolute value of all the differences, then take the mean. This would report back on average to absolute difference between the critics rating versus the user rating.

# **TASK: Calculate the Mean Absolute Difference between RT scores and RT User scores as described above.**

# In[44]:


# CODE HERE
all_sites['Rotten_Diff'].apply(abs).mean()


# In[213]:





# **TASK: Plot the distribution of the differences between RT Critics Score and RT User Score. There should be negative values in this distribution plot. Feel free to use KDE or Histograms to display this distribution.**

# In[333]:


#CODE HERE
plt.figure(figsize=(10,4),dpi=150)
sns.histplot(data=all_sites, x= 'Rotten_Diff', kde =True,bins=25)


# In[215]:





# **TASK: Now create a distribution showing the *absolute value* difference between Critics and Users on Rotten Tomatoes.**

# In[336]:


#CODE HERE
plt.figure(figsize=(10,4),dpi=150)
sns.histplot(data=all_sites, x= all_sites['Rotten_Diff'].apply(abs), kde =True,bins=25)


# In[217]:





# **Let's find out which movies are causing the largest differences. First, show the top 5 movies with the largest *negative* difference between Users and RT critics. Since we calculated the difference as Critics Rating - Users Rating, then large negative values imply the users rated the movie much higher on average than the critics did.**

# **TASK: What are the top 5 movies users rated higher than critics on average:**

# In[47]:


# CODE HERE

all_sites.nsmallest(5,'Rotten_Diff')['FILM']


# In[ ]:





# **TASK: Now show the top 5 movies critics scores higher than users on average.**

# In[343]:


# CODE HERE
all_sites.nlargest(5,'Rotten_Diff')['FILM']


# In[221]:





# ## MetaCritic
# 
# Now let's take a quick look at the ratings from MetaCritic. Metacritic also shows an average user rating versus their official displayed rating.

# **TASK: Display a scatterplot of the Metacritic Rating versus the Metacritic User rating.**

# In[344]:


# CODE HERE
all_sites.head()


# In[33]:


plt.figure(figsize=(10,4), dpi = 150)
sns.scatterplot(data=all_sites, x= 'Metacritic',y='Metacritic_User')
plt.xlim(0,100)
plt.ylim(0,10)


# In[223]:





# In[ ]:





# In[ ]:





# ## IMDB
# 
# Finally let's explore IMDB. Notice that both Metacritic and IMDB report back vote counts. Let's analyze the most popular movies.
# 
# **TASK: Create a scatterplot for the relationship between vote counts on MetaCritic versus vote counts on IMDB.**

# In[36]:


#CODE HERE
plt.figure(figsize=(10,4), dpi = 150)
sns.scatterplot(data=all_sites, x= 'Metacritic_user_vote_count',y='IMDB_user_vote_count')


# In[225]:





# **Notice there are two outliers here. The movie with the highest vote count on IMDB only has about 500 Metacritic ratings. What is this movie?**
# 
# **TASK: What movie has the highest IMDB user vote count?**

# In[52]:


#CODE HERE
all_sites.nlargest(1,'IMDB_user_vote_count')


# In[227]:





# **TASK: What movie has the highest Metacritic User Vote count?**

# In[54]:


#CODE HERE
all_sites.nlargest(1,'Metacritic_user_vote_count')


# In[229]:





# ## Fandago Scores vs. All Sites
# 
# Finally let's begin to explore whether or not Fandango artificially displays higher ratings than warranted to boost ticket sales.

# **TASK: Combine the Fandango Table with the All Sites table. Not every movie in the Fandango table is in the All Sites table, since some Fandango movies have very little or no reviews. We only want to compare movies that are in both DataFrames, so do an *inner* merge to merge together both DataFrames based on the FILM columns.**

# In[87]:


#CODE HERE
df = pd.merge(fandango, all_sites,on ='FILM', how='inner')


# In[56]:


df


# In[232]:





# In[233]:





# ### Normalize columns to Fandango STARS and RATINGS 0-5 
# 
# Notice that RT,Metacritic, and IMDB don't use a score between 0-5 stars like Fandango does. In order to do a fair comparison, we need to *normalize* these values so they all fall between 0-5 stars and the relationship between reviews stays the same.
# 
# **TASK: Create new normalized columns for all ratings so they match up within the 0-5 star range shown on Fandango. There are many ways to do this.**
# 
# Hint link: https://stackoverflow.com/questions/26414913/normalize-columns-of-pandas-data-frame
# 
# 
# Easier Hint:
# 
# Keep in mind, a simple way to convert ratings:
# * 100/20 = 5 
# * 10/2 = 5

# In[88]:


# CODE HERE
df.describe().transpose()


# In[89]:


df.describe().transpose()


# In[90]:


df.describe().transpose()['max']


# In[91]:


df['RT_Norm']=np.round(df['RottenTomatoes']/20,1)
df['RTU_Norm']=np.round(df['RottenTomatoes_User']/20,1)


# In[92]:


df['Meta_Norm']=np.round(df['Metacritic']/20,1)
df['Mata_U_Norm']=np.round(df['Metacritic_User']/2,1)


# In[93]:


df['IMBD_Norm']=np.round(df['IMDB']/2,1)


# In[94]:


df.head()


# **TASK: Now create a norm_scores DataFrame that only contains the normalizes ratings. Include both STARS and RATING from the original Fandango table.**

# In[ ]:





# In[97]:


norm_scores = df[['STARS', 'RATING','RT_Norm', 'RTU_Norm', 'Meta_Norm','Mata_U_Norm', 'IMBD_Norm']]


# In[100]:


norm_scores.head()


# In[241]:





# ### Comparing Distribution of Scores Across Sites
# 
# 
# Now the moment of truth! Does Fandango display abnormally high ratings? We already know it pushs displayed RATING higher than STARS, but are the ratings themselves higher than average?
# 
# 
# **TASK: Create a plot comparing the distributions of normalized ratings across all sites. There are many ways to do this, but explore the Seaborn KDEplot docs for some simple ways to quickly show this. Don't worry if your plot format does not look exactly the same as ours, as long as the differences in distribution are clear.**
# 
# Quick Note if you have issues moving the legend for a seaborn kdeplot: https://github.com/mwaskom/seaborn/issues/2280

# In[242]:


#CODE HERE


# In[127]:


fig, ax = plt.subplots(figsize=(15,6), dpi =200)
sns.kdeplot(data=norm_scores,shade = True, palette='Set1')
plt.xlim(0,5)
plt.ylim(0,0.12)
#plt.legend(loc=(0.5, 1.5))

def move_legend(ax, new_loc, **kws):
    old_legend = ax.legend_
    handles = old_legend.legendHandles
    labels = [t.get_text() for t in old_legend.get_texts()]
    title = old_legend.get_title().get_text()
    ax.legend(handles, labels, loc=new_loc, title=title, **kws)
    
move_legend(ax, "upper left")


# In[244]:





# **Clearly Fandango has an uneven distribution. We can also see that RT critics have the most uniform distribution. Let's directly compare these two.** 
# 
# **TASK: Create a KDE plot that compare the distribution of RT critic ratings against the STARS displayed by Fandango.**

# In[136]:


#CODE HERE
fig, ax = plt.subplots(figsize=(15,6), dpi =200)
sns.kdeplot(data=norm_scores[['RT_Norm','STARS']],clip=[0,5],shade = True, palette='Set1')

move_legend(ax, "upper left")


# In[167]:





# **OPTIONAL TASK: Create a histplot comparing all normalized scores.**

# In[157]:


#CODE HERE
plt.figure(figsize=(10,4), dpi=200)
sns.histplot(data=norm_scores, bins=53)



# In[168]:





# 
# ### How are the worst movies rated across all platforms?
# 
# **TASK: Create a clustermap visualization of all normalized scores. Note the differences in ratings, highly rated movies should be clustered together versus poorly rated movies. Note: This clustermap does not need to have the FILM titles as the index, feel free to drop it for the clustermap.**

# In[ ]:


# CODE HERE


# In[158]:


sns.clustermap(norm_scores,cmap = 'magma', col_cluster=False)


# **TASK: Clearly Fandango is rating movies much higher than other sites, especially considering that it is then displaying a rounded up version of the rating. Let's examine the top 10 worst movies. Based off the Rotten Tomatoes Critic Ratings, what are the top 10 lowest rated movies? What are the normalized scores across all platforms for these movies? You may need to add the FILM column back in to your DataFrame of normalized scores to see the results.**

# In[159]:


# CODE HERE
norm_scores.columns


# In[160]:


norm_films = df[['FILM','STARS', 'RATING', 'RT_Norm', 'RTU_Norm', 'Meta_Norm', 'Mata_U_Norm',
       'IMBD_Norm']]


# In[164]:


worst_films = norm_films.nsmallest(10,'RT_Norm')


# In[248]:





# **FINAL TASK: Visualize the distribution of ratings across all sites for the top 10 worst movies.**

# In[165]:


# CODE HERE
fig, ax = plt.subplots(figsize=(15,6), dpi =200)
sns.kdeplot(data=worst_films,shade = True, palette='Set1')


# In[251]:





# ---
# ----
# 
# <img src="https://upload.wikimedia.org/wikipedia/en/6/6f/Taken_3_poster.jpg">
# 
# **Final thoughts: Wow! Fandango is showing around 3-4 star ratings for films that are clearly bad! Notice the biggest offender, [Taken 3!](https://www.youtube.com/watch?v=tJrfImRCHJ0). Fandango is displaying 4.5 stars on their site for a film with an [average rating of 1.86](https://en.wikipedia.org/wiki/Taken_3#Critical_response) across the other platforms!**

# In[253]:





# In[254]:


0.4+2.3+1.3+2.3+3


# In[255]:


9.3/5


# ----
