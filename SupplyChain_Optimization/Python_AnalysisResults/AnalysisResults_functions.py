
import pandas as pd
import plotly.graph_objs as go

df = pd.DataFrame([['DE',5,2,'rgb(255,0,0)'],['FR',6,3,'rgb(255,255,0)'],['CH',2,8,'rgb(255,0,0)']], columns=['Country','Price','Volume','Color'])

df['Id'] = list(range(1,len(df)+1,1))


fig = go.Figure()

x = 'Volume'
y = 'Price'

df = df.sort_values([y])
df.index = range(1,len(df)+1,1)
x0_i = 0
for i in df.index:
    print(i)

    xend_i = x0_i + df.loc[i,x]
    i_color = df.loc[i,'Color']
    fig.add_trace(go.Scatter(x=[x0_i, xend_i], y=[df.loc[i,y], df.loc[i,y]], fill='tozeroy', fillcolor=i_color)

    x0_i = xend_i

fig.show()



