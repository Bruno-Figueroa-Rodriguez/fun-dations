import rc_calcs_and_checks as rc
import handcalcs
from handcalcs.decorator import handcalc
import forallpeople as us
us.environment('us_customary')
from plotly import graph_objects as go
import pytest



def test_prelim_width():

    assert abs(float(rc.prelim_width(4000,240,300,0,0)[1])-float(12*us.ft))<1

#test_prelim_width()


def test_prelim_thick():

    assert float(rc.prelim_thick(24)[1]) == float(24*us.inch*1.5)

test_prelim_thick()

def test_footing_geom():

    assert type(rc.footing_geom(24,
                               rc.prelim_width(4000,240,300,0,0)[1],
                               rc.prelim_thick(24)[1],)) == go.Figure
    
test_footing_geom()

def test_max_fact_load():

    assert rc.max_fact_load(240,300,0,0) == 768*us.kip

test_max_fact_load()

def test_two_way_shear():

    print(rc.two_way_shear(rc.prelim_width(4000,240,300,0,0)[1],
                            rc.prelim_thick(24)[1],
                            24,
                            rc.max_fact_load(240,300,0,0),
                            4000)[1])

    twowaychecks = (0.09*us.kg*us.m**-1*us.s**-2,
                    0.175*us.kg*us.m**-1*us.s**-2,
                    32*us.inch,
                    5.689*us.kg*us.m**-1*us.s**-2,
                    0.75)

    print(twowaychecks)
    float(rc.two_way_shear(rc.prelim_width(4000,240,300,0,0)[1],rc.prelim_thick(24)[1],24,rc.max_fact_load(240,300,0,0),4000)[1][0])
    print(twowaychecks[0])
    assert float(abs((rc.two_way_shear(rc.prelim_width(4000,240,300,0,0)[1],rc.prelim_thick(24)[1],24,rc.max_fact_load(240,300,0,0),4000)[1][0]) - twowaychecks[0]*1000)) < 1

test_two_way_shear()


# def test_one_way_shear():


# def test_flexure():


# def test_flexure_reinf():


# def test_rebar_amount():


# def test_prelim_flex_reinf_calcs():


# def test_flex_demo():