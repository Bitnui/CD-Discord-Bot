import pandas as pd
import discord 
import os
import time
import requests
def get_color_guide():
    # Import color guide
    url = "GOOGLE_DOCS_URL_HERE"
    r = requests.get(url, allow_redirects=True)
    open('Vital Csvs/color_guide.csv', 'wb').write(r.content)

def clean_csv(columns,csv,final_name):
    # Pass Columns as a list
    # Pass CSV as 'Folder/Filename.csv'
    df = pd.read_csv(csv)
    df = df[columns]
    match csv:
        case 'Vital Csvs/restock_report.csv':
            pass
        case "Vital Csvs/business_report.csv":
            df['Units Ordered'] = df['Units Ordered'].str.replace(',', '').astype(float)
        case "Vital Csvs/yearly_business_report.csv":
            df['Ordered Product Sales'] = df['Ordered Product Sales'].str.replace('$', '')
            df['Ordered Product Sales'] = df['Ordered Product Sales'].str.replace(',', '')
            df['Units Ordered'] = df['Units Ordered'].str.replace(',', '')
    df.to_csv(final_name)
def clean_duplicates(csv,output):
    # Pass CSV as 'Folder/Filename.csv'
    df = pd.read_csv(csv)
    get_duplicates = df.loc[df['(Child) ASIN'].duplicated(), :]
    get_duplicates.to_csv(output)
    drop_dupes = df.drop_duplicates(subset=['(Child) ASIN'])
    drop_dupes.to_csv(f'{csv}')  
def filter_by_kw(kw,csv):
    # KW passed from discord
    # Pass CSV as 'Folder/Filename.csv'
    df = pd.read_csv(csv)
    match csv:
        case 'Created Csvs/FNSKU.csv':
            df = df.loc[df['Price'] == 5.99]
            df.sort_values(by=['Units Sold Last 30 Days'],inplace=True, ascending=False)
            df = df[df['Product Name'].str.contains(f'(?i){kw}')]
            df.to_csv(f'{kw}_data.csv')
        case 'Created Csvs/Combined_Duplicates_yearly.csv':
            df = df[df['Title'].str.contains(f'(?i){kw}')]
            df.to_csv(f'{kw}_data.csv')
        case 'Vital Csvs/color_guide.csv':
            df = df[df['Name'].str.contains(f'(?i){kw}')]
            df.to_csv(f'{kw}_data.csv')
        case _:
            df = df[df['Product Name'].str.contains(f'(?i){kw}')]
            df.to_csv(f'{kw}_data.csv')
def combine_duplicates(csv1,csv2,column1,column2):
    # Pass CSV as 'Folder/Filename.csv'
    # CSV1 combines into CSV2
    # CSV 1 = Duplicates folder
    # CSV 2 = Cleaned Report
    # Column 1 = CSV 1's Match to list
    # Column 2 = CSV 2's Match to list
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)
    try:
        for i in range(len(df1[column1].values)):
            for x in range(len(df1[column1].values)):
                if df1[column1].values[x] == df2[column2].values[i]:
                    print("Match found")
                    print(df1[column1].values[x])
                    print(df2[column2].values[i])
                    match csv1:
                        case 'Created Csvs/Duplicates.csv':
                          val1 = df1['Units Ordered'].values[x]
                          val2 = df2['Units Ordered'].values[i]
                          df2['Units Ordered'].values[i] = int(val1) + int(val2) 
                          
                        case 'Created Csvs/Yearly_Duplicates.csv':
                            val1 = df1['Ordered Product Sales'].values[x]
                            val2 = df2['Ordered Product Sales'].values[i]
                            val3 = df1['Units Ordered'].values[x]
                            val4 = df2['Units Ordered'].values[i]
                            df2['Ordered Product Sales'].values[i] = int(val1) + int(val2)
                            df2['Units Ordered'].values[i] = int(val3) + int(val4)
                            
                        case 'Created Csvs/Combined_Duplicates.csv':
                            val1 = df1['Units Ordered'].values[x]
                            val2 = df2['Units Sold Last 30 Days'].values[i]
                            df2.drop_duplicates(subset=['ASIN'])
                            df2['Units Sold Last 30 Days'].values[i] = val1
                            df2.sort_values(by=['Units Sold Last 30 Days'], inplace=True, ascending=False)
                            
            match csv1:
                case 'Created Csvs/Duplicates.csv':
                    df2.to_csv("Created Csvs/Combined_Duplicates.csv")
                case 'Created Csvs/Yearly_Duplicates.csv':
                    df2.to_csv("Created Csvs/Combined_Duplicates_yearly.csv")
                case 'Created Csvs/Combined_Duplicates.csv':
                    df2.to_csv("Created Csvs/final.csv")
    except:
        pass
def real_sales():
    df = pd.read_csv('Created Csvs/final.csv')
    z = df.assign(Real_Sales = lambda x: df['Units Sold Last 30 Days'] * df['Price'])
    z.to_csv('Created Csvs/final.csv')
def run_CSVs():
    clean_csv(["Product Name", "FNSKU", "Price", "Units Sold Last 30 Days"],"Vital Csvs/restock_report.csv", 'Created Csvs/FNSKU.csv')
    clean_csv(["(Child) ASIN","Units Ordered"], 'Vital Csvs/business_report.csv', 'Created Csvs/Cleaned_Business_Report.csv')
    clean_duplicates('Created Csvs/Cleaned_Business_Report.csv', "Created Csvs/Duplicates.csv")
    clean_csv(["(Child) ASIN","Title","Units Ordered","Ordered Product Sales"], "Vital Csvs/yearly_business_report.csv", "Created Csvs/Cleaned_yearly_Business_Report.csv")
    clean_duplicates('Created Csvs/Cleaned_yearly_Business_Report.csv',"Created Csvs/Yearly_Duplicates.csv")
    combine_duplicates('Created Csvs/Duplicates.csv','Created Csvs/Cleaned_Business_Report.csv','(Child) ASIN','(Child) ASIN')
    combine_duplicates('Created Csvs/Yearly_Duplicates.csv', 'Created Csvs/Cleaned_yearly_Business_Report.csv', '(Child) ASIN', '(Child) ASIN')
    combine_duplicates('Created Csvs/Combined_Duplicates.csv', 'Vital Csvs/restock_report.csv', '(Child) ASIN', 'ASIN')
    real_sales()
run_CSVs() # Uncomment if you don't have CSV's Already in place
# You will need business_report.csv, restock_report.csv,yearly_business_report.csv
def discord_send_message(msg,csv):
    msg = msg[1:]
    place_holder = []
    sheet = filter_by_kw(msg,csv)
    df = pd.read_csv(f'{msg}_data.csv')
    match csv:
        case 'Created Csvs/FNSKU.csv':
            fnsku = df['FNSKU'].values
            name = df['Product Name'].values
            for i in range(len(fnsku)):
                text = f'FNSKU: __**{fnsku[i]}**__ : {name[i]} - {i+1}/{len(fnsku)}'
                place_holder.append(text)
            os.remove(f'{msg}_data.csv')
            return place_holder
        case 'Created Csvs/final.csv':
            sales = df['Real_Sales'].values
            name = df['Product Name'].values
            units = df['Units Sold Last 30 Days'].values
            for i in range(len(sales)):
                text = f'Total *Monthly* **Sales**: $__**{str(sales[i])} **__ - Total *Monthly* **Units**: __**{str(units[i])}**__ - {name[i]} - {i+1}/{len(sales)}'
                place_holder.append(text)
            os.remove(f'{msg}_data.csv')
            return place_holder
        case 'Created Csvs/Combined_Duplicates_yearly.csv':
            sales = df['Ordered Product Sales'].values
            name = df['Title'].values
            units = df['Units Ordered'].values
            for i in range(len(sales)):
                text = f'Total *Yearly* **Sales**: $__**{str(sales[i])} **__ - Total *Yearly* **Units**: __**{str(units[i])}**__ - {name[i]} - {i+1}/{len(sales)}'
                place_holder.append(text)
            os.remove(f'{msg}_data.csv')
            return place_holder
        case 'Vital Csvs/color_guide.csv':
            name = df['Name'].values 
            color = df['Color'].values
            scent = df['Scent'].values
            for i in range(len(name)):
                text = f'Name: __**{str(name[i])}**__ Scent: __**{str(scent[i])}**__ Color: __**{str(color[i])}**__ - {i+1}/{len(name)}'
                place_holder.append(text)
            os.remove(f'{msg}_data.csv')
            return place_holder
client = discord.Client()
TOKEN = "TOKEN_HERE"
@client.event
async def on_ready():
    print(f'{client.user} has connected to discord')
@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return
    if msg.startswith('!'):
        send_this = discord_send_message(msg,'Created Csvs/FNSKU.csv')
        for i in range(len(send_this)):
            time.sleep(.5)
            await message.channel.send(send_this[i])
    if msg.startswith('$'):
        send_this = discord_send_message(msg,'Created Csvs/final.csv')
        for i in range(len(send_this)):
            time.sleep(.5)
            await message.channel.send(send_this[i])
    if msg.startswith('#'):
        send_this = discord_send_message(msg,'Created Csvs/Combined_Duplicates_yearly.csv')
        for i in range(len(send_this)):
            time.sleep(.5)
            await message.channel.send(send_this[i])
    if msg.startswith('?'):
        get_color_guide()
        send_this = discord_send_message(msg,'Vital Csvs/color_guide.csv')
        for i in range(len(send_this)):
            time.sleep(.5)
            await message.channel.send(send_this[i])
client.run(TOKEN)
