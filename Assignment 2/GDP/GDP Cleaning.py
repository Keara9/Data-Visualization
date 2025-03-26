
import pandas as pd


df = pd.read_csv("GDP original.csv")
df


df = df.drop(range(20,25))
df





df.replace('..', pd.NA, inplace=True)
df


missing_values = df.isnull().sum()  
missing_values


df = df.drop(df.loc['1960 [YR1960]':'1990 [YR1990]'].index)
df




# Transform the data from wide to long format
df_long = df.melt(
    id_vars=["Series Name"],  
    var_name="Year",        
    value_name="Value"    
)    

df_long["Year"] = df_long["Year"].str.extract(r"(\d{4})")


#Convert year to in
df_long["Year"] = df_long["Year"].astype(int)

df = df_long


missing_values = df.isnull().sum()  
missing_values
df


df.to_csv("GDP cleaned.csv")


