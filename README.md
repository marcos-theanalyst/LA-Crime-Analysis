# Los Angeles Crime Trends Analysis

## Project Overview

- **Project Title**: Los Angeles Crime Trends Analysis 
- **Data**: [`LA Crime Data`](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data)

This project is designed to demonstrate python skills and techniques typically used by data analysts to explore, clean, and analyze retail sales data. The project involves importing relevant libraries, setting up dataframes, initial data inspection, data cleaning, data standardization, EDA and more. This was done with the goal of answering specific questions through python code.

## Objectives

- Analyze crime trends in Los Angeles, identifying key patterns in crime types, locations, time, victim demographics, and reporting delays.
- Identify and remove any records with missing or null values.
- Perform basic exploratory data analysis to understand the dataset.
- Use Python to derive insights from the data.

## Project Structure

### 1. Importing Libraries

```py
#Data Manipulation
import pandas as pd
import numpy as np

#Visualization
import matplotlib.pyplot as plt
```
### 2. Creating dataframe

```py
df = pd.read_csv('Crime_Data_from_2020_to_Present.csv').set_index('DR_NO')
```

### 3. Initial Data Inspection

```py
#Checking file structure
df.info()

#Checking firts 5 rows
df.head()

#Checking null values in each column
df.isnull().sum()
```

### 4. Data Cleaning

```py
#Creating a list with unwanted columns
unwanted_columns = [
    'Part 1-2','Crm Cd','Crm Cd 1','Crm Cd 2','Crm Cd 3',
    'Crm Cd 4','LOCATION','Cross Street','Premis Cd','Weapon Used Cd',
    'Rpt Dist No','AREA','Status','Premis Desc'
]

#Removing said columns
df.drop(columns=unwanted_columns,inplace=True)

#Filling Unknown values for categorical columns
columns_to_fill = ['Mocodes', 'Vict Sex', 'Vict Descent', 'Weapon Desc']
df[columns_to_fill] = df[columns_to_fill].fillna('Unknown')
```

### 5. Data Filtering

```py
#Removing rows where victim age is greater than 0 and not equal to 120
df_cleaned = df[(df['Vict Age']>0) & (df['Vict Age'] != 120) & (df['LAT'] != 0)]
```

### 6. Data Standardization
```py
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
```
```py
#Removing time from dates

df_cleaned['Date Occurred'] = pd.to_datetime(df_cleaned['Date Occurred'], format='%m/%d/%y %I:%M %p').dt.date
df_cleaned['Date Reported'] = pd.to_datetime(df_cleaned['Date Reported'], format='%m/%d/%y %I:%M %p').dt.date
```

```py
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
```

```py
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
```

```py
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
```
```py
#Standardizing the time occurred column values

df_cleaned['Time Occurred'] = df_cleaned['Time Occurred'].astype(str).str.zfill(4)

def time_fixer(time):
    return f'{time[:2]}:{time[2:]}'

df_cleaned['Time Occurred'] = df_cleaned['Time Occurred'].apply(time_fixer)
df_cleaned['Time Occurred'] = pd.to_datetime(df_cleaned['Time Occurred'], format='%H:%M').dt.strftime('%I:%M %p')
```

### 7. Data Exploration

```py
#Creating a column which shows the total amount of days that passed between the day the crime was committed, and the day it was reported.
df_cleaned['Days Elapsed'] = (pd.to_datetime(df_cleaned['Date Reported']) - pd.to_datetime(df_cleaned['Date Occurred'])).dt.days

#Creating Year, Quarter, Month columns
df_cleaned['Year'] = pd.to_datetime(df_cleaned['Date Occurred']).dt.year
df_cleaned['Quarter'] = pd.to_datetime(df_cleaned['Date Occurred']).dt.quarter
df_cleaned['Month'] = pd.to_datetime(df_cleaned['Date Occurred']).dt.month_name()
```
```py
#General view of weapons used in crimes
df_cleaned['Weapon Used'].value_counts().sort_values().plot(kind='barh')
plt.title('Weapons Used')
plt.ylabel('')
plt.xlabel('# of crimes')
plt.show()
```
![output](https://github.com/user-attachments/assets/829bb977-400b-4df2-87f1-0021846e299a)

```py

#Plotting weapons used in crimes without outliers
df_filtered = df_cleaned[~df_cleaned['Weapon Used'].isin(['Unknown', 'Other Weapons'])]

df_filtered['Weapon Used'].value_counts().sort_values().plot(kind='barh', figsize=(10,6))
plt.xlabel('Number of Crimes')
plt.ylabel('')
plt.title('Weapons Used (Excluding Unknown & Other)')
plt.show()
```
![output](https://github.com/user-attachments/assets/6341c17a-5d53-44fe-b34d-235fec6415c5)

```py
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
```
![output](https://github.com/user-attachments/assets/920a5422-8b90-4163-abb2-097ce8c3f6ba)

```py
#Plotting crimes by victim gender
df_cleaned['Victim Sex'].value_counts().plot(kind='pie',autopct='%1.1f%%')
plt.title('Total Crimes per Gender')
plt.ylabel('')
plt.show()
```
![output](https://github.com/user-attachments/assets/5a663d06-18cc-4ff6-83b9-b32b0b28edfa)

```py
#Plotting crimes count by area
df_cleaned['Area Name'].value_counts().head(10).sort_values().plot(kind='barh',)
plt.title('Top 10 areas of Crime')
plt.xlabel('')
plt.ylabel('')
plt.show()
```
![output](https://github.com/user-attachments/assets/d565c14a-1a3b-47ab-8fbf-2c7565ef12f0)

```py
#Creating a list to sort months in order
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Convert 'Month' column to a categorical type with the correct order
df_cleaned["Month"] = pd.Categorical(df_cleaned["Month"], categories=month_order, ordered=True)

#Creating a pivot
years_and_months_df = df_cleaned.pivot_table(
    index="Month",
    values="Victim Age",
    columns="Year",
    aggfunc="count",
    observed=True
)

#Creating a plot for crime per year
years_and_months_df = years_and_months_df.sort_index()
years_and_months_df.plot()
plt.xlabel('')
plt.show()
```
![output](https://github.com/user-attachments/assets/9eed32c7-3a13-418d-abf2-075d03373909)

```py
#Creating a dataframe to showcase total crimes per year
years_df = df_cleaned['Year'].value_counts().sort_index()
years_df.plot(marker='o')
plt.title('Crimes Reported by Year')
plt.xlabel('')
plt.grid(True)

plt.show()
```
![output](https://github.com/user-attachments/assets/5eb15c98-8ee2-4522-bc4a-fc76b3cbdd67)

## Report

## Top 10 Crimes
```
BATTERY - SIMPLE ASSAULT                                    73,429
BURGLARY FROM VEHICLE                                       61,449
THEFT OF IDENTITY                                           61,280
ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT              51,406
THEFT PLAIN - PETTY ($950 & UNDER)                          46,783
VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)     46,247
INTIMATE PARTNER - SIMPLE ASSAULT                           45,981
BURGLARY                                                    39,711
THEFT FROM MOTOR VEHICLE - GRAND ($950.01 AND OVER)         35,073
THEFT-GRAND ($950.01 & OVER)EXCPT,GUNS,FOWL,LIVESTK,PROD    27,615
```

## Top 10 Areas with Highest Crime
```
Central        51887
Southwest      47679
77th Street    46051
Pacific        42118
Hollywood      39003
Southeast      36376
N Hollywood    36060
Olympic        36007
Wilshire       35623
Topanga        34311
```

## Victim Age Statistics
```
count    732958.000000
mean         39.503826
std          15.570000
min           2.000000
25%          28.000000
50%          37.000000
75%          50.000000
max          99.000000
```

## Most Used Weapons in Crimes
```
Unknown             43,3235
Other Weapons       230,151
Firearms             34,801
Bladed Weapons       19,475
Blunt Objects        11,567
Chemical Weapons      3,674
Explosives               55
```

## Case Resolution Status
```
Invest Cont     56,3361
Adult Other      99,604
Adult Arrest     65,988
Juv Arrest        2,468
Juv Other         1,532
UNK                   5
```

## Yearly Crime Trend
```
Year
2020    150,530
2021    158,225
2022    179,166
2023    168,684
2024     76,353
```

## Monthly Crime Trend
```
Month
April        61,338
August       60,458
December     56,968
February     63,819
January      69,010
July         60,914
June         58,956
March        65,040
May          60,156
November     56,872
October      60,845
September    58,582
```

## Quarterly Crime Trend
```
Quarter
1    197,869
2    180,450
3    179,954
4    174,685
```
## Conclusion

Crime in LA is widespread, with assaults and theft-related crimes being predominant. Certain areas experience higher crime rates, indicating potential hotspots for law enforcement focus. The high number of unresolved cases suggests a need for improved investigative measures. Demographic data shows that crime affects individuals of various ages and ethnic backgrounds, emphasizing the importance of targeted prevention strategies, tha being said, the amount of crime has been declining over the years, which is a good sign.

If you have any questions or feedback, feel free to get in touch!
