import astropy.units as u
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import astropy.constants as const
import pandas as pd

def ballistic_map(carr_coord, rss, vsw):
    """Ballistically maps the spacecraft longitude to rss.

    Parameters
    ----------
    rss : Quantity
        Distance from the Sun to ballistically map too. Needs to have units attached.
    vsw : Quantity
        Speed to perform the ballistic mapping. Needs to have units attached.

    Returns
    -------
    float
        Mapped longitude in degrees without units attached.
    """
    #add the extra longitude
    ss_skycoord = carr_coord.lon + delta_long(carr_coord.radius, rss, vsw)

    #extract without units
    ss_lon = ss_skycoord.value

    #wrap angle around 360
    while (ss_lon > 360).any():
        ss_lon -= (ss_lon > 360).astype(int)*360.

    return ss_lon


def delta_long(r, rss, vsw):
    """Finds the extra longitude needed in ballistic mapping

    Parameters
    ----------
    r : Quantity
        Distance of the spacecraft. Units attached.
    rss : Quantity
        Distance to ballistically map to. Units attached.
    vsw : Quantity
        Speed used for the ballistic mapping. Units attached.

    Returns
    -------
    Quantity
        Extra longitude from ballistic mapping
    """
    sun_rot = (14.713 *u.deg)/(24*3600*u.s)
    return sun_rot * (r - rss) / vsw

def wrap(arr, difference = 340):
    diff = np.diff(arr)
    idx = np.argwhere(abs(diff) > difference)
    arr[idx+1] = np.nan

    return arr


def add_sc(fig, df, label, colour):
    by_default = ['PSP', 'Solar Orbiter']
    if label not in by_default:
        is_visible = 'legendonly'
    else:
        is_visible = True
        
    # adds a scatter point for the legend
    fig.add_trace(
                go.Scatter(
                    #make a date that is not visible
                    x=np.array([datetime(2017,1,1), datetime(2017,1,1)]), 
                    y=np.array([0,0]), 
                    mode='markers',
                    name = label,
                    legendgroup=label,
                    marker = dict(
                        color= colour,
                        size = 20,# one of plotly colorscales
                        symbol= 'circle'),
                    showlegend=True,
                    visible=is_visible))   
    
    times = df.index
    radii = df['Radius'].values/(const.R_sun.to(u.km))
    text_list = ['{}'.format(value) for value in radii.value]

    # top panel Radius
    fig.append_trace(go.Scatter(
        x=df.index,
        y=df['Radius'].values/u.au.to(u.km),
        name = f'{label} Radius',
        text = text_list,
        showlegend = False,
        visible=is_visible,
        legendgroup = label,
        hovertemplate=
            "R: %{y:.2f} AU<br>" +
            "%{text:.0f} Rs",
        line=dict(color=colour, width=2),
    
    ), row=1, col=1)
    
    # Latitude
    fig.append_trace(go.Scatter(
        x=df.index,
        y=df['Carr_lat'].values,
        name = f'{label} Latitude',
        hovertemplate= "%{y:.1f} degrees<br>",
        showlegend = False,
        visible=is_visible,
        legendgroup = label,
        line=dict(color=colour, width=2),
    ), row=2, col=1)
    # Longitude
    fig.append_trace(go.Scatter(
        x=df.index,
        y=wrap(df['Carr_lon'].values),
        name = f'{label} Longitude',
        hovertemplate= "%{y:.0f} degrees<br>",
        showlegend = False,
        visible=is_visible,
        legendgroup = label,
        line=dict(color=colour, width=2),
    ), row=3, col=1)
    
    #this bit makes the highlighting better formatted between Mapped_300 and 700
    mod_700 = df['Mapped_700'].values.copy()

    mod_dates = df.index.values.copy()
    
    diff = np.diff(mod_700)
    idx = np.argwhere(abs(diff) > 90)
    mod_700[idx+1] = 0
    
    mod_300 = df['Mapped_300'].values.copy()
    diff = np.diff(mod_300)
    idx = np.argwhere(abs(diff) > 90)
    #also change the datetimes of these to be from the one ahead of it
    mod_dates[idx] = mod_dates[idx+1]
    
    mod_700[mod_700 >= mod_300] = 0
    #need to add extra points so there are two values per date at certain
    
    mod_700 = np.nan_to_num(mod_700, 0)
    
    random_df = pd.DataFrame(index = mod_dates)
    # Mapped Longitude fill
    # fig.append_trace(go.Scatter(
    #     x=random_df.index,
    #     y=mod_300,
    #     legendgroup = label,
    #     showlegend = False,
    #     visible=is_visible,
    #     fill=None,
    #     # hoverinfo= 'none',
    #     hovertemplate= "%{y:.0f} degrees<br>",
    #     line=dict(color=colour, width=0),
    # ), row=4, col=1)
    
    # fig.append_trace(go.Scatter(
    #     x=random_df.index,
    #     y=mod_700,
    #     legendgroup = label,
    #     showlegend = False,
    #     visible=is_visible,
    #     fill='tonexty',
    #     # hoverinfo= 'none',
    #     hovertemplate= "%{y:.0f} degrees<br>",
    #     line=dict(color=colour, width=0),
    # ), row=4, col=1)
    
    
    # mapped longitude line
    fig.append_trace(go.Scatter(
        x=df.index,
        y=wrap(df['Mapped_300'].values.copy(), 90),
        name = f'{label} 300 km/s',
        hovertemplate= "%{y:.0f} degrees<br>",
        showlegend = False,
        visible=is_visible,
        legendgroup = label,
        line=dict(color=colour, width=2),
    ), row=4, col=1)
    
    
    
    fig.append_trace(go.Scatter(
        x=df.index,
        y=wrap(df['Mapped_700'].values.copy(), 90),
        name = f'{label} 700 km/s',
        legendgroup = label,
        showlegend = False,
        visible=is_visible,
        fill=None,
        hovertemplate= "%{y:.0f} degrees<br>",
        line=dict(color=colour, width=2),
    ), row=4, col=1)
    
    
    
    
    #have to make an invisible trace to make the fill work - if 300 > 700 then make it have zeros so the fill works
        


    return fig