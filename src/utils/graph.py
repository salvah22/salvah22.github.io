import matplotlib.pyplot as plt
import pandas as pd

def pie_chart(df_grouped: pd.DataFrame, color: str):
    plt.close()
    def my_fmt(x, total):
        return f'{x:.0f}%' + (f"\n({x*total/100:.0f} GBP)" if total else "")

    fig = plt.figure(constrained_layout=True, figsize=(8, 5))
    if color:
        fig.set_facecolor(color)

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

        ax.axis('equal')

        if color:
            ax.set_facecolor(color)

        if len(sums) > max_items:
            x = sums[:max_items] + (sum(sums[max_items:]),)
            labels = labels[:max_items] + ("others",)
        else:
            x = sums
        
        labels = [_[:9]+".." if len(_)>9 else _ for _ in labels]

        text_tuple = ax.pie(x, explode=[0.1]*len(x), labels=labels, autopct=lambda x: my_fmt(x,False), shadow=True, startangle=90)

        for i in range(len(text_tuple[1])):
            text_tuple[1][i].set_color('white')
            text_tuple[2][i].set_color('white')
        

    return fig
