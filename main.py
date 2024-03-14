import pandas as pd
from time import sleep
from lightweight_charts import Chart

def convert_df_in_ohlc(df):
    df.columns = ['stock','date','time','open','high','low','close', 'vol', 'iv']
    df['date'] = df['date'].apply(str)
    df['date'] = df['date'] + ' ' + df['time']
    df = df.drop(['stock', 'time', 'iv', 'vol'], axis = 1)
    df['date'] = pd.to_datetime(df['date'])
    df = df.rename(columns={'date':'time'})
    return df

if __name__ == '__main__':

    chart = Chart()

    df1 = pd.read_csv('/Users/pradumnkumar/Desktop/stocks/NSE_Equity_Futures_iEOD/2023/JAN/02JAN/NIFTY.txt')
    df1 = convert_df_in_ohlc(df1)

    df2 = pd.read_csv('/Users/pradumnkumar/Desktop/stocks/NSE_Equity_Futures_iEOD/2023/JAN/03JAN/NIFTY.txt')
    df2 = convert_df_in_ohlc(df2)

    chart.set(df1)

    chart.show()

    print("Provide supports with spaces")
    supports = map(float, input().strip().split())
    for support in supports:
        line = chart.create_line('Support_{}'.format(support))
        support_data = pd.DataFrame({'time':df1['date'], 'Support_{}'.format(support): support})
        line.set(support_data)
    
    for i, series in df2.iterrows():
        bar = pd.Series(dtype='float64')
        if i%5 == 0:
            chart.update(series)
            _last_bar = series
        else:
            bar = _last_bar
            bar['high'] = max(_last_bar['high'], series['close'])
            bar['low'] = min(_last_bar['low'], series['close'])
            bar['price'] = series['close']
            chart.update_from_tick(bar)
        sleep(1)