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
from bokeh.models.renderers import GlyphRenderer

# Improt files
expose = pd.read_csv(r'/Users/richardtsai/Documents/DataScience/Covid19_job_risks/Exposed_to_Disease_or_Infections.csv',encoding='gbk')
expose.head() #context, code, occupation 
expose.shape #(968,3)

physical = pd.read_csv('/Users/richardtsai/Documents/DataScience/Covid19_job_risks/Physical_Proximity.csv')
physical.head()
physical.shape #(967,3)

TW_job = pd.read_excel('/Users/richardtsai/Documents/DataScience/Covid19_Job_risks/Small_Chinese.xlsx',encoding='utf-8')
TW_job.shape #(968,3)
TW_job = TW_job.iloc[:,:2]
TW_job.head()

#Merge
temp_df = pd.merge(expose,physical,on=['Code','Occupation'])
temp_df.head()
temp_df.columns=['Expose_frequency','Code','Occupation','Physical_proximity']
temp_df.head()
full_table = temp_df.merge(TW_job,how='left',on='Code')
full_table.shape #967,5

# Delete Expose frequency for Rock splitter, timing deivce 
full_table = full_table.iloc[:965,:]

# change expose  to int64 
full_table['Expose_frequency']=full_table['Expose_frequency'].astype('int64')
full_table.info()

# Start plotting 
source = ColumnDataSource(full_table) 
p = figure(title="各職業之新型冠狀病毒之風險圖", x_axis_label='暴露疾病頻率', y_axis_label='與人接近距離')
p.circle('Expose_frequency',
           'Physical_proximity', name = 'allcircle',
            size=10,fill_alpha=0.2, source=source, fill_color='gray', hover_fill_color='firebrick', hover_line_color="firebrick", line_color=None)
hover = HoverTool(tooltips=[('職業','@TW_Occupation'),('Occupation','@Occupation'),('暴露於疾病指數','@Expose_frequency'),('與人接近距離指數','@Physical_proximity')])
p.add_tools(hover)

# Define a callback function 
def update_plot(attr, old, new):

       old_choice=full_table[full_table['TW_Occupation']==old]  
       p.circle(old_choice['Expose_frequency'],old_choice['Physical_proximity'],size=10,fill_alpha=1,fill_color='Gray', line_color=None )
       
       choice=full_table[full_table['TW_Occupation']==new]
       a=choice['Expose_frequency']
       b=choice['Physical_proximity']
       p.circle(a,b,size=10,fill_alpha=1,fill_color='blue' )
       
       citation=Label(x=choice.Expose_frequency.item()+0.5,y=choice.Physical_proximity.item()+0.5, 
            text=choice.TW_Occupation.item(), 
            border_line_color=None, border_line_alpha=1.0,
            background_fill_color=None, background_fill_alpha=0,
            text_font_size="8pt", text_align="center")
 
       p.add_layout(citation) 

# Add Select 
select = Select(title='Occupation', options=full_table['TW_Occupation'].tolist(), value='')

# Attach the update_plot callback to the 'value' property of select
select.on_change('value', update_plot)

#layout 
layout = row(p, select)

# Add the plot to the current document
curdoc().add_root(layout)

