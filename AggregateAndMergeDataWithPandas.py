#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# Today we'll dive deep into a dataset all about LEGO. From the dataset we can ask whole bunch of interesting questions about the history of the LEGO company, their product offering, and which LEGO set ultimately rules them all:
# 
# <ul type="square">
# <li>What is the most enormous LEGO set ever created and how many parts did it have?</li>
# 
# <li>How did the LEGO company start out? In which year were the first LEGO sets released and how many sets did the company sell when it first launched?</li>
# 
# <li>Which LEGO theme has the most sets? Is it one of LEGO's own themes like Ninjago or a theme they licensed liked Harry Potter or Marvel Superheroes?</li>
# 
# <li>When did the LEGO company really expand its product offering? Can we spot a change in the company strategy based on how many themes and sets did it released year-on-year?</li>
# 
# <li>Did LEGO sets grow in size and complexity over time? Do older LEGO 
# sets tend to have more or fewer parts than newer sets?</li>
# </ul>
# 
# **Data Source**
# 
# [Rebrickable](https://rebrickable.com/downloads/) has compiled data on all the LEGO pieces in existence. I recommend you use download the .csv files provided in this lesson. 

# <img src='assets/bricks.jpg'>

# # Import Statements

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt


# # Data Exploration

# **Challenge**: How many different colours does the LEGO company produce? Read the colors.csv file in the data folder and find the total number of unique colours. Try using the [.nunique() method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.nunique.html?highlight=nunique#pandas.DataFrame.nunique) to accomplish this.

# In[6]:


df = pd.read_csv('day73-data/colors.csv')
df.head()


# Use df.nunique() to return the number of unique values in each column

# In[7]:


df.nunique()


# **Challenge**: Find the number of transparent colours where <code>is_trans == 't'</code> versus the number of opaque colours where <code>is_trans == 'f'</code>. See if you can accomplish this in two different ways.

# <strong>Method 1 : Use the groupby method to make groups on the is_trans column and then use the .count() function</strong>

# In[10]:


transparent_group = df.groupby('is_trans')
transparent_group.count()


# <strong> Method 2: Use .value_counts() method to return a series with the index as the values and the counts of each value as the values in the column </strong>

# In[13]:


df['is_trans'].value_counts()


# <strong> Method 3, Use df.pivot_table() </strong>

# In[15]:


df.pivot_table(columns='is_trans', values='id', aggfunc='count')


# <h3> Understanding LEGO Themes vs. LEGO Sets </h3>

# <h4> Walk into a LEGO store and you will see their products organised by theme. Their themes include Star Wars, Batman, Harry Potter and many more. </h4>
# 
# <img src='https://i.imgur.com/aKcwkSx.png'>

# <h4> A lego set is a particular box of LEGO or product. Therefore, a single theme typically has many different sets. </h4>
# 
# <img src='https://i.imgur.com/whB1olq.png'>

# The <code>sets.csv</code> data contains a list of sets over the years and the number of parts that each of these sets contained.
# 
# **Challenge**: Read the sets.csv data and take a look at the first and last couple of rows. 

# In[19]:


sets_df = pd.read_csv('day73-data/sets.csv')


# In[20]:


sets_df.head()


# **Challenge**: In which year were the first LEGO sets released and what were these sets called?

# In[21]:


sets_df['year'].min()


# In[26]:


mask = sets_df['year'] == 1949
sets_df[mask]['name']


# **Challenge**: How many different sets did LEGO sell in their first year? How many types of LEGO products were on offer in the year the company started?

# In[27]:


sets_df[mask]['name'].count()


# **Challenge**: Find the top 5 LEGO sets with the most number of parts. 

# In[30]:


sets_df.nlargest(n=5, columns='num_parts')


# **Challenge**: Use <code>.groupby()</code> and <code>.count()</code> to show the number of LEGO sets released year-on-year. How do the number of sets released in 1955 compare to the number of sets released in 2019? 

# In[36]:


counts_by_year_df = sets_df.groupby('year').count()['set_num']


# In[37]:


counts_by_year_df.head()


# **Challenge**: Show the number of LEGO releases on a line chart using Matplotlib. <br>
# <br>
# Note that the .csv file is from late 2020, so to plot the full calendar years, you will have to exclude some data from your chart. Can you use the slicing techniques covered in Day 21 to avoid plotting the last two years? The same syntax will work on Pandas DataFrames. 

# In[38]:


plt.figure(figsize=(16,10))
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Year', fontsize=16)
plt.ylabel('Number of Sets', fontsize=16)
plt.ylim(0, 850)
plt.plot(counts_by_year_df.index, counts_by_year_df)


# In[39]:


plt.figure(figsize=(16,10))
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Year', fontsize=16)
plt.ylabel('Number of Sets', fontsize=16)
plt.ylim(0, 850)
plt.plot(counts_by_year_df.index[0:-3], counts_by_year_df[0:-3])


# ### Aggregate Data with the Python .agg() Function
# 
# Let's work out the number of different themes shipped by year. This means we have to count the number of unique theme_ids per calendar year.

# In[46]:


themes_by_year = sets_df.groupby('year')
themes_by_year = themes_by_year.agg(func={'theme_id':pd.Series.nunique})
themes_by_year.rename(columns={'theme_id':'nr_themes'}, inplace=True)
themes_by_year.tail()


# **Challenge**: Plot the number of themes released by year on a line chart. Only include the full calendar years (i.e., exclude 2020 and 2021). 

# In[55]:


plt.figure(figsize=(16,10))
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Year', fontsize=16)
plt.ylabel('Number of themes', fontsize=16)
plt.ylim(0, 100)
plt.plot(themes_by_year.index[:-2], themes_by_year.values[:-2])


# ### Line Charts with Two Seperate Axes

# In[65]:


plt.figure(figsize=(16,10))
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
ax1 = plt.gca()
ax2 = plt.twinx()

ax1.plot(themes_by_year.index[:-2], themes_by_year.values[:-2], color='g')
ax2.plot(counts_by_year_df.index[:-2], counts_by_year_df.values[:-2], color='b')

ax1.set_xlabel('Year', fontsize=16)
ax1.set_ylabel('Number of Themes', fontsize=16, color='g')
ax2.set_ylabel('Number of Sets', fontsize=16, color='b')


# **Challenge**: Use the <code>.groupby()</code> and <code>.agg()</code> function together to figure out the average number of parts per set. How many parts did the average LEGO set released in 1954 compared to say, 2017?

# In[73]:


parts_per_set = sets_df.groupby('year').agg(func={'num_parts': pd.Series.mean})


# In[74]:


parts_per_set.head()


# ### Scatter Plots in Matplotlib

# **Challenge**: Has the size and complexity of LEGO sets increased over time based on the number of parts? Plot the average number of parts over time using a Matplotlib scatter plot. See if you can use the [scatter plot documentation](https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.scatter.html) before I show you the solution. Do you spot a trend in the chart? 

# In[77]:


plt.figure(figsize=(16,10))
plt.xlabel('Year', fontsize=16)
plt.ylabel('Mean Parts Per Set', fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.scatter(parts_per_set.index, parts_per_set.values)


# ### Number of Sets per LEGO Theme

# LEGO has licensed many hit franchises from Harry Potter to Marvel Super Heros to many others. But which theme has the largest number of individual sets? 

# <img src='https://i.imgur.com/Sg4lcjx.png'>

# **Challenge** Use what you know about HTML markup and tags to display the database schema: https://i.imgur.com/Sg4lcjx.png

# 

# ### Database Schemas, Foreign Keys and Merging DataFrames
# 
# The themes.csv file has the actual theme names. The sets .csv has <code>theme_ids</code> which link to the <code>id</code> column in the themes.csv. 

# **Challenge**: Explore the themes.csv. How is it structured? Search for the name 'Star Wars'. How many <code>id</code>s correspond to this name in the themes.csv? Now use these <code>id</code>s and find the corresponding the sets in the sets.csv (Hint: you'll need to look for matches in the <code>theme_id</code> column)

# In[82]:


themes = pd.read_csv('day73-data/themes.csv', index_col='id')
themes.head()


# In[87]:


mask = themes['name'].str.contains('Star Wars')
star_wars_themes = themes[mask]
star_wars_themes


# In[93]:


mask2 = sets_df['theme_id'].isin(star_wars_themes.index)
star_wars_sets = sets_df[mask2]
star_wars_sets.head()


# In[ ]:





# In[ ]:





# ### Merging (i.e., Combining) DataFrames based on a Key
# 

# In[95]:


set_theme_count = sets_df['theme_id'].value_counts()
set_theme_count.head()


# In[99]:


set_theme_count = set_theme_count.to_frame()


# In[103]:


set_theme_count.reset_index(level=0, inplace=True)


# In[108]:


set_theme_count.rename(columns={'index': 'id', 'theme_id':'set_count'}, inplace=True)


# In[110]:


set_theme_count


# In[113]:


merged_df = set_theme_count.merge(right=themes, on='id')
merged_df.head()


# In[116]:


plt.figure(figsize=(16,10))
plt.xticks(fontsize=16, rotation=45)
plt.yticks(fontsize=16)
plt.xlabel('Theme Name', fontsize=16)
plt.ylabel('Set Count', fontsize=16)
plt.bar(merged_df['name'][:10], merged_df['set_count'][0:10])


# In[ ]:




