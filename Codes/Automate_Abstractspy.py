#%% import required packages
import pandas as pd
import numpy as np

#%%
text_or = '<tr><td class="{}" nowrap>{} {}</td><td class="{}">{}</td><td class="{}"><a href="./Abstracts/{}.html">{}</a></td></tr>'
text_po = '<tr><td class="{}" nowrap>{} {}</td><td class="{}"><a href="./Abstracts/{}.html">{}</a></td></tr>'
with open(r'/Users/mohammad/Documents/GitHub/EL24/ELDIA/Codes/text2.txt') as f:
    poster = f.readlines()
with open(r'/Users/mohammad/Documents/GitHub/EL24/ELDIA/Codes/text_oral.txt') as f:
    oral = f.readlines()
    
#%% read excel file
filename = r'/Users/mohammad/Documents/GitHub/EL24/ELDIA/Abstracts/Website-Presentation-Database-BAK_2024-SpringBreak.xlsx'
data = pd.read_excel(filename).set_index('PID')

#%% abstract table
times = [
    ['11:30', '11:40', '11:50', '12:00', '12:10', '12:20'],
    ['13:45', '13:55', '14:05', '14:15', '14:25', '14:35'],
    ['15:55', '16:05', '16:15', '16:25', '16:35', '16:45']
    ]

times = [['TBA'] * 6] * 3

tables = []
sessions = ['Oral Session 1', 'Oral Session 2', 'Oral Session 3', 'Poster Session 1', 'Poster Session 2']
for j, session in enumerate(sessions):
    table = ''
    subset = data[data['Presentation Session'] == session]
    if j < 3:
        subset = subset = subset.sort_values('Time Slot')
    for i in range(subset.shape[0]):
        if i%2 == 0:
            color = 'gr'
        else:
            color = 'wr'
        temp = subset
        if j < 3:
            table = table + text_or.format(color,
                                        subset.iloc[i]['First Name'],
                                        subset.iloc[i]['Last Name'],
                                        color,
                                        str(data['Time Slot'].loc[subset.index[i]])[:5],
                                        color,
                                        str(subset.index[i]) + '_' + subset.iloc[i]['First Name'],
                                        subset.iloc[i]['Abstract Title'].title()) + ' '
        else:
            table = table + text_po.format(color,
                                        subset.iloc[i]['First Name'],
                                        subset.iloc[i]['Last Name'],
                                        # color,
                                        # time[j][i],
                                        color,
                                        str(subset.index[i]) + '_' + subset.iloc[i]['First Name'],
                                        subset.iloc[i]['Abstract Title'].title()) + ' '
    tables.append(table)

#%%
poster[70+1] = poster[70+1].format(tables[3])
poster[81+1] = poster[81+1].format(tables[4])

with open(r'/Users/mohammad/Documents/GitHub/EL24/ELDIA/abstracts_poster.html', 'w', encoding='utf-8') as f:
        f.writelines(poster)

oral[73+1] = oral[73+1].format(tables[0])
oral[85+1] = oral[85+1].format(tables[1])
oral[97+1] = oral[97+1].format(tables[2])

with open(r'/Users/mohammad/Documents/GitHub/EL24/ELDIA/abstracts_oral.html', 'w', encoding='utf-8') as f:
        f.writelines(oral)
        
#%% abstract details
with open(r'/Users/mohammad/Documents/GitHub/EL24/ELDIA/Codes/abstract_oral.txt') as f:
    text_oral = f.readlines()

with open(r'/Users/mohammad/Documents/GitHub/EL24/ELDIA/Codes/abstract_poster.txt') as f:
    text_poster = f.readlines()

#%% write files
adict = {
    'Oral Session 3': 'Oral Session 3', 
    'Poster Session 2': 'Poster Session 2', 
    'Oral Session 2': 'Oral Session 2',
    'Oral Session 1': 'Oral Session 1', 
    'Poster Session 1': 'Poster Session 1'
    }
for i in range(0, data.shape[0]):
    coauthors = ['-' if pd.isnull(data.iloc[i]['Co Authors']) else data.iloc[i]['Co Authors']][0]
    session = ['../abstracts_oral.html' if data.iloc[i]['Presentation Session'].startswith('Oral') else '../abstracts_poster.html'][0]
    
    if data.iloc[i]['Presentation Session'] in ['Oral Session 3', 'Oral Session 2', 'Oral Session 1']:
        sample = text_oral.copy()
        sample[34+1] = sample[34+1].format(session, adict[data.iloc[i]['Presentation Session']])
        sample[36+1] = sample[36+1].format(data.iloc[i]['Abstract Text'])
    elif data.iloc[i] ['Presentation Session'] in ['Poster Session 1', 'Poster Session 2']:
        sample = text_poster.copy()
        sample[35+1] = sample[35+1].format(session, adict[data.iloc[i]['Presentation Session']])
        sample[37+1] = sample[37+1].format(data.iloc[i]['Abstract Text'])
        if str(data.iloc[i]['Link to PDF']) == 'nan': 
            sample[34+1] = sample[34+1].format("")
        else:
            sample[34+1] = sample[34+1].format(data.iloc[i]['Link to PDF'])
        
    sample[3] = sample[3].format(data.iloc[i]['First Name'])
    sample[25+1] = sample[25+1].format(data.iloc[i]['Abstract Title'].title())
    sample[27+1] = sample[27+1].format(data.iloc[i]['First Name'], data.iloc[i]['Last Name'])
    sample[28+1] = sample[28+1].format(coauthors)
    sample[29+1] = sample[29+1].format(data.iloc[i]['Faculty Advisors'])
    sample[30+1] = sample[30+1].format(data.iloc[i]['Affiliation'])
    
    if str(data.iloc[i]['Link to Video']) == 'nan': 
        sample[33+1] = sample[33+1].format("")
    else:
        sample[33+1] = sample[33+1].format(data.iloc[i]['Link to Video'])
    
    filename = r'/Users/mohammad/Documents/GitHub/EL24/ELDIA/Abstracts/{}_{}.html'.format(data.index[i], data.iloc[i]['First Name'])
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(sample)
# %%
