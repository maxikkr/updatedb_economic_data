from flask import Flask
import db
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route("/")
def start_page():
    return "Folgende Endpoints gibt es: \n/getDefaultSpreadsAndRiskPremiums, /getDefaultSpreadsAndRiskPremiums/<country>"


@app.route("/getDefaultSpreadsAndRiskPremiums")
def getDefaultSpreadsAndRiskPremiums():
    data = db.getDefaultSpreadsAndRiskPremiums()
    json_data = {}
    for i in data:
        adj_default_spread = i[1]
        if adj_default_spread != None:
            adj_default_spread = float(adj_default_spread)
        equity_risk_premium = i[2]
        if equity_risk_premium != None:
            equity_risk_premium = float(equity_risk_premium)
        country_risk_premium = i[3]
        if country_risk_premium != None:
            country_risk_premium = float(country_risk_premium)
        corporate_tax_rate = i[4]
        if corporate_tax_rate != None:
            corporate_tax_rate = float(corporate_tax_rate)
        moodys_rating = i[5]
        if moodys_rating == None:
            moodys_rating = "Not ranked"
        sovereign_cds_spread = i[6]
        if sovereign_cds_spread != None:
            sovereign_cds_spread = float(sovereign_cds_spread)
        datetime = i[7]
        answer = {
                    "adj_default_spread": adj_default_spread,
                    "equity_risk_premium": equity_risk_premium,
                    "country_risk_premium": country_risk_premium,
                    "corporate_tax_rate": corporate_tax_rate,
                    "moodys_rating": moodys_rating,
                    "sovereign_cds_spread": sovereign_cds_spread,
                    "datetime": datetime,
                }

        json_data[i[0]] = answer
    return json_data

@app.route("/getDefaultSpreadsAndRiskPremiums/<country>")
def getDefaultSpreadsAndRiskPremiumsByCountry(country):
    print(country)
    data = db.getDefaultSpreadsAndRiskPremiumsByCountry(country)
    json_data = {}
    adj_default_spread = data[1]
    if adj_default_spread != None:
        adj_default_spread = float(adj_default_spread)
    equity_risk_premium = data[2]
    if equity_risk_premium != None:
        equity_risk_premium = float(equity_risk_premium)
    country_risk_premium = data[3]
    if country_risk_premium != None:
        country_risk_premium = float(country_risk_premium)
    corporate_tax_rate = data[4]
    if corporate_tax_rate != None:
        corporate_tax_rate = float(corporate_tax_rate)
    moodys_rating = data[5]
    if moodys_rating == None:
        moodys_rating = "Not ranked"
    sovereign_cds_spread = data[6]
    if sovereign_cds_spread != None:
        sovereign_cds_spread = float(sovereign_cds_spread)
    datetime = data[7]
    answer = {
                "adj_default_spread": adj_default_spread,
                "equity_risk_premium": equity_risk_premium,
                "country_risk_premium": country_risk_premium,
                "corporate_tax_rate": corporate_tax_rate,
                "moodys_rating": moodys_rating,
                "sovereign_cds_spread": sovereign_cds_spread,
                "datetime": datetime,
            }

    json_data[data[0]] = answer
    print(json_data)
    return json_data
if __name__ == "__main__":
    db.createDatabase()
    app.run()
    #http_server = WSGIServer(('', 80), app)
    #http_server_serve_forever()

