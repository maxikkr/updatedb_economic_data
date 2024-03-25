import psycopg2
import toml


def addDefaultSpreadsAndRiskPremiums(data):
    cur.execute("SELECT * from country_default_spreads WHERE country = %s", (data["country"], ))
    output = cur.fetchall()
    if output == []:
        print(f"NA: {data['country']}")
        cur.execute("""INSERT INTO country_default_spreads (country, adj_default_spread, equity_risk_premium, country_risk_premium, corporate_tax_rate, moodys_rating,
                  sovereign_cds_spread, datetime) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())""", (data["country"], data["adj_default_spread"], data["equity_risk_premium"], data["country_risk_premium"], data["corporate_tax_rate"],
                   data["moodys_rating"], data["sovereign_cds_spread"]))
    else:
        print(f"Update: {data['country']}")
        cur.execute("""UPDATE country_default_spreads SET adj_default_spread = %s, equity_risk_premium = %s, country_risk_premium = %s, corporate_tax_rate = %s, moodys_rating = %s,
                  sovereign_cds_spread = %s, datetime = NOW() WHERE country = %s""", (data["adj_default_spread"], data["equity_risk_premium"], data["country_risk_premium"], data["corporate_tax_rate"], data["moodys_rating"]
                                                                  , data["sovereign_cds_spread"], data["country"]))
    conn.commit()


def closedb():
    cur.close()
    conn.close()

def getDefaultSpreadsAndRiskPremiums():
    cur.execute("SELECT * from country_default_spreads")
    output = cur.fetchall()
    return output

def getDefaultSpreadsAndRiskPremiumsByCountry(country):
    print(country)
    if country.lower() == "albania":
        cur.execute("SELECT * from country_default_spreads WHERE country = %s", ("albania", ))
    else:
        cur.execute("SELECT * from country_default_spreads WHERE country = %s", (country, ))
    output = cur.fetchone()
    return output

def createDatabase():
    cur.execute("""CREATE TABLE IF NOT EXISTS country_default_spreads (country VARCHAR(255) PRIMARY KEY,
                    adj_default_spread DECIMAL, equity_risk_premium DECIMAL, country_risk_premium DECIMAL, corporate_tax_rate DECIMAL, moodys_rating VARCHAR(19),
                    sovereign_cds_spread DECIMAL, datetime timestamp)""")
    conn.commit()

config = toml.load("config.toml")
conn = psycopg2.connect(host=config["host"], dbname=config["dbname"], user=config["user"], password=config["password"], port=config["port"])
cur = conn.cursor()