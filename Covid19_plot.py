import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select
from bokeh.models import HoverTool, Label, LabelSet
from bokeh.io import curdoc
from bokeh.layouts import row

# Improt files
expose = pd.read_csv(r'/Users/richardtsai/Documents/DataScience/Covid19_job_risks/Exposed_to_Disease_or_Infections.csv',encoding='gbk')
expose.head() #context, code, occupation 
expose.shape #(968,3)

physical = pd.read_csv('/Users/richardtsai/Documents/DataScience/Covid19_job_risks/Physical_Proximity.csv')
physical.head()
physical.shape #(967,3)

temp_df = pd.merge(expose,physical,on=['Code','Occupation'])
temp_df.head()
temp_df.columns=['Expose_frequency','Code','Occupation','Physical_proximity']
temp_df.head()

df_25 = temp_df.loc[:24,:]
df_25.shape

# Input Chinese translation 
ocu_TW=['急診護理師','口腔衛生師','家庭醫師','內科醫師','急重症護理師','專責一般醫療主治醫師','口腔外科醫師','呼吸治療師','呼吸治療技術員',
  '麻醉醫師助理','職能治療師助理','醫院勤務員','牙醫助理','醫事檢驗師','麻醉護理師','泌尿科醫師','過敏免疫科醫師','牙醫師','放射治療師',
  '護理師','執業護士','婦產科醫師','運動醫學科醫師','皮膚科醫師','核醫醫事技術師']

# change expose  to int64 
df_25['Expose_frequency']=df_25['Expose_frequency'].astype('int64')

# Pick 25
df_25['Occupation_TW'] = ocu_TW

# Start plotting 
source = ColumnDataSource(df_25)
source.data  
p = figure(x_axis_label='暴露疾病頻率', y_axis_label='與人接近距離')
p.circle('Expose_frequency',
           'Physical_proximity',
            size=10,fill_alpha=0.2, source=source, fill_color='gray', hover_fill_color='firebrick', hover_line_color="firebrick", line_color=None)
hover = HoverTool(tooltips=[('職業','@Occupation_TW'),('暴露於疾病指數','@Expose_frequency'),('與人接近距離指數','@Physical_proximity')])
p.add_tools(hover)


# Define a callback function 
def update_plot(attr, old, new):
    if new == select.value :
       old_choice=df_25[df_25['Occupation_TW']==old]  
       p.circle(old_choice['Expose_frequency'],old_choice['Physical_proximity'],size=10,fill_alpha=1,fill_color='Gray', line_color=None )
       
       choice=df_25[df_25['Occupation_TW']==select.value]
       a=choice['Expose_frequency']
       b=choice['Physical_proximity']
       p.circle(a,b,size=10,fill_alpha=1,fill_color='blue' )
       
       #Add label 
       citation=Label(x=98,y=98, 
            text='text', 
            border_line_color='black', border_line_alpha=1.0,
            background_fill_color='white', background_fill_alpha=1.0)
    p.add_layout(citation)   

# Add Select 
select = Select(title='Occupation', options=ocu_TW)

# Attach the update_plot callback to the 'value' property of select
select.on_change('value', update_plot)

#layout 
layout = row(p, select)

# Add the plot to the current document
curdoc().add_root(layout)

