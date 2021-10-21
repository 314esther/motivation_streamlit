import streamlit as st
import math
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import Legend

st.set_page_config(layout='wide')
st.title("Income vs. Motivation")


def calc_scarcity(income):
    #based on annual income figures
    if income <= 20000:
        return 1
    elif income > 20000 and income <= 75000:
        return (15/11)-(income/55000)
    elif income > 75000:
        return 0

def calc_extrinsic_motivation(income, incentive):
    #incentive = calc_incentive(income)
    raw_motivation = calc_scarcity(income)*(incentive/income)
    if raw_motivation >= 1:
        return 1
    else:
        return raw_motivation

def calc_happiness(income, personality):
    #income + personality
    if income <= 20000:
        return 0+(personality*0.5)
    elif income > 20000 and income <= 75000:
        return (income/55000 - (4/11))*0.5+(personality*0.5)
    elif income > 75000:
        return 0.5+(personality*0.5)

incentive = st.sidebar.slider("Incentive", 5000,20000,10000)
stocastic = st.sidebar.checkbox("Make Personality a Stocastic variable")


motivation_data = []
extrinsic_data = []
intrinsic_data = []
for income in range(10000,90000,5000):
	if stocastic:
		personality = np.random.normal(0.5, 0.125, 1)[0]
	else:
		personality = 0.5
	intrinsic_motivation = calc_happiness(income, personality)
	extrinsic_data.append(calc_extrinsic_motivation(income, incentive))
	intrinsic_data.append(intrinsic_motivation)
	motivation_data.append((calc_extrinsic_motivation(income, incentive)+intrinsic_motivation))

p = figure(x_axis_label="income",y_axis_label="motivation", width=700, height=350)

motivation = [motivation_data, extrinsic_data, intrinsic_data]
xs = [list(range(20000,80000,5000)), list(range(20000,80000,5000)), list(range(20000,80000,5000))]

mot = p.line(list(range(10000,90000,5000)), motivation_data, color=(255,0,0))
ext = p.line(list(range(10000,90000,5000)), extrinsic_data, color=(0,255,0))
intr = p.line(list(range(10000,90000,5000)), intrinsic_data, color=(0,0,255))
my_legend = Legend(items=[("Total Motivation" , [mot]), ("Extrinsic Motivation", [ext]), ("Intrinsic Motivation", [intr])])

p.add_layout(my_legend, 'right')

st.bokeh_chart(p)
