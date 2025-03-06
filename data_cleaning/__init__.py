import pandas as pd

##################
# Data
##################
us_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", 
    "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", 
    "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", 
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", 
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", 
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", 
    "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

#*#*#*#*#*#*#*#*#
# Data Cleaning Functions
#*#*#*#*#*#*#*#*#
def clean_phone_numbers(df: pd.core.frame.DataFrame, column: str) -> None:
    df[column] = df[column].str.replace(r"[^0-9x]","",regex=True)

def regularize_us_phone_numbers(
        df: pd.core.frame.DataFrame, 
        phone_column: str, 
        state_column: str) -> None:
    us_mask = df[state_column].isin(us_states) 
    extension_free_numbers = df.loc[us_mask,phone_column].replace(r"x.*","",regex=True)
    # Adding the international extension in front of the us numbers
    add_one_mask = extension_free_numbers.apply(lambda x: len(x)) == 10
    df.loc[(us_mask) & (add_one_mask),phone_column] = "1" + df[us_mask].loc[add_one_mask,"Phone Number"]
    # Removing zeroes at the beginning of the international extension if applicable
    df[phone_column].str.replace(r"0?0(1[0-9]{10})",r"\1",regex=True)