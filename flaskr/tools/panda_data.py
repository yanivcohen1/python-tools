import pandas as pd

# --------- print utc
print(pd.to_datetime(['2018-10-26 12:00 -0530', '2018-10-26 12:00 -0500'],
                utc=True)[0]) # print in utc: 2018-10-26 17:30:00+00:00

# ------------ panda from csv
csv_file_path = r"D:\pyProj\adi\third_year\proj3\clients_data.csv"
df = pd.read_csv(csv_file_path)
all_ids = df['ID'].astype(str).values
print("heads:",df.columns.tolist())
# print: heads: ['ID', 'Name', 'Phone number', 'Birth year', 'Is Employee']

# ------------ panda from dict
dict1 = {
  "Date": ["2018-10-26", "2018-10-26", "2018-10-27", "2018-10-28", "2018-10-29", "2018-10-29"],
  "Sales": [1000, 1200, 1500, 1800, 2000, 2200],
  "Profit": [200, 300, 400, 500, 600, 700],
  'time': [1, 2, 3],
}
table = pd.DataFrame(dict1, columns=['Date', 'Sales', "Profit"])# option to fillter
table[["Date"]] = table[["Date"]].apply(pd.to_datetime)

# Panda print from colums ['Date', 'Profit'] 3 first rows
print(table[['Date', 'Profit']].head(3))
#         Date  Profit
# 0 2018-10-26     200
# 1 2018-10-26     300
# 2 2018-10-27     400

# ------------ panda from html
url = "https://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list"
df = pd.read_html(url)[0]
print(df.iloc[0:3])
#                               Bank Name          City         State   Cert                Aquiring Institution      Closing Date  Fund  Sort ascending
# 0                   Pulaski Savings Bank       Chicago      Illinois  28611                     Millennium Bank  January 17, 2025                 10548
# 1     The First National Bank of Lindsay       Lindsay      Oklahoma   4134  First Bank & Trust Co., Duncan, OK  October 18, 2024                 10547
# 2  Republic First Bank dba Republic Bank  Philadelphia  Pennsylvania  27332   Fulton Bank, National Association    April 26, 2024                 10546
print("number of rows:" , df.shape[0])
print("number of columns:" , df.shape[1])
# number of rows: 10
# number of columns: 7

# add head to table
# Create a DataFrame without headers
data = [
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9]
]
df = pd.DataFrame(data)
# Add headers
df.columns = ['Column1', 'Column2', 'Column3']
print(df)
#    Column1  Column2  Column3
# 0        1        4        7
# 1        2        5        8
# 2        3        6        9
