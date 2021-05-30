import matplotlib.pyplot as plt
import pandas as pd

def make_graph(dates, healths):
    data = {'date': dates, 'health': healths}
    df = pd.DataFrame(data=data)
    df = df.groupby(by='date').mean()
    print(df)
    # df.plot(x='date', y='health', kind='bar')