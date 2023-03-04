import matplotlib.pyplot as plt
import pandas as pd

def pie_chart(df_grouped: pd.DataFrame):
    plt.close()
    def my_fmt(x):
        return f'{x:.0f}%\n({x*total/100:.0f} GBP)'

    fig = plt.figure(constrained_layout=True, figsize=(8, 5))

    if len(df_grouped) > 0:

        # processsing

        max_items = 5 

        category_sum = []
        for category, rows in df_grouped:
            category_sum.append((sum(rows.values), category))
        sums, labels = zip(*sorted(category_sum, reverse=True))

        total = sum(sums)

        # matplotlib

        # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subfigures.html
        subfigs = fig.subfigures(1, 1)
        # subfigs[0].suptitle('Expenses per category')

        ax = subfigs.subplots(1,1)

        if len(sums) > max_items:
            x = sums[:max_items] + (sum(sums[max_items:]),)
            labels = labels[:max_items] + ("others",)
        else:
            x = sums
            labels = labels

        ax.pie(x, explode=[0.1]*len(x), labels=labels, autopct=my_fmt,
                shadow=True, startangle=90)
        ax.axis('equal')

    return fig
