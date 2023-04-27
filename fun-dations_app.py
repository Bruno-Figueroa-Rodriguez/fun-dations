import streamlit as st
import rc_calcs_and_checks as rc
import forallpeople as us
import matplotlib as plt
from handcalcs.decorator import handcalc
us.environment('us_customary')

st.title('Reinforced Concrete Foundation Design (US UNITS)')


in_data = st.sidebar

with in_data:
    dead_load = st.number_input('Dead Load (kip)',value = 1)
    live_load = st.number_input('Live Load (kip)',value = 1)
    snow_load = st.number_input('Snow Load (kip)')
    wind_load = st.number_input('Wind Load (kip)')
    col_dim = st.number_input('Column width (inch)',value = 24)
    depth_footing = st.number_input('Depth of bottom of footing (ft)')
    gamma_soil = st.number_input('Unit weight of Soil (lb/tf^3)')
    Q_all = st.number_input('Allowable soil pressure (psf)',value = 4000)
    f_c = st.number_input('Concrete Compressive strength (psi)',value = 4000)
    reb_size = st.text_input('Rebar size for footing (i.e #8)',value='#8')
    gamma_conc = st.number_input('Concrete Unit weight (lb/tf^3)',value = 150)
    f_y = st.number_input('Steel Yield Strength (psi)',value = 60000)

    #aspect_ratio = st.number_input('Footing aspect ratio')
st.header('Dimensioning')

latex_foot_width,foot_width = rc.prelim_width(Q_all,dead_load,live_load,snow_load,wind_load)
latex_foot_thick,foot_thick = rc.prelim_thick(col_dim)
st.latex(latex_foot_width)
st.write('footing width = ' + str(foot_width))
st.latex(latex_foot_thick)
st.write('footing thickness = ' +str(foot_thick))

st.write(rc.footing_geom(col_dim,foot_width,foot_thick))

st.header('Calculating loads')

fact_load = rc.max_fact_load(dead_load,live_load,snow_load,wind_load)

st.latex('Maximum\:Factored\:Load = ' + str(fact_load))

st.header('Evaluating two-way shear')

latex_twowayshear,twowayshear = rc.two_way_shear(foot_width,foot_thick,col_dim,fact_load,f_c)

st.latex(latex_twowayshear)

st.latex('Stress\:due\:to\:Two-way\:shear:')
st.latex(twowayshear[0]/(us.kip/us.inch**2)*us.ksi)
st.latex('Two-way\:shear\:stress\:capacity:')
st.latex(twowayshear[1]/(us.kip/us.inch**2)*us.ksi)
d_avg,q_nu = twowayshear[2],twowayshear[3]
q_nu = q_nu/(us.kip/us.ft**2)*us.kip/(12*us.inch)**2/(us.kip/us.inch**2)*us.ksi


if twowayshear[1]*twowayshear[4]>=twowayshear[0]:
    st.latex('Two\:way\:shear\:is\:OK,\:DCR\:=\:'+str(round(twowayshear[0]/(twowayshear[1]*twowayshear[4]),3)))
    
else:
    st.latex('Two\:way\:shear\:FAILS,\:revise\:design,\:DCR\:=\:'+str(round(twowayshear[0]/(twowayshear[1]*twowayshear[4]),3)) )

# st.latex(foot_width)
# st.latex(q_nu)


st.header('Evaluating One-way shear')

latex_onewayshear,onewayshear = rc.one_way_shear(foot_width,f_c,d_avg,q_nu,col_dim)
st.latex(latex_onewayshear)
# st.latex(onewayshear[0])
# st.latex(onewayshear[1])
# st.latex(onewayshear[2])

if onewayshear[0]*onewayshear[1]>=onewayshear[2]:
    st.latex('One\:way\:shear\:is\:OK,\:DCR\:=\:'+str(round(onewayshear[2]/(onewayshear[0]*onewayshear[1]),3)))
else:
    st.latex('One\:way\:shear\:FAILS,\:revise\:design ')

st.header('Evaluating flexure')

latex_flex,M_u = rc.flexure(q_nu,foot_width,col_dim)

st.latex(latex_flex)
#st.latex(M_u)
#st.write(float(M_u))


A_s,Phi_flex_M_n,M_u = rc.flexure_reinf(f_c,f_y,M_u,foot_width,d_avg)

#flex_reinf gives A_s,Phi_flex*M_n,M_u

a,Phi_flex_real,beta_1 = rc.prelim_flex_reinf_calcs(A_s,f_c,f_y,M_u,foot_width,d_avg)


rebars = rc.rebar_amount(A_s)

st.table(rebars)

latex_flex_demo,Phi_M_n = rc.flex_demo(rebars,reb_size,a,Phi_flex_real,f_y,d_avg,beta_1)


st.latex(latex_flex_demo)

if float(Phi_M_n) > float(M_u):
    st.write('Flexure is OKAY, DCR = '+str(float(M_u)/float(Phi_M_n)))
else:
    st.write('Flexure failes, REVISE, DCR = '+str(float(M_u)/float(Phi_M_n)) )


#st.latex(latex_flex_reinf_calcs)

#st.latex('A_s,\:Phi_flex*M_n,\:M_u')
#st.latex(flex_reinf)

# st.write(10*us.ksi)
# st.write(10*us.kip/us.inch**2)


# a=1
# b=5
# c=6   
# latex_code,vals = rc.quadratic(a,b,c)
# st.latex(latex_code)
# st.write(vals)