import random
from typing import List

from faker import Faker
import pandas as pd
from tqdm import tqdm

fake = Faker()

#*#*#*#*#*#*#*#*#
# Fake Data
#*#*#*#*#*#*#*#*#
def generate_name_related_or_random_email(names: List[str]):
    work_related = None
    random_float = random.random()
    if random_float < .1:
        first_part_of_email = names[0].lower() + "." + names[1].lower() + (str(random.randint(1,999)) if random_float < .05 else "")
    elif random_float < .2:
        first_part_of_email = names[0].lower() + names[1].lower() + (str(random.randint(1,999)) if random_float < .15 else "")
    elif random_float < .4:
        first_part_of_email = names[0].lower() + names[1].lower()[0]  + (str(random.randint(1,999)) if random_float < .65 else "")
    elif random_float < .75:
        first_part_of_email = names[0].lower()[0] + names[1].lower()[0] + (str(random.randint(1,999)) if random_float < .7499 else "")     
    else:
        work_related = False
        first_part_of_email = fake.word() + (str(random.randint(1,999)) if random_float < .95 else "")
    
    random_float = random.random()
    if work_related == False:
        while random_float >= .85:
            random_float = random.random()
    if random_float < .4:
        new_email = first_part_of_email + "@gmail.com"
    elif random_float < .5:
        new_email = first_part_of_email + "@outlook.com"
    elif random_float < .6:
        new_email = first_part_of_email + "@yahoo.com" 
    elif random_float < .65:
        new_email = first_part_of_email + "@icloud.com"
    elif random_float < .7:
        new_email = first_part_of_email + "@aol.com"
    elif random_float < .72:
        new_email = first_part_of_email + "@ProtonMail.com"
    elif random_float < .74:
        new_email = first_part_of_email + "@Zoho.com"
    elif random_float < .76:
        new_email = first_part_of_email + "@GMX.com"
    elif random_float < .78:
        new_email = first_part_of_email + "@mail.com"
    elif random_float < .85:
        new_email = first_part_of_email + "@mymail.com"
    else:
        new_email = first_part_of_email + f"@{fake.company().replace(' ','').lower()}.com"    
    return new_email

def generate_fake_data(num_entries=10):
    data = []    
    for _ in range(num_entries):
        # Generate random fake data for each field
        name = fake.name()
        street_address = fake.street_address()
        city = fake.city()
        state = fake.state()
        zip_code = fake.zipcode()
        phone_number = fake.phone_number()
        tax_id = fake.ssn()  if random.random() < 0.7 else generate_fake_tax_id()# Use `ssn()` for generating a Tax ID or SSN
        email = generate_name_related_or_random_email(name.split(" "))
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d")  # Date of Birth        
        data.append({
            'Name': name,
            'Street Address': street_address,
            'City': city,
            'State': state,
            'Zip': zip_code,
            'Phone Number': phone_number,
            'Tax ID/SSN': tax_id,
            'Email': email,
            'Date Of Birth': dob
        })
    return data

#*#*#*#*#*#*#*#*#
# Duplicate Additions
#*#*#*#*#*#*#*#*#
def select_changes(try_for_more_natural:bool=True) -> List[str]: 
    if try_for_more_natural: 
        changes_distribution = [80,40,20,40,1,10]
        number_of_changes_distribution = [4096,1024,512,128,16,1] 
    else:
        changes_distribution = [1,1,1,1,1,1]
        number_of_changes_distribution = [1,1,1,1,1,1]
    return random.choices([
        "Address Change","Email Change","Phone Change","Name Change",
        "Date Of Birth Change","ID Change"],
        changes_distribution,
        k = random.choices([1,2,3,4,5,6],number_of_changes_distribution)[0]
    )

def generate_duplicates(df, num_rows=5):
    "Mixed similarities - more realistic"
    new_rows = []
    for _ in tqdm(range(num_rows)):
        column = ""
        new_row = df.sample(n=1)
        selected_changes = select_changes()
        if "Street Address" in selected_changes:
            column = random.choices(["State","City","Street Address"],[1,2,4])
            if column == "State":
                new_row[column] = fake.state()
                if random.random() < 0.95:
                    column = "City"
            if column == "City":
                new_row[column] = fake.city()
                if random.random() < 0.95:
                    column = "Zip"
            if column == "Zip":
                new_row[column] = fake.zipcode()
                if random.random() < 0.99:
                    column = "Street Address"
            if column == "Street Address":
                new_row[column] = fake.street_address()    
        if "ID Change" in selected_changes:
            column = "Tax ID/SSN"
        if column == "Tax ID/SSN":
            if random.random() < 0.95:
                new_row[column] = generate_fake_tax_id()
            else:    
                new_row[column] = fake.ssn() if random.random() > 0.7 else generate_fake_tax_id()
            if random.random() < 0.9999:
                column = "Name"
        if "Date Of Birth Change" in selected_changes:
            column = "Date Of Birth"
        if column == "Date Of Birth":
            new_row[column] = fake.date_of_birth()
            if random.random() > 0.99:
                column = "Name"
        if "Name Change" in selected_changes:
            column = "Name"
        if column == "Name":
            names = new_row[column].iloc[0].split(" ")
            # Last Name Random Changes
            random_float = random.random()
            if random_float < .10:
                new_row[column] = fake.first_name() + " " + " ".join(names[1:]) 
            if random_float < .25:
                if random_float < .11:
                    new_row[column] = new_row[column] + "-" +  fake.last_name()
                elif random_float < .13:
                    new_row[column] = new_row[column] + " " + fake.last_name()
                else:
                    new_row[column] = " ".join(names[:-1]) + " " + fake.last_name()
            else:
                if len(names) == 2:
                    middle_name = fake.first_name()
                    # Middle Initial Only
                    if random_float < .7:
                        middle_name = middle_name[0]
                    new_row[column] = names[0] + " " + middle_name + " " + names[1]
                else:
                    new_row[column] = names[0] + " " + names[1]
            if len(new_row[column].iloc[0].split(" ")) < 2:
                new_row[column] = new_row[column]
            if random.random() > 0.95:
                column = "Email"
        if "Email Change" in selected_changes:
            column = "Email"
        if column == "Email":
            random_float = random.random()
            name_information = new_row["Name"].to_list()[0].split(" ")
            if random_float < .1:
                first_part_of_email = name_information[0].lower() + "." + name_information[1].lower() + (str(random.randint(1,999)) if random_float < .05 else "")
            elif random_float < .2:
                first_part_of_email = name_information[0].lower() + name_information[1].lower() + (str(random.randint(1,999)) if random_float < .15 else "")
            elif random_float < .4:
                first_part_of_email = name_information[0].lower() + name_information[1].lower()[0]  + (str(random.randint(1,999)) if random_float < .65 else "")
            elif random_float < .75:
                first_part_of_email = name_information[0].lower()[0] + name_information[1].lower()[0]     
            else:
                first_part_of_email = fake.word() + (str(random.randint(1,999)) if random_float < .95 else "")

            
            random_float = random.random()
            if random_float < .4:
                new_email = first_part_of_email + "@gmail.com"
            elif random_float < .5:
                new_email = first_part_of_email + "@outlook.com"
            elif random_float < .6:
                new_email = first_part_of_email + "@yahoo.com" 
            elif random_float < .65:
                new_email = first_part_of_email + "@icloud.com"
            elif random_float < .7:
                new_email = first_part_of_email + "@aol.com"
            elif random_float < .72:
                new_email = first_part_of_email + "@ProtonMail.com"
            elif random_float < .74:
                new_email = first_part_of_email + "@Zoho.com"
            elif random_float < .76:
                new_email = first_part_of_email + "@GMX.com"
            elif random_float < .78:
                new_email = first_part_of_email + "@mail.com"
            elif random_float < .85:
                new_email = first_part_of_email + "@mymail.com"
            else:
                new_email = first_part_of_email + f"@{fake.company().replace(" ","_").lower()}.com"
            new_row[column] = new_email
        if "Phone Change" in selected_changes:
            column = "Phone Number"
        if column == "Phone Number":
            new_row[column] = fake.phone_number()
        new_rows.append(new_row.iloc[0].to_list())
    return pd.DataFrame(new_rows,columns=['Name', 'Street Address', 'City', 'State', 'Zip',
       'Phone Number', 'Tax ID/SSN', 'Email', 'Date Of Birth'])

def generate_fake_tax_id():
    # 9 digits starting with a 9
    return "9" + ''.join([str(random.randint(0, 9)) for _ in range(8)])
generate_fake_tax_id()

# Create Some Base Fake Data
# fake_data = generate_fake_data(100000)
# df = pd.DataFrame(fake_data)
# df.to_csv(r"steps\1_fake_data\data\fake_deduplication_data_base.csv",index=False)

# Read From Existing Fake Base Deduplication Data
df = pd.read_csv(r"steps\1_fake_data\data\fake_deduplication_data_base.csv")[:1000]

# Create additional fake data with some potential for overlap (but not a guarantee)
df = pd.concat([df,generate_duplicates(df,1000)],ignore_index=True)
df.to_csv("fake_deduplication_data_v1_small.csv",index=False)