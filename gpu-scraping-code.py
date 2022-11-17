from bs4 import BeautifulSoup
import requests
import re

urls = [ # List with all urls.
    'https://www.amazon.es/Gigabyte-GV-N3090GAMING-OC-24GD-Tarjeta-gr%C3%A1fica/dp/B08HLYQ9XL/ref=sr_1_4?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1OJ9JEU2ELL6L&keywords=rtx+3090&qid=1668684618&qu=eyJxc2MiOiI2LjE5IiwicXNhIjoiNS4yMiIsInFzcCI6IjQuNjQifQ%3D%3D&sprefix=rtx+3090%2Caps%2C72&sr=8-4',
    'https://www.amazon.es/ZOTAC-ZT-A30810D-10P-Tarjeta-gr%C3%A1fica-GeForce/dp/B0968MBC3R/ref=sr_1_10?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=ATSZPKMTT1SO&keywords=tarjeta+gr%C3%A1fica&qid=1668684322&qu=eyJxc2MiOiI3LjY1IiwicXNhIjoiNi44OCIsInFzcCI6IjQuNTAifQ%3D%3D&refinements=p_72%3A831280031%2Cp_36%3A1323860031&rnid=1323854031&s=computers&sprefix=tarjeta+gr%C3%A1fica%2Caps%2C86&sr=1-10',
    'https://www.amazon.es/Gigabyte-Technology-GV-N307TGAMING-OC-8GD-Tarjeta/dp/B095X6RLJW/ref=sr_1_2?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2W89ZFU39X87B&keywords=3070+ti&qid=1668684431&qu=eyJxc2MiOiI1LjM1IiwicXNhIjoiMy45NCIsInFzcCI6IjMuMTcifQ%3D%3D&s=computers&sprefix=3070+ti%2Ccomputers%2C75&sr=1-2',
    'https://www.amazon.es/PNY-Tarjeta-gr%C3%A1fica-GeForce-UPRISING/dp/B0971YSVS3/ref=sr_1_11?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=ATSZPKMTT1SO&keywords=tarjeta+gr%C3%A1fica&qid=1668684322&qu=eyJxc2MiOiI3LjY1IiwicXNhIjoiNi44OCIsInFzcCI6IjQuNTAifQ%3D%3D&refinements=p_72%3A831280031%2Cp_36%3A1323860031&rnid=1323854031&s=computers&sprefix=tarjeta+gr%C3%A1fica%2Caps%2C86&sr=1-11',
    'https://www.amazon.es/MSI-Radeon-6650-Mech-Velocidad/dp/B09YHXT12P/ref=sr_1_1?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=36CA57X3D8TEB&keywords=amd+tarjeta+gr%C3%A1fica+rx&qid=1668684457&qu=eyJxc2MiOiIxLjgwIiwicXNhIjoiMC4wMCIsInFzcCI6IjAuMDAifQ%3D%3D&refinements=p_72%3A831280031%2Cp_36%3A1323860031&rnid=1323854031&s=computers&sprefix=amd+tarjeta+gr%C3%A1fica+rx%2Ccomputers%2C65&sr=1-1',
    'https://www.amazon.es/PowerColor-Fighter-AMD-Radeon-6700/dp/B08Y91QVG8/ref=sr_1_2?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=36CA57X3D8TEB&keywords=amd+tarjeta+gr%C3%A1fica+rx&qid=1668684457&qu=eyJxc2MiOiIxLjgwIiwicXNhIjoiMC4wMCIsInFzcCI6IjAuMDAifQ%3D%3D&refinements=p_72%3A831280031%2Cp_36%3A1323860031&rnid=1323854031&s=computers&sprefix=amd+tarjeta+gr%C3%A1fica+rx%2Ccomputers%2C65&sr=1-2',
    'https://www.amazon.es/Asrock-RX6800-PGD-16GO-Tarjeta/dp/B08Q7D4M98/ref=sr_1_3?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=36CA57X3D8TEB&keywords=amd+tarjeta+gr%C3%A1fica+rx&qid=1668684457&qu=eyJxc2MiOiIxLjgwIiwicXNhIjoiMC4wMCIsInFzcCI6IjAuMDAifQ%3D%3D&refinements=p_72%3A831280031%2Cp_36%3A1323860031&rnid=1323854031&s=computers&sprefix=amd+tarjeta+gr%C3%A1fica+rx%2Ccomputers%2C65&sr=1-3',
    'https://www.amazon.es/ASUS-Gaming-TUF-RX6900XT-O16G-GAMING-Radeon-GDDR6/dp/B08BQX8VP3/ref=sr_1_4?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=36CA57X3D8TEB&keywords=amd+tarjeta+gr%C3%A1fica+rx&qid=1668684457&qu=eyJxc2MiOiIxLjgwIiwicXNhIjoiMC4wMCIsInFzcCI6IjAuMDAifQ%3D%3D&refinements=p_72%3A831280031%2Cp_36%3A1323860031&rnid=1323854031&s=computers&sprefix=amd+tarjeta+gr%C3%A1fica+rx%2Ccomputers%2C65&sr=1-4'
]
names = [ # List with custom names. I don't really like using the amazon name and each string has the name in a different position.
    'GTX 3090: ',               #  # We could make a list of possible titles like this and find the substr in the amazon title, but it would make no sense :)
    'GTX 3080 Ti: ',
    'GTX 3070 Ti: ',
    'GTX 3060 Ti: ',
    'RX 6650 XT: ',
    'RX 6700 XT: ',
    'RX 6800 PGD: ',
    '6900 XT OC: '
]
headers = {     # You can find your user-agent here: https://httpbin.org/get
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}

for i in range(len(urls)):  # Main loop that will iterate each GPU in the list.
    url = urls[i]
    name = names[i]         # Since names and urls have the same name, this is the best way to get both.

    page = requests.get(url, headers=headers)   # Get the html file.
    soup1 = BeautifulSoup(page.content, "html.parser")  # Read the html file.
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")  # Give it a json-like format. Useful if you want to debug.
    price = soup2.find(id="corePriceDisplay_desktop_feature_div").get_text()    # Find the desktop price display data.

    price = price.replace('\n',' ')     # Clean line breaks.
    price = re.sub(' +', ' ', price)    # Remove extra spaces.
    lst = price.split()                 # Split the string to find the price.
    for p in lst:
        if "€" in p:    # The fist occurence with "€" is always the price.
            price = p
            break

    print('{}{}'.format(name,price))    # The display. We could save this into a csv file.
print('-----------------------')
