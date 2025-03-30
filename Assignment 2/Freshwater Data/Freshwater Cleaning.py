

import pandas as pd


df = pd.read_csv("NewZealand Freshwater Original.csv")
df

#Drop the rows with metadata 
df = df.drop(range(8,13))
df

#Drop the columns that are not needed
df = df.drop(columns = "2023 [YR2023]")
df = df.drop(columns = "Series Code")
df = df.drop(columns = "Country Code")
df = df.drop(columns = "Country Name")
df

#drop the years witout data
df = df.drop(columns=[col for col in df.columns if col.startswith(tuple(str(year) for year in range(1960, 1985)))])
df = df.drop(columns=[col for col in df.columns if col.startswith(tuple(str(year) for year in range(2022, 2024)))])
df

# replace .. with NA
df.replace('..', pd.NA, inplace=True)
df

# Transform the data from wide to long format
df_long = df.melt(
    id_vars=["Series Name"], 
    var_name="Year",          
    value_name="Value"       
)

#Convert year to integer
df_long["Year"] = df_long["Year"].str.extract(r"(\d{4})").astype(int)

df = df_long
df


missing_values = df.isnull().sum()  
missing_values


df.to_csv("NewZealand Freshwater cleaned.csv", index=False)


