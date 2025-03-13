# %% [markdown]
# 1. Loading Required Libraries

# %%
#Data Manipulation
import pandas as pd
import numpy as np

#Visualization
import matplotlib.pyplot as plt

# %% [markdown]
# 2. Loading the data

# %%
df = pd.read_csv('Crime_Data_from_2020_to_Present.csv').set_index('DR_NO')

# %% [markdown]
# 3. Initial Data Inspection

# %%
#Checking file structure
df.info()

# %%
#Checking firts 5 rows
df.head()

# %%
df.isnull().sum()

# %% [markdown]
# 4. Data Cleaning

# %%
#Creating a list with unwanted columns
unwanted_columns = [
    'Part 1-2','Crm Cd','Crm Cd 1','Crm Cd 2','Crm Cd 3',
    'Crm Cd 4','LOCATION','Cross Street','Premis Cd','Weapon Used Cd',
    'Rpt Dist No','AREA','Status','Premis Desc'
]

#Removing said columns
df.drop(columns=unwanted_columns,inplace=True)

# %%
#Filling Unknown values for categorical columns
columns_to_fill = ['Mocodes', 'Vict Sex', 'Vict Descent', 'Weapon Desc']
df[columns_to_fill] = df[columns_to_fill].fillna('Unknown')

# %% [markdown]
# 5. Data Filtering  

# %%
#Removing rows where victim age is greater than 0 and not equal to 120
df_cleaned = df[(df['Vict Age']>0) & (df['Vict Age'] != 120) & (df['LAT'] != 0)]

# %% [markdown]
# 6. Data Standardization

# %%
#Standardizing column names

standardized_columns = {
    'Date Rptd':'Date Reported',
    'DATE OCC':'Date Occurred',
    'TIME OCC':'Time Occurred',
    'AREA NAME':'Area Name',
    'Crm Cd Desc':'Crime Description',
    'Mocodes':'Modus Operandi',
    'Vict Age':'Victim Age',
    'Vict Sex':'Victim Sex',
    'Vict Descent':'Victim Ethnicity',
    'Premis Desc':'Location of Crime',
    'Weapon Desc':'Weapon Used',
    'Status Desc':'Status of case',
    'LAT':'Latitude',
    'LON':'Longitude'
}

df_cleaned.index.name = "Division of Records #"

#Applying dict to columns
df_cleaned= df_cleaned.rename(columns=standardized_columns)

# %%
#Removing time from dates

df_cleaned['Date Occurred'] = pd.to_datetime(df_cleaned['Date Occurred'], format='%m/%d/%y %I:%M %p').dt.date
df_cleaned['Date Reported'] = pd.to_datetime(df_cleaned['Date Reported'], format='%m/%d/%y %I:%M %p').dt.date

# %%
#Standardizing sex column values

def standardized_sexes(sex):
    sex = str(sex).strip().upper()  # Normalize input

    if sex == 'M':
        return 'Male'
    elif sex == 'F':
        return 'Female'
    elif sex in ['X', 'H', '-']:
        return 'UNKNOWN'
    else:
        return sex  

df_cleaned['Victim Sex'] = df_cleaned['Victim Sex'].apply(standardized_sexes)

# %%
#Standardizing Ethnicity column values

standardized_ethnicity = {
    "-":'Unknown',
    "A": "Other Asian",
    "B": "Black",
    "C": "Chinese",
    "D": "Cambodian",
    "F": "Filipino",
    "G": "Guamanian",
    "H": "Hispanic/Latin/Mexican",
    "I": "American Indian/Alaskan Native",
    "J": "Japanese",
    "K": "Korean",
    "L": "Laotian",
    "O": "Other",
    "P": "Pacific Islander",
    "S": "Samoan",
    "U": "Hawaiian",
    "V": "Vietnamese",
    "W": "White",
    "X": "Unknown",
    "Z": "Asian Indian"
}

#Applying map to column
df_cleaned['Victim Ethnicity'] = df_cleaned['Victim Ethnicity'].map(standardized_ethnicity).fillna('Unknown')

# %%
#creating lists to group the type of weapon used

Bladed_Weapons = [
        'AXE','BOWIE KNIFE','FOLDING KNIFE','KITCHEN KNIFE','KNIFE WITH BLADE 6INCHES OR LESS',
        'KNIFE WITH BLADE OVER 6 INCHES IN LENGTH','MACHETE','OTHER KNIFE','RAZOR BLADE','SWITCH BLADE','SWORD','CLEAVER',
        'DIRK/DAGGER','RAZOR','STRAIGHT RAZOR'
]

Blunt_Objects = [
        'CLUB/BAT','CONCRETE BLOCK/BRICK','HAMMER','PIPE/METAL PIPE','ROCK/THROWN OBJECT','STICK','BLUNT INSTRUMENT','BLACKJACK'
]

Chemical_Weapons = ['CAUSTIC CHEMICAL/POISON','MACE/PEPPER SPRAY']

Explosives = ['BOMB THREAT']

Firearms = [
        'AIR PISTOL/REVOLVER/RIFLE/BB GUN','ANTIQUE FIREARM','ASSAULT WEAPON/UZI/AK47/ETC','AUTOMATIC WEAPON/SUB-MACHINE GUN',
        'HAND GUN','HECKLER & KOCH 91 SEMIAUTOMATIC ASSAULT RIFLE','HECKLER & KOCH 93 SEMIAUTOMATIC ASSAULT RIFLE','M1-1 SEMIAUTOMATIC ASSAULT RIFLE',
        'M-14 SEMIAUTOMATIC ASSAULT RIFLE','MAC-10 SEMIAUTOMATIC ASSAULT WEAPON','MAC-11 SEMIAUTOMATIC ASSAULT WEAPON','OTHER FIREARM','RELIC FIREARM',
        'REVOLVER','RIFLE','SAWED OFF RIFLE/SHOTGUN','SEMI-AUTOMATIC PISTOL','SEMI-AUTOMATIC RIFLE','SHOTGUN','SIMULATED GUN','STARTER PISTOL/REVOLVER',
        'STUN GUN','TOY GUN','UNK TYPE SEMIAUTOMATIC ASSAULT RIFLE','UNKNOWN FIREARM','UZI SEMIAUTOMATIC ASSAULT RIFLE'
]

other = [
        'BELT FLAILING INSTRUMENT/CHAIN','BOARD','BOTTLE','BOW AND ARROW','BRASS KNUCKLES','DEMAND NOTE',
        'DOG/ANIMAL (SIC ANIMAL ON)','EXPLOXIVE DEVICE','FIRE','FIXED OBJECT','GLASS','ICE PICK','LIQUOR/DRUGS','MARTIAL ARTS WEAPONS',
        'OTHER CUTTING INSTRUMENT','PHYSICAL PRESENCE','ROPE/LIGATURE','SCALDING LIQUID','SCISSORS','SCREWDRIVER','STRONG-ARM (HANDS, FIST, FEET OR BODILY FORCE)',
        'SYRINGE','TIRE IRON','Unknown','UNKNOWN TYPE CUTTING INSTRUMENT','UNKNOWN WEAPON/OTHER WEAPON','VEHICLE','VERBAL THREAT'
]

#Creating a function which will categorize each weapon
def weapon_standardization(weapon):
        if weapon == 'Unknown':
                return 'Unknown'
        elif weapon in Bladed_Weapons:
                return 'Bladed Weapons'
        elif weapon in Blunt_Objects:
                return 'Blunt Objects'
        elif weapon in Chemical_Weapons:
                return 'Chemical Weapons'
        elif weapon in Explosives:
                return 'Explosives'
        elif weapon in Firearms:
                return 'Firearms'
        elif weapon in other:
                return 'Other Weapons'
        else:
                return 'Uncategorized'

#Applying function to the weapon used column     
df_cleaned['Weapon Used'] = df_cleaned['Weapon Used'].apply(weapon_standardization)

#Saving cleaned dataset for other uses.
df_cleaned.to_csv('LA Crime Data - Cleaned.csv')

# %%
#Standardizing the time occurred column values

df_cleaned['Time Occurred'] = df_cleaned['Time Occurred'].astype(str).str.zfill(4)

def time_fixer(time):
    return f'{time[:2]}:{time[2:]}'

df_cleaned['Time Occurred'] = df_cleaned['Time Occurred'].apply(time_fixer)
df_cleaned['Time Occurred'] = pd.to_datetime(df_cleaned['Time Occurred'], format='%H:%M').dt.strftime('%I:%M %p')

# %% [markdown]
# 6. Data Exploration

# %%
#Creating a column which shows the total amount of days that passed between the day the crime was committed, and the day it was reported.
df_cleaned['Days Elapsed'] = (pd.to_datetime(df_cleaned['Date Reported']) - pd.to_datetime(df_cleaned['Date Occurred'])).dt.days

#Creating Year, Quarter, Month columns
df_cleaned['Year'] = pd.to_datetime(df_cleaned['Date Occurred']).dt.year
df_cleaned['Quarter'] = pd.to_datetime(df_cleaned['Date Occurred']).dt.quarter
df_cleaned['Month'] = pd.to_datetime(df_cleaned['Date Occurred']).dt.month_name()

# %%
#General view of weapons used in crimes
df_cleaned['Weapon Used'].value_counts().sort_values().plot(kind='barh')
plt.title('Weapons Used')
plt.ylabel('')
plt.xlabel('')
plt.show()

# %%
df_filtered = df_cleaned[~df_cleaned['Weapon Used'].isin(['Unknown', 'Other Weapons'])]

df_filtered['Weapon Used'].value_counts().sort_values().plot(kind='barh', figsize=(10,6))
plt.xlabel('Number of Crimes')
plt.ylabel('')
plt.title('Weapons Used (Excluding Unknown & Other)')
plt.show()

# %%
#Calculating the average days it takes to report a crime

print(f'{np.floor(df_cleaned['Days Elapsed'].mean())} Days')

# %%
#Calculating the average days it takes to report a crime by gender

genders_df = df_cleaned.pivot_table(
    index='Victim Sex',
    values='Days Elapsed',
    aggfunc='mean'
).apply(np.floor)

genders_df = genders_df[genders_df.index != 'UNKNOWN']

genders_df.plot(kind='bar', legend=False)
plt.title('Average Days Elapsed by Gender')
plt.xlabel('')
plt.ylabel('')
plt.xticks(rotation=0)  # Ensures x-axis labels are readable

plt.show()

# %%
df_cleaned['Victim Sex'].value_counts().plot(kind='pie',autopct='%1.1f%%')
plt.title('Total Crimes per Gender')
plt.ylabel('')
plt.show()

# %%
df_cleaned['Area Name'].value_counts().head(10).sort_values().plot(kind='barh',)
plt.title('Top 10 areas of Crime')
plt.xlabel('')
plt.ylabel('')
plt.show()

# %%
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Convert 'Month' column to a categorical type with the correct order
df_cleaned["Month"] = pd.Categorical(df_cleaned["Month"], categories=month_order, ordered=True)

years_and_months_df = df_cleaned.pivot_table(
    index="Month",
    values="Victim Age",
    columns="Year",
    aggfunc="count",
    observed=True
)

years_and_months_df = years_and_months_df.sort_index()
years_and_months_df.plot()
plt.xlabel('')
plt.show()

# %%
years_and_quarters_df = df_cleaned.pivot_table(
    index="Month",
    values="Victim Age",
    columns="Year",
    aggfunc="count",
    observed=True
)

years_and_months_df = years_and_months_df.sort_index()
years_and_months_df.plot(subplots=True)
plt.show()

# %%
years_df = df_cleaned['Year'].value_counts().sort_index()
years_df.plot(marker='o')
plt.title('Crimes Reported by Year')
plt.xlabel('')
plt.grid(True)

plt.show()

# %%
#Total crimes by ethnicity
victim_Ethnicity = df_cleaned['Victim Ethnicity'].value_counts().sort_values()
victim_Ethnicity.plot(kind='barh')
plt.show()

# %%
# Filter out outlier ethnicities
valid_ethnicities = [
    'Chinese', 'Filipino', 'Korean', 'Unknown', 
    'Other Asian', 'Other', 'Black', 'White', 'Hispanic/Latin/Mexican']
filtered_df = df_cleaned[df_cleaned['Victim Ethnicity'].isin(valid_ethnicities)]

# Count occurrences
ethnicity_counts = filtered_df['Victim Ethnicity'].value_counts().sort_values()

# Plot horizontal bar chart
plt.figure(figsize=(10,6))
ethnicity_counts.plot(kind='barh', color='skyblue')
plt.xlabel('')
plt.ylabel('')
plt.title('Total Crimes by Ethnicity (Without Outliers)')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()


