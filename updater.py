from bs4 import BeautifulSoup
import requests
import db
import pandas as pd
import yfinance
import nasdaqdatalink
import cpi


def call_website(url: str) -> str:
    soup = requests.get(url, verify=False)
    soup = BeautifulSoup(soup.text, "html.parser")
    return soup


def getDefaultSpreadsAndRiskPremiums():
    url = "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html"
    content = call_website(url)
    table = content.find("table")
    for tr in table.findAll("tr")[1:-1]:
        td = tr.findAll("td")
        country = td[0].text.replace("""\n                (Principality of)""", ""). \
            replace(" &\n                ", "&").replace("\n                ", " ").replace("'", "").lower()
        adj_default_spread = td[1].text.replace("%", "")
        if adj_default_spread == "NA":
            adj_default_spread = None
        else:
            adj_default_spread = float(adj_default_spread) / 100
        equity_risk_premium = td[2].text.replace("%", "")
        if equity_risk_premium == "NA":
            equity_risk_premium = None
        else:
            equity_risk_premium = float(equity_risk_premium) / 100
        country_risk_premium = td[3].text.replace("%", "")
        if country_risk_premium == "NA":
            country_risk_premium = None
        else:
            country_risk_premium = float(country_risk_premium) / 100
        corporate_tax_rate = td[4].text.replace("%", "")
        if corporate_tax_rate == "NA":
            corporate_tax_rate = None
        else:
            corporate_tax_rate = float(corporate_tax_rate) / 100
        moodys_rating = td[5].text
        if moodys_rating == "NR":
            moodys_rating = None
        sovereign_cds_spread = td[6].text.replace("%", "")
        if sovereign_cds_spread == "NA":
            sovereign_cds_spread = None
        else:
            sovereign_cds_spread = float(sovereign_cds_spread) / 100
        data = {
            "country": country,
            "adj_default_spread": adj_default_spread,
            "equity_risk_premium": equity_risk_premium,
            "country_risk_premium": country_risk_premium,
            "corporate_tax_rate": corporate_tax_rate,
            "moodys_rating": moodys_rating,
            "sovereign_cds_spread": sovereign_cds_spread,
        }
        db.addDefaultSpreadsAndRiskPremiums(data)

#ToDo
def getTBillYield() -> int:
    url = "https://www.worldgovernmentbonds.com/"
    content = call_website(url)
    table = content.find("table", {"class": "homeBondTable sortable w3-table money pd44 -f14"})
    allTr = table.findAll("tr")
    #for tr in allTr:
    #    print(tr)
    tr = allTr[2]
    for td in tr.findAll("td"):
        print(td.find("a"))


def closedbb():
    db.closedb()


if __name__ == "__main__":
    pass
