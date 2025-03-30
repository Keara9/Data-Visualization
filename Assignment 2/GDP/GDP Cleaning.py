
import pandas as pd


df = pd.read_csv("GDP original.csv")
df

# Drop rows with metadata
df = df.drop(range(20,25))
#drop columns that are not needed
df = df.drop(columns = "Series Code")
df = df.drop(columns = "Country Code")
df = df.drop(columns = "Country Name")
df

#replace .. with NA
df.replace('..', pd.NA, inplace=True)
df


missing_values = df.isnull().sum()  
missing_values

# Delete yeaer without data
df = df.drop(df.loc['1960 [YR1960]':'1990 [YR1990]'].index)
df


# Transform the data from wide to long format
df_long = df.melt(
    id_vars=["Series Name"],  
    var_name="Year",         
    value_name="Value"        
)

#convert year to int
df_long["Year"] = df_long["Year"].str.extract(r"(\d{4})").astype(int)


df = df_long
df

missing_values = df.isnull().sum()  

missing_values


df.to_csv("GDP cleaned.csv")


