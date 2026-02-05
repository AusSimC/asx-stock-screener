"""
ASX 300 Ticker List
This file contains the tickers for ASX300 companies.

Note: The ASX300 composition changes quarterly. This list should be updated periodically.
You can get the latest list from sources like:
- https://www2.asx.com.au/markets/trade-our-cash-market/directory
- Wikipedia: List of S&P/ASX 300 companies
- Financial data providers
"""

# Full ASX 300 list (you'll need to populate this with actual tickers)
# For now, here's a substantial starting list of major ASX stocks

ASX300_TICKERS_EXTENDED = [
    # ASX 20 (largest companies)
    'BHP.AX',   # BHP Group
    'CBA.AX',   # Commonwealth Bank
    'CSL.AX',   # CSL Limited
    'NAB.AX',   # National Australia Bank
    'WBC.AX',   # Westpac Banking
    'ANZ.AX',   # ANZ Banking
    'WES.AX',   # Wesfarmers
    'MQG.AX',   # Macquarie Group
    'FMG.AX',   # Fortescue Metals
    'WDS.AX',   # Woodside Energy
    'RIO.AX',   # Rio Tinto
    'WOW.AX',   # Woolworths
    'GMG.AX',   # Goodman Group
    'TCL.AX',   # Transurban Group
    'TLS.AX',   # Telstra
    'REA.AX',   # REA Group
    'COL.AX',   # Coles Group
    'ALL.AX',   # Aristocrat Leisure
    'STO.AX',   # Santos
    'QBE.AX',   # QBE Insurance
    
    # ASX 21-50
    'WTC.AX',   # WiseTech Global
    'S32.AX',   # South32
    'RMD.AX',   # ResMed
    'IAG.AX',   # Insurance Australia Group
    'AMP.AX',   # AMP Limited
    'ORG.AX',   # Origin Energy
    'AGL.AX',   # AGL Energy
    'SUN.AX',   # Suncorp Group
    'JHX.AX',   # James Hardie
    'CPU.AX',   # Computershare
    'QAN.AX',   # Qantas Airways
    'NCM.AX',   # Newcrest Mining
    'SHL.AX',   # Sonic Healthcare
    'COH.AX',   # Cochlear
    'LLC.AX',   # Lendlease
    'SCG.AX',   # Scentre Group
    'ASX.AX',   # ASX Limited
    'MIN.AX',   # Mineral Resources
    'WOR.AX',   # Worley
    'ALX.AX',   # Atlas Arteria
    'GPT.AX',   # GPT Group
    'MGR.AX',   # Mirvac Group
    'DXS.AX',   # Dexus
    'APA.AX',   # APA Group
    'ORI.AX',   # Orica
    'AMC.AX',   # Amcor
    'AWC.AX',   # Alumina
    'BXB.AX',   # Brambles
    'DOW.AX',   # Downer EDI
    'EVN.AX',   # Evolution Mining
    
    # ASX 51-100
    'ALD.AX',   # Ampol
    'CHC.AX',   # Charter Hall Group
    'CAR.AX',   # Carsales.com
    'SEK.AX',   # Seek Limited
    'WPL.AX',   # Woodside Petroleum (now WDS)
    'RHC.AX',   # Ramsay Health Care
    'ILU.AX',   # Iluka Resources
    'IPL.AX',   # Incitec Pivot
    'AZJ.AX',   # Aurizon Holdings
    'BSL.AX',   # BlueScope Steel
    'IGO.AX',   # IGO Limited
    'OZL.AX',   # Oz Minerals
    'NST.AX',   # Northern Star Resources
    'TAH.AX',   # Tabcorp Holdings
    'SGP.AX',   # Stockland
    'TPG.AX',   # TPG Telecom
    'CWY.AX',   # Cleanaway Waste Management
    'ALU.AX',   # Altium
    'NXT.AX',   # NextDC
    'MPL.AX',   # Medibank Private
    'VCX.AX',   # Vicinity Centres
    'IFL.AX',   # Insignia Financial
    'TWE.AX',   # Treasury Wine Estates
    'HVN.AX',   # Harvey Norman
    'BWP.AX',   # BWP Trust
    'CSR.AX',   # CSR Limited
    'JBH.AX',   # JB Hi-Fi
    'WEB.AX',   # Webjet
    'CIA.AX',   # Champion Iron
    'NHF.AX',   # nib Holdings
    
    # ASX 101-200 (add more as needed)
    'A2M.AX',   # The a2 Milk Company
    'ABC.AX',   # Adbri
    'ABP.AX',   # Abacus Property Group
    'AGL.AX',   # AGL Energy
    'AIA.AX',   # Auckland Airport
    'ANN.AX',   # Ansell
    'ARB.AX',   # ARB Corporation
    'AVN.AX',   # Aventus Group
    'BEN.AX',   # Bendigo and Adelaide Bank
    'BOQ.AX',   # Bank of Queensland
    'CGF.AX',   # Challenger
    'CIA.AX',   # Champion Iron
    'CMW.AX',   # Cromwell Property Group
    'CNU.AX',   # Chorus
    'CTD.AX',   # Corporate Travel Management
    'DMP.AX',   # Domino's Pizza
    'EDV.AX',   # Endeavour Group
    'ELD.AX',   # Elders
    'FLT.AX',   # Flight Centre
    'FPH.AX',   # Fisher & Paykel Healthcare
    'GNC.AX',   # GrainCorp
    'GOZ.AX',   # Growthpoint Properties
    'GUD.AX',   # G.U.D. Holdings
    'GWA.AX',   # GWA Group
    'HLS.AX',   # Healius
    'HUB.AX',   # Hub24
    'IEL.AX',   # IDP Education
    'ING.AX',   # Inghams Group
    'IPH.AX',   # IPH Limited
    'IRE.AX',   # Iress
    'JHG.AX',   # Janus Henderson Group
    'LNK.AX',   # Link Administration Holdings
    'LOV.AX',   # Lovisa Holdings
    'LYC.AX',   # Lynas Rare Earths
    'MFG.AX',   # Magellan Financial Group
    'MMS.AX',   # McMillan Shakespeare
    'MPL.AX',   # Medibank Private
    'MTS.AX',   # Metcash
    'NAN.AX',   # Nanosonics
    'NEC.AX',   # Nine Entertainment
    'NSR.AX',   # National Storage REIT
    'NWL.AX',   # Netwealth Group
    'OML.AX',   # oOh!media
    'ORE.AX',   # Orocobre
    'OSH.AX',   # Oil Search (now merged with Woodside)
    'PNI.AX',   # Pinnacle Investment Management
    'PPT.AX',   # Perpetual
    'PRU.AX',   # Perseus Mining
    'PXA.AX',   # PEXA Group
    'RFF.AX',   # Rural Funds Group
    'RRL.AX',   # Regis Resources
    'RSG.AX',   # Resolute Mining
    'SAR.AX',   # Saracen Mineral Holdings
    'SBM.AX',   # St Barbara
    'SDF.AX',   # Steadfast Group
    'SDR.AX',   # SomnoMed
    'SGM.AX',   # Sims Metal Management
    'SGR.AX',   # Star Entertainment Group
    'SIQ.AX',   # Smartgroup Corporation
    'SKI.AX',   # Spark Infrastructure
    'SPK.AX',   # Spark New Zealand
    'STO.AX',   # Santos
    'SUL.AX',   # Super Retail Group
    'SVW.AX',   # Seven Group Holdings
    'SYD.AX',   # Sydney Airport
    'TPM.AX',   # TPG Telecom (merged)
    'VEA.AX',   # Viva Energy Group
    'VOC.AX',   # Vocus Group
    'VRL.AX',   # Village Roadshow
    'VUK.AX',   # Virgin Money UK
    'WHC.AX',   # Whitehaven Coal
    'WOR.AX',   # Worley
]

# Note: This is not the complete ASX300 list
# To get the full current list, you should:
# 1. Visit https://www2.asx.com.au/markets/trade-our-cash-market/directory
# 2. Or use a financial data API
# 3. Or scrape from Wikipedia: https://en.wikipedia.org/wiki/List_of_S%26P/ASX_300_companies

def get_full_asx300_list():
    """
    Returns the full ASX300 ticker list
    In production, this should fetch the current list from a reliable source
    """
    return ASX300_TICKERS_EXTENDED


if __name__ == "__main__":
    tickers = get_full_asx300_list()
    print(f"Total tickers loaded: {len(tickers)}")
    print("\nFirst 20 tickers:")
    for ticker in tickers[:20]:
        print(f"  - {ticker}")
    print("\n...")
    print(f"\nLast 20 tickers:")
    for ticker in tickers[-20:]:
        print(f"  - {ticker}")
