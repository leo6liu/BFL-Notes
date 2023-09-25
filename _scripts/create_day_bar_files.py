import os
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from zoneinfo import ZoneInfo

# get api keys from env variables
api_key = os.environ.get("APCA_API_KEY_ID")
secret_key = os.environ.get("APCA_API_SECRET_KEY")

# create alpaca client
stock_client = StockHistoricalDataClient(api_key, secret_key)

# get all tickers as list (tickers from _data/tickers.txt)
tickers = "A AAL AAPL ABBV ABT ACGL ACN ADBE ADI ADM ADP ADSK AEE AEP AES AFL AIG AIZ AJG AKAM ALB ALGN ALK ALL ALLE AMAT AMCR AMD AME AMGN AMP AMT AMZN ANET ANSS AON AOS APA APD APH APTV ARE ATO ATVI AVB AVGO AVY AWK AXON AXP AZO BA BAC BALL BAX BBWI BBY BDX BEN BF.B BG BIIB BIO BK BKNG BKR BLK BMY BR BRK.B BRO BSX BWA BXP C CAG CAH CARR CAT CB CBOE CBRE CCI CCL CDAY CDNS CDW CE CEG CF CFG CHD CHRW CHTR CI CINF CL CLX CMA CMCSA CME CMG CMI CMS CNC COF COO COP COR COST CPB CPRT CPT CRL CRM CSCO CSGP CSX CTAS CTLT CTRA CTSH CTVA CVS CVX CZR D DAL DD DE DFS DG DGX DHI DHR DIS DLR DLTR DOV DOW DPZ DRI DTE DUK DVA DVN DXC DXCM EA EBAY ECL ED EFX EG EIX EL ELV EMN EMR ENPH EOG EPAM EQIX EQR EQT ES ESS ETN ETR ETSY EVRG EW EXC EXPD EXPE EXR F FANG FAST FCX FDS FDX FE FFIV FI FICO FIS FITB FLT FMC FOX FOXA FRT FSLR FTNT FTV GD GE GEHC GEN GILD GIS GL GLW GM GNRC GOOG GOOGL GPC GPN GRMN GS GWW HAL HAS HBAN HCA HD HES HIG HII HLT HOLX HON HPE HPQ HRL HSIC HST HSY HUM HWM IBM ICE IDXX IEX IFF ILMN INCY INTC INTU INVH IP IPG IQV IR IRM ISRG IT ITW IVZ J JBHT JCI JKHY JNJ JNPR JPM K KDP KEY KEYS KHC KIM KLAC KMB KMI KMX KO KR KVUE L LDOS LEN LH LHX LIN LKQ LLY LMT LNC LNT LOW LRCX LUV LVS LW LYB LYV MA MAA MAR MAS MCD MCHP MCK MCO MDLZ MDT MET META MGM MHK MKC MKTX MLM MMC MMM MNST MO MOH MOS MPC MPWR MRK MRNA MRO MS MSCI MSFT MSI MTB MTCH MTD MU NCLH NDAQ NDSN NEE NEM NFLX NI NKE NOC NOV NOW NRG NSC NTAP NTRS NUE NVDA NVR NWL NWS NWSA O ODFL OGN OKE OMC ON ORCL ORLY OTIS OXY PANW PARA PAYC PAYX PCAR PCG PEAK PEG PEP PFE PG PGR PH PHM PKG PLD PM PNC PNR PNW PODD POOL PPG PPL PRU PSA PSX PTC PWR PXD PYPL QCOM QRVO RCL REG REGN RF RHI RJF RL RMD ROK ROL ROP ROST RSG RTX RVTY SBAC SBUX SCHW SHEDG SEE SHW SJM SLB SNA SNPS SO SPG SPGI SRE STE STLD STT STX STZ SWK SWKS SYF SYK SYY T TAP TDG TDY TECH TEL TER TFC TFX TGT TJX TMO TMUS TPR TRGP TRMB TROW TRV TSCO TSLA TSN TT TTWO TXN TXT TYL UAL UDR UHS ULTA UNH UNP UPS URI USB V VFC VICI VLO VMC VRSK VRSN VRTX VTR VTRS VZ WAB WAT WBA WBD WDC WEC WELL WFC WHR WM WMB WMT WRB WRK WST WTW WY WYNN XEL XOM XRAY XYL YUM ZBH ZBRA ZION ZTS AAPL MSFT AMZN NVDA GOOGL GOOG TSLA AVGO ADBE COST PEP CSCO NFLX CMCSA AMD TMUS INTC INTU TXN AMGN AMAT HON QCOM BKNG SBUX ISRG ADP MDLZ GILD LRCX REGN ADI VRTX MU PANW MELI SNPS KLAC PYPL CDNS CHTR MAR CSX ABNB MNST ORLY PDD ASML NXPI WDAY CTAS FTNT LULU MRVL ADSK KDP ODFL PCAR PAYX MCHP CPRT ON MRNA ROST KHC DXCM AZN EXC AEP IDXX SGEN CRWD BIIB BKR TTD CTSH VRSK CEG CSGP EA GFS XEL TEAM FAST GEHC DDOG FANG WBD ANSS DLTR ALGN ILMN ZS EBAY WBA ZM SIRI ENPH JD LCID SPY QQQ IWM DIA"
# tickers = "AAPL MSFT AMZN GOOG NVDA TSLA META"  # shorter list for testing
tickers = tickers.split(" ")

# create start and end dates
start_dt = datetime(2015, 1, 1, 0, 0, 0, tzinfo=ZoneInfo("America/New_York"))
end_dt = datetime(2023, 9, 23, 0, 0, 0, tzinfo=ZoneInfo("America/New_York"))

# create directory
dir_name = "../_data/day/bars"
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# create day bar files for each ticker
for ticker in tickers:
    try:
        print(f"[ INFO ] Pulling day bar data for: {ticker}")
        bars = stock_client.get_stock_bars(
            StockBarsRequest(
                symbol_or_symbols=ticker,
                timeframe=TimeFrame.Day,
                start=start_dt,
                end=end_dt,
            )
        )
        bars = bars.data[ticker]

        # create file
        # print(f"[ INFO ] Writing bar data to file for: {ticker}")
        with open(f"{dir_name}/{ticker}.csv", "w") as f:
            f.write("date,open,high,low,close,volume\n")
            for bar in bars:
                f.write(
                    f"{bar.timestamp.strftime('%Y-%m-%d')},{bar.open:.2f},{bar.high:.2f},{bar.low:.2f},{bar.close:.2f},{int(bar.volume)}\n"
                )
    except Exception as e:
        print(f"[ ERROR ] {ticker} - {e}")
