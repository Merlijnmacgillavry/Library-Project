import urllib.request
import calendar

url_template = "https://repository.tudelft.nl/islandora/search?collection=education&f%5B0%5D=mods_originInfo_dateSort_dt%3A%5B{:0>2}-{:0>2}-{:0>2}T00%3A00%3A00Z%20TO%20{:0>2}-{:0>2}-{:0>2}T23%3A59%3A59Z%5D&display=tud_csv"

def getFile(year, month):
    print(f"{year}-{month:0>2}")
    last_day = calendar.monthrange(year, month)[1]
    url = url_template.format(year, month, 1, year, month, last_day)
    filename = f"data/{year}-{month:0>2}.csv"

    urllib.request.urlretrieve(url, filename)


print("1900")
url = url_template.format(1900, 1, 1, 1999, 12, 31)
filename = f"data/1900.csv"
urllib.request.urlretrieve(url, filename)

for year in range(2000, 2023):
    for month in range(1, 12+1):
        getFile(year, month)

print("2023")
url = url_template.format(2023, 1, 1, 2025, 12, 31)
filename = f"data/2023.csv"
urllib.request.urlretrieve(url, filename)
