import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from io import BytesIO
import base64

def make_graph(dates, healths):
    data = {'date': dates, 'health': healths}
    df = pd.DataFrame(data=data)
    df = df.groupby(by='date').mean()
    # plt.ioff()
    plt.figure(figsize=(13, 7))
    plt.plot(linewidth = '50')
    # sns.set_style('whitegrid')
    # sns.set_palette('rainbow')
    plt.ylabel("Healthy Plant % (0-1)")
    sns_plot = sns.lineplot(data=df, markers=True, dashes=False)

    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url
    # df.plot(x='date', y='health', kind='bar')