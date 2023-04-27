import handcalcs
from handcalcs.decorator import handcalc
import forallpeople as us
from plotly import graph_objects as go

us.environment('us_customary')
@handcalc()
def prelim_width(Q_all:float,dead_load:float,live_load:float,snow_load:float,wind_load:float):
    area_req = (dead_load*us.kip+live_load*us.kip+snow_load*us.kip+wind_load*us.kip)/(Q_all*(us.kip/1000/us.ft**2))
    return round(area_req.sqrt()/us.ft*us.ft)
@handcalc()
def prelim_thick(col_dim:float):
    return (col_dim*us.inch*1.5)

def footing_geom(col_dim:float,foot_width,foot_thick):
    foot_width = foot_width/us.inch
    foot_thick = foot_thick/us.inch


    col_face = [[-col_dim/2,-col_dim/2,0],
                   [col_dim/2,-col_dim/2,0],
                   [col_dim/2,col_dim/2,0],
                   [-col_dim/2,col_dim/2,0],
                   [-col_dim/2,-col_dim/2,0]]



    bot_foot_face = [[-foot_width/2,-foot_width/2,-foot_thick],
                     [foot_width/2,-foot_width/2,-foot_thick],
                     [foot_width/2,foot_width/2,-foot_thick],
                     [-foot_width/2,foot_width/2,-foot_thick],
                     [-foot_width/2,-foot_width/2,0],
                     [foot_width/2,-foot_width/2,0],
                     [foot_width/2,foot_width/2,0],
                     [-foot_width/2,foot_width/2,0]]

      

    foot_triangles = [[0,1,2],
                     [2,3,0],
                     [0,1,5],
                     [5,4,0],
                     [3,2,6],
                     [6,7,3],
                     [1,2,6],
                     [6,5,1],
                     [0,3,7],
                     [7,4,0],
                     [4,5,6],
                     [6,7,4]]
    
    x_col,y_col,z_col = zip(*col_face)
    x_bot_foot,y_bot_foot,z_bot_foot = zip(*bot_foot_face)
    foot_tri_i,foot_tri_j,foot_tri_k = zip(*foot_triangles)

    fig = go.Figure()


    fig.add_trace(go.Mesh3d(x=x_col,y=y_col,z=z_col))
    fig.add_trace(go.Mesh3d(x=x_bot_foot,y=y_bot_foot,z=z_bot_foot,i=foot_tri_i,j=foot_tri_j,k=foot_tri_k,opacity = 0.3))

    fig.update_layout(
    scene = dict(
        xaxis = dict(nticks=10, range=[-foot_width*0.75,foot_width*0.75],),
                     yaxis = dict(nticks=10, range=[-foot_width*0.75,foot_width*0.75],),
                     zaxis = dict(nticks=10, range=[-foot_width*0.75,foot_width*0.75],),),
    width=700,
    margin=dict(r=20, l=10, b=10, t=10))

    return fig

#handcalc did not work here
#@handcalc()
def max_fact_load(dead_load,live_load,snow_load,wind_load):
    fact_load = max(1.4*dead_load,
               1.2*dead_load+1.6*live_load+0.5*snow_load,
               1.2*dead_load+1.6*snow_load+live_load,
               1.2*dead_load+1.6*snow_load+0.5*wind_load,
               1.2*dead_load+wind_load+live_load+0.5*snow_load,
               0.9*dead_load+wind_load)*us.kip
     
    return fact_load


#Assuming #8 bars are used
#Following ACI 3-18 TABLE 22.6.5.2
#variations for edge and corner columns have not been implemented
@handcalc(override='long')
def two_way_shear(foot_width,foot_thick,col_dim,fact_load,f_c):

    Phi_shear = 0.75
    d_avg = ((foot_thick-3-0.5)+(foot_thick-3-1.5))/2
    shear_trib_area = foot_width**2-(col_dim*us.inch+d_avg)**2
    q_nu = fact_load/(foot_width**2)
    Vu = q_nu*shear_trib_area
    Vu_stress = Vu/(4*(col_dim*us.inch+d_avg)*d_avg)
    lamb_s = min((2/(1+(d_avg/us.inch/10)))**0.5,1)
    beta = 1
    alpha_s = 40
    b_0 = 4*(col_dim*us.inch+d_avg)

    vc = min(4*lamb_s*f_c**0.5,(2+4/beta)*lamb_s*f_c**0.5,(2+(alpha_s*d_avg/b_0)*lamb_s*f_c**0.5))*us.kip/us.inch**2/1000

    return Vu_stress, vc, d_avg, q_nu,Phi_shear

#onewayshear computed d_avg away from face of col
#NO SHEAR REINFORCEMENT


@handcalc(override='long')
def one_way_shear(foot_width,f_c,d_avg,q_nu,col_dim):
    Phi_shear = 0.75
    foot_width = foot_width/us.ft*12*us.inch
    V_c = 2*((f_c)**0.5)*us.kip/1000/us.inch**2*foot_width*d_avg
    V_u = (q_nu/us.ksi*us.kip/us.inch**2)*foot_width*(foot_width/2-col_dim*us.inch/2-d_avg)

    return Phi_shear,V_c,V_u


#Bending computed at the face of the column
#result is in kip-ft
@handcalc(override='long')
def flexure(q_nu,foot_width,col_dim):
    M_u = q_nu*(((foot_width-col_dim*us.inch)/2)/us.inch*us.inch)**2*(foot_width)/2
     

    return M_u


#Assuming phi_mn = 0.9 (will be verified later)
# T = C, 0.85*f_c*b*a = As*f_y
# a = As*f_y/(0.85*f_c*b)
# phi_M_n = M_u = phi_M_n*As*f_y*(d_avg-a/2)
# phi_M_n = M_u = phi_M_n*As*f_y*(d_avg-(As*f_y/0.85*f_c*b)/2)

def flexure_reinf(f_c,f_y,M_u,foot_width,d_avg):
    Phi_flex = 0.9
    M_n = 0
    A_s = 0*us.inch**2
    #A_s = A_s + 8.91*us.inch**2
    #M_n = A_s*f_y*us.kip/1000/(us.inch**2)*(d_avg-((A_s*f_y)/(2*0.85*f_c*foot_width)))*us.ft/(12*us.inch)
    


    while ((Phi_flex*float(M_n))<float(M_u)):
        A_s = A_s + 0.01*us.inch**2
        M_n = A_s*f_y*us.kip/1000/(us.inch**2)*(d_avg-((A_s*f_y)/(2*0.85*f_c*foot_width)))*us.ft/(12*us.inch)
        
        if A_s > 100 :
            break

    return A_s,Phi_flex*M_n,M_u

def rebar_amount(A_s):
    rebars = {'#3':{'diam':0.375*us.inch,'area':0.11*us.inch**2},
              '#4':{'diam':0.5*us.inch,'area':0.2*us.inch**2},
              '#5':{'diam':0.625*us.inch,'area':0.31*us.inch**2},
              '#6':{'diam':0.75*us.inch,'area':0.44*us.inch**2},
              '#7':{'diam':0.875*us.inch,'area':0.6*us.inch**2},
              '#8':{'diam':1*us.inch,'area':0.79*us.inch**2},
              '#9':{'diam':1.128*us.inch,'area':1*us.inch**2},
              '#10':{'diam':1.27*us.inch,'area':1.27*us.inch**2},
              '#11':{'diam':1.41*us.inch,'area':1.56*us.inch**2}}
    
    min_rebar = []
    for i in list(rebars.keys()):
      min_rebar.append(int(float(A_s)/float(rebars[i]['area'])) + (float(A_s)%float(rebars[i]['area'])>0))

    for j in range(len(list(rebars.keys()))):
        rebars[list(rebars.keys())[j]].update({'num_bars':min_rebar[j]})

    return rebars

#@handcalc(override='long')
def prelim_flex_reinf_calcs(A_s,f_c,f_y,M_u,foot_width,d_avg):
    a = (A_s*f_y)/(0.85*f_c*foot_width)/us.inch*us.inch

    if f_c <= 4000:
        beta_1 = 0.85
    elif f_c < 8000:
        beta_1 = 0.85-(0.05*(f_c-4000))/1000
    else:
        beta_1 = 0.65

    c = a/beta_1
    epsilon_t = (0.003/c)*d_avg-0.003 

    if float(epsilon_t) > 0.005:
        Phi_flex_real = 0.9
    elif float(epsilon_t) > 0.002:
        Phi_flex_real = 0.65+(0.25*(epsilon_t-0.002)/(0.003))
    else:
        Phi_flex_real = 0.65



    return a,Phi_flex_real,beta_1

@handcalc(override='long')
def flex_demo(rebars,reb_size,a,Phi_flex_real,f_y,d_avg,beta_1):
    c = a/beta_1
    epsilon_t = (0.003/c)*d_avg-0.003
    Phi_flex_real = Phi_flex_real
    real_A_s = rebars[reb_size]['area']*rebars[reb_size]['num_bars']
    Phi_M_n = Phi_flex_real*real_A_s*f_y*us.kip/1000/(us.inch**2)*(d_avg-(a/2))*us.ft/(12*us.inch)
    return Phi_M_n


#NOT CHECKING FOR MIN REINFORCEMENT OR SPACING REQS
#flexure not working yet, check units
#flexure working, just check the moment and min reinforcement and tensile 0.003

# @handcalc()
# def quadratic(a,b,c):
#     x_1 = (-b + (b**2 - 4*a*c)**0.5) / (2*a)
#     x_2 = (-b - (b**2 - 4*a*c)**0.5) / (2*a)
#     return x_1,x_2

#THIS FUNCTION HAS NOT BEEN CHECKED YET
