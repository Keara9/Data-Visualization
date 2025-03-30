
import pandas as pd


df = pd.read_excel("Infant Mortality Original.xls")
df

#Delete the rows with metadata
df = df.drop(range(6,11))
df

# delete columns that are not needed
df = df.drop(columns = "2023 [YR2023]")
df = df.drop(columns = "Series Code")
df = df.drop(columns = "Country Code")
df = df.drop(columns = "Country Name")
df

# delete duplicates
df = df.drop_duplicates()
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

df.to_csv("Infant Mortality Cleaned.csv", index = False)


