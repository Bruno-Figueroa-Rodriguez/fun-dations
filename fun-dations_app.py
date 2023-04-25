import streamlit as st
import rc_calcs_and_checks as rc
import forallpeople as us
import matplotlib as plt
from handcalcs.decorator import handcalc
us.environment('us_customary')

st.markdown('Reinforced Concrete Foundation Design (US UNITS)')


in_data = st.sidebar

with in_data:
    dead_load = st.number_input('Dead Load (kip)')
    live_load = st.number_input('Live Load (kip)')
    snow_load = st.number_input('Snow Load (kip)')
    wind_load = st.number_input('Wind Load (kip)')
    col_dim = st.number_input('Column width (inch)')
    depth_footing = st.number_input('Depth of bottom of footing (ft)')
    gamma_soil = st.number_input('Unit weight of Soil (lb/tf^3)')
    Q_all = st.number_input('Allowable soil pressure (psf)',value = 4000)
    f_c = st.number_input('Concrete Compressive strength (psi)',value = 4000)
    gamma_conc = st.number_input('Concrete Unit weight (lb/tf^3)',value = 150)
    f_y = st.number_input('Steel Yield Strength (psi)',value = 60000)

    #aspect_ratio = st.number_input('Footing aspect ratio')
latex_foot_width,foot_width = rc.prelim_width(Q_all,dead_load,live_load,snow_load,wind_load)
latex_foot_thick,foot_thick = rc.prelim_thick(col_dim)
st.latex(latex_foot_width)
st.write(foot_width)
st.latex(latex_foot_thick)
st.write(foot_thick)

st.write(rc.footing_geom(col_dim,foot_width,foot_thick))

fact_load = rc.max_fact_load(dead_load,live_load,snow_load,wind_load)

st.latex('Maximum\:Factored\:Load = ' + str(fact_load))
latex_twowayshear,twowayshear = rc.two_way_shear(foot_width,foot_thick,col_dim,fact_load,f_c)

st.latex(latex_twowayshear)

st.write('Stress due to Two-way shear')
st.write(twowayshear[0])
st.write('Two-way shear capacity')
st.write(twowayshear[1])


st.write(10*us.kip/us.inch**2)

a=1
b=5
c=6
latex_code,vals = rc.quadratic(a,b,c)
st.latex(latex_code)
st.write(vals)