import streamlit as st
import rc_calcs_and_checks as rc
import forallpeople as us
import matplotlib as plt
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
    gamma_soil = st.number_input('Unit weight of foodint (lb/tf^3)')
    Q_all = st.number_input('Allowable soil pressure (psf)',value = 4000)
    f_c = st.number_input('Concrete Compressive strength (psi)',value = 4000)
    gamma_conc = st.number_input('Concrete Unit weight (lb/tf^3)',value = 150)
    f_y = st.number_input('Steel Yield Strength (psi)',value = 60000)

    #aspect_ratio = st.number_input('Footing aspect ratio')
foot_width = rc.prelim_width(Q_all,dead_load,live_load,snow_load,wind_load)
foot_thick = rc.prelim_thick(col_dim)
st.write(foot_width)
st.write(foot_thick)

st.write(rc.footing_geom(col_dim,foot_width,foot_thick))


st.write(two_way_shear(foot_width,foot_thick,col_dim,dead_load,live_load,snow_load,wind_load,f_c))