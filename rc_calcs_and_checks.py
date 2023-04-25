import handcalcs
import forallpeople as us
from plotly import graph_objects as go

us.environment('us_customary')

def prelim_width(Q_all:float,dead_load:float,live_load:float,snow_load:float,wind_load:float):
    prelim_width = (dead_load*us.kip+live_load*us.kip+snow_load*us.kip+wind_load*us.kip)/(Q_all*(us.kip/1000/us.ft**2))
    return round(prelim_width.sqrt()/us.ft*us.ft)

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

def max_fact_load(dead_load,live_load,snow_load,wind_load):
    return max(1.4*dead_load,
               1.2*dead_load+1.6*live_load+0.5*snow_load,
               1.2*dead_load+1.6*snow_load+live_load,
               1.2*dead_load+1.6*snow_load+0.5*wind_load,
               1.2*dead_load+wind_load+live_load+0.5*snow_load,
               0.9*dead_load+wind_load)*us.kip


def two_way_shear(foot_width,foot_thick,col_dim,dead_load,live_load,snow_load,wind_load,f_c):
    #Asuming #8 bars are used
    """
    Following ACI 3-18 TABLE 22.6.5.2
    variations for edge and corner columns have not been implemented
    """
    d_avg = ((foot_thick-3-0.5)+(foot_thick-3-1.5))/2
    shear_trib_area = foot_width**2-(col_dim*us.inch+d_avg)**2
    q_nu = max_fact_load(dead_load,live_load,snow_load,wind_load)/(foot_width**2)
    Vu = q_nu*shear_trib_area
    Vu_stress = Vu/(4*(col_dim*us.inch+d_avg)*d_avg)
    lamda_s = min((2/(1+(d_avg/us.inch/10)))**0.5,1)
    beta = 1
    alpha_s = 40
    b_0 = 4*(col_dim*us.inch+d_avg)

    vc = min(4*lamda_s*f_c**0.5,
             (2+4/beta)*lamda_s*f_c**0.5,
             (2+(alpha_s*d_avg/b_0)*lamda_s*f_c**0.5))*us.kip/us.inch**2/1000



    


    return Vu_stress, vc

#THIS FUNCTION HAS NOT BEEN CHECKED YET
