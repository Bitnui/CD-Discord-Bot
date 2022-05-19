import pandas as pd 

def clean_restock_report():
    df = pd.read_csv("restock_report.csv")
    df = df.drop([
        "Country",
        "Merchant SKU",
        "ASIN",
        "Condition",
        "Supplier",
        "Supplier part no.",
        "Currency code",
        "Sales last 30 days",
        "Customer Order",
        "Unfulfillable",
        "Working",
        "Shipped",
        "Receiving",
        "Fulfilled by",
        "Total Units",
        "Inbound",
        "Available",
        "FC transfer",
        "FC Processing",
        "Total Days of Supply (including units from open shipments)",
        "Days of Supply at Amazon Fulfillment Network",
        "Alert",
        "Recommended replenishment qty",
        "Recommended ship date",
        "Recommended action"
    ],axis=1)
    #df['Units Sold Last 30 Days'] = df['Units Sold Last 30 Days'].str.replace(',', '').astype(float)
    df.to_csv('FNSKU.csv')
clean_restock_report()
def clean_business_report():
    df = pd.read_csv("business_report.csv")
    # Get Units ordered & ASIN (All thats needed) -- Update cleaned_restock
    df = df.drop([
        "(Parent) ASIN",
        "Title",
        "SKU",
        "Sessions - Total",
        "Session Percentage - Total",
        "Page Views - Total",
        "Page Views Percentage - Total",
        "Featured Offer (Buy Box) Percentage",
        "Units Ordered - B2B",
        "Unit Session Percentage",
        "Unit Session Percentage - B2B",
        "Ordered Product Sales",
        "Ordered Product Sales - B2B",
        "Total Order Items",
        "Total Order Items - B2B"
    ], axis=1)
    #Change top ones 
    df['Units Ordered'] = df['Units Ordered'].str.replace(',', '').astype(float)
    df.to_csv("Cleaned_Business_Report.csv")

def clean_yearly_business_report():
    df = pd.read_csv("yearly_business_report.csv")
    # Get Units ordered & ASIN (All thats needed) -- Update cleaned_restock
    df = df.drop([
        "(Parent) ASIN",
        "SKU",
        "Sessions - Total",
        "Session Percentage - Total",
        "Page Views - Total",
        "Page Views Percentage - Total",
        "Featured Offer (Buy Box) Percentage",
        "Units Ordered - B2B",
        "Unit Session Percentage",
        "Unit Session Percentage - B2B",
        "Ordered Product Sales - B2B",
        "Total Order Items",
        "Total Order Items - B2B"
    ], axis=1)
    #Change top ones 
    df['Ordered Product Sales'] = df['Ordered Product Sales'].str.replace('$', '')
    df['Ordered Product Sales'] = df['Ordered Product Sales'].str.replace(',', '')
    df['Units Ordered'] = df['Units Ordered'].str.replace(',', '')
    df.to_csv("Cleaned_yearly_Business_Report.csv")

def get_duplicates():
    # Replace duplicates and add total
    df = pd.read_csv('Cleaned_Business_Report.csv')
    z = df.loc[df['(Child) ASIN'].duplicated(), :]
    z.to_csv('Duplicates.csv')
    #clean Cleaned_Busines_Report to delete duplicates
    cleaner = df.drop_duplicates(subset=['(Child) ASIN'])
    #cols=[0,1,2]
    #cleaner.drop(df.columns[cols],axis=1,inplace=True)
    cleaner.to_csv('Cleaned_Business_Report.csv')

def get_yearly_duplicate():
    df = pd.read_csv('Cleaned_yearly_Business_Report.csv')
    z = df.loc[df['(Child) ASIN'].duplicated(), :]
    z.to_csv('Duplicates_yearly.csv')
    #clean Cleaned_Busines_Report to delete duplicates
    cleaner = df.drop_duplicates(subset=['(Child) ASIN'])
    #cols=[0,1,2]
    #cleaner.drop(df.columns[cols],axis=1,inplace=True)
    cleaner.to_csv('Cleaned_yearly_Business_Report.csv')

def filter_by_kw(kw):
    df = pd.read_csv('FNSKU.csv')
    #Filter Further (ONly single melt)
    df = df.loc[df['Price'] == 5.99]
    df.sort_values(by=['Units Sold Last 30 Days'],inplace=True, ascending=False)
    df = df[df['Product Name'].str.contains(f'(?i){kw}')]
    df.to_csv(f'{kw}_data.csv')
    # Prints out all filters to CSV

def filter_by_kw_sales(kw):
    df = pd.read_csv('final2.csv')
    df = df[df['Product Name'].str.contains(f'(?i){kw}')]
    df.to_csv(f'{kw}_data.csv')
    # Prints out all filters to CSV

def filter_by_kw_sales_yearly(kw):
    df = pd.read_csv('Combined_Duplicates_yearly.csv')
    df = df[df['Title'].str.contains(f'(?i){kw}')]
    df.to_csv(f'{kw}_data.csv')
    # Prints out all filters to CSV

def filter_colors(kw):
    df = pd.read_csv('color_guide.csv')
    df = df[df['Name'].str.contains(f'(?i){kw}')]
    df.to_csv(f'{kw}_data.csv')

def combine_duplicates():
    # Comine Duplicates and Cleaned_business_report.csv
    df1 = pd.read_csv('Duplicates.csv')
    df2 = pd.read_csv('Cleaned_Business_Report.csv')
    
    lol = df1['(Child) ASIN'].tolist()
    lol2 = int(len(lol))
    lol3 = df2['(Child) ASIN'].tolist()
    lol4 = int(len(lol))
    # loop... loop (if match break loop & delete row)... 
    try:
        for i in range(lol4):
            for x in range(lol2):
                if df1['(Child) ASIN'].values[x] == df2['(Child) ASIN'].values[i]:
                    print("match found")
                    print(df1['(Child) ASIN'].values[x])
                    print(df2['(Child) ASIN'].values[i])
                    # Get value of 1 ASIN
                    # Get value of 2 ASIN
                    val1 = df1['Units Ordered'].values[x]
                    val2 = df2['Units Ordered'].values[i]
                    # Set val1+val2 = df2 value
                    df2['Units Ordered'].values[i] = int(val1) + int(val2) 
                    #df1.drop(df1['(Child) ASIN'][x].index)
                    # MAtch found add up df1 Units Ordered + df2 Units Ordered
                    df2.to_csv("Combined_Duplicates.csv")
                    break
                else:
                    pass
    except:
        pass

def combine_yearly_duplicate():
    # Comine Duplicates and Cleaned_business_report.csv
    df1 = pd.read_csv('Duplicates_yearly.csv')
    df2 = pd.read_csv('Cleaned_yearly_Business_Report.csv')
    
    lol = df1['(Child) ASIN'].tolist()
    lol2 = int(len(lol))
    lol3 = df2['(Child) ASIN'].tolist()
    lol4 = int(len(lol))
    # loop... loop (if match break loop & delete row)... 
    try:
        for i in range(lol4):
            for x in range(lol2):
                if df1['(Child) ASIN'].values[x] == df2['(Child) ASIN'].values[i]:
                    print("match found")
                    print(df1['(Child) ASIN'].values[x])
                    print(df2['(Child) ASIN'].values[i])
                    # Get value of 1 ASIN
                    # Get value of 2 ASIN
                    val1 = df1['Ordered Product Sales'].values[x]
                    val2 = df2['Ordered Product Sales'].values[i]
                    val3 = df1['Units Ordered'].values[x]
                    val4 = df2['Units Ordered'].values[i]
                    # Set val1+val2 = df2 value
                    df2['Ordered Product Sales'].values[i] = int(val1) + int(val2)
                    df2['Units Ordered'].values[i] = int(val3) + int(val4)
                    #df1.drop(df1['(Child) ASIN'][x].index)
                    # MAtch found add up df1 Units Ordered + df2 Units Ordered
                    df2.to_csv("Combined_Duplicates_yearly.csv")
                    break
                else:
                    pass
    except:
        pass
def final_send():
    # Comine Duplicates and Cleaned_business_report.csv
    df1 = pd.read_csv('Combined_Duplicates.csv')
    df2 = pd.read_csv('restock_report.csv')
    
    lol = df1['(Child) ASIN'].tolist()
    lol2 = int(len(lol))
    lol3 = df2['ASIN'].tolist()
    lol4 = int(len(lol))
    # loop... loop (if match break loop & delete row)... 
    try:
        for i in range(lol4):
            for x in range(lol4):
                if df1['(Child) ASIN'].values[x] == df2['ASIN'].values[i]:
                    print("match found")
                    print(df1['(Child) ASIN'].values[x])
                    print(df2['ASIN'].values[i])
                    # Get value of 1 ASIN
                    # Get value of 2 ASIN
                    val1 = df1['Units Ordered'].values[x]
                    val2 = df2['Units Sold Last 30 Days'].values[i]
                    df2.drop_duplicates(subset=['ASIN'])
                    df2['Units Sold Last 30 Days'].values[i] = val1 
                    break
                else:
                    pass
    except:
        pass
    df2.sort_values(by=['Units Sold Last 30 Days'],inplace=True, ascending=False)
    df2.to_csv("final.csv")

def run_yearly():
	clean_yearly_business_report()
	get_yearly_duplicate()
	combine_yearly_duplicate()
	# COmbined_duplcates.csv is final


def real_sales():
    df = pd.read_csv('final.csv')
    z = df.assign(Real_Sales = lambda x: df['Units Sold Last 30 Days'] * df['Price'])
    z.to_csv('final2.csv')

def sales_csv():
    import os 
    clean_business_report()
    get_duplicates()
    combine_duplicates()
    final_send()
    real_sales()

    os.remove('Cleaned_Business_Report.csv')
    os.remove('Combined_Duplicates.csv')
    os.remove('Duplicates.csv')
    os.remove('final.csv')

#sales_csv() - Use to update 
import discord 
import os 
TOKEN = "TOKEN_HERE"

client= discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    if msg.startswith('!'):
        # Split msg 
        msg = msg[1:]
        alist1 =[]
        sheet = filter_by_kw(msg)
        import pandas as pd 
        df = pd.read_csv(f'{msg}_data.csv')
        x = df['FNSKU'].values
        z = df['Product Name'].values
        # For loop Rewrite
        try:
            for i in range(len(x)):
                alist = f'FNSKU: __**{x[i]}**__ : {z[i]} - {i+1}/{len(x)}'
                alist1.append(alist)
                import time 
                time.sleep(.5)
                await message.channel.send(alist1[i])
        except Exception as e:
            await message.channel.send(e)
        os.remove(f'{msg}_data.csv')
    if msg.startswith('help'):
        ok = "To use you must include a '!' and a scent/name (If it's too many it wont work, you can always retry to get less)"
        await message.channel.send(ok)

    if msg.startswith('$'):
        #Split msg
        msg = msg[1:]
        import pandas as pd 
        alist1= []
        alist2 = []
        sheet = filter_by_kw_sales(msg)
        df = pd.read_csv(f'{msg}_data.csv')
        df.sort_values(by=['Real_Sales'],inplace=True, ascending=False)
        x = df['Real_Sales'].values
        z = df['Product Name'].values
        y = df['Units Sold Last 30 Days'].values
        
        try:   
            # Edit it around
            for i in range(len(x)):
                alist = f'Total *Monthly* **Sales**: $__**{str(x[i])} **__ - Total *Monthly* **Units**: __**{str(y[i])}**__ - {z[i]} - {i+1}/{len(x)}'
                alist1.append(alist)
                import time 
                time.sleep(.5)
                await message.channel.send(alist1[i])
            os.remove(f'{msg}_data.csv')
        except Exception as e:
            await message.channel.send(e)
            os.remove(f'{msg}_data.csv')

    if msg.startswith('#'):
        msg = msg[1:]
        import pandas as pd
        alist1=[]
        df=pd.read_csv('Combined_Duplicates_yearly.csv')
        filter_by_kw_sales_yearly(msg)
        df = pd.read_csv(f'{msg}_data.csv')
        df.sort_values(by=['Ordered Product Sales'],inplace=True,ascending=False)
        x = df['Ordered Product Sales'].values
        z = df['Title'].values
        y = df['Units Ordered'].values

        try:
            for i in range(len(x)):
                alist = f'Total *Yearly* **Sales**: $__**{str(x[i])} **__ - Total *Yearly* **Units**: __**{str(y[i])}**__ - {z[i]} - {i+1}/{len(x)}'
                alist1.append(alist)
                import time 
                time.sleep(.5)
                await message.channel.send(alist1[i])
            os.remove(f'{msg}_data.csv')
        except Exception as e:
            await message.channel.send(e)
            os.remove(f'{msg}_data.csv')

    if msg.startswith('?'):
        msg = msg[1:]
        import pandas as pd
        filter_colors(msg)
        alist1 = []
        df = pd.read_csv(f'{msg}_data.csv')
        x = df['Name'].values 
        z = df['Color'].values
        y = df['Scent'].values
        try:
            for i in range(len(x)):
                alist = f'Name: __**{str(x[i])}**__ Scent: __**{str(y[i])}**__ Color: __**{str(z[i])}**__ - {i+1}/{len(x)}'
                alist1.append(alist)
                import time 
                time.sleep(.5)
                await message.channel.send(alist1[i])
            os.remove(f'{msg}_data.csv')
        except Exception as e:
            await message.channel.send(e)
            os.remove(f'{msg}_data.csv')
        

client.run(TOKEN)