import jdatetime
import streamlit as st


def show_box(box_title, main_text):
    colors = (252, 248, 243)
    selected_color = colors
    wch_colour_font = (0, 0, 0)
    fontsize = 22
    valign = "left"
    lnk = ('<link rel="stylesheet" '
           'href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" '
           'crossorigin="anonymous">')

    htmlstr = f"""<p style='background-color: rgb({selected_color[0]}, 
                                                  {selected_color[1]}, 
                                                  {selected_color[2]}, 0.75); 
                            color: rgb({wch_colour_font[0]}, 
                                       {wch_colour_font[1]}, 
                                       {wch_colour_font[2]}, 0.75); 
                            font-size: {fontsize}px; 
                            border-radius: 7px; 
                            padding-right: 12px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;
                            text-align: center;'>
                            <i class=' fa-xs'></i> {main_text}
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>{box_title}</style></span></p>"""

    return st.markdown(lnk + htmlstr, unsafe_allow_html=True)


def miladi_to_shamsi(date):
    return jdatetime.date.fromgregorian(date=date)


today_shamsi = miladi_to_shamsi(jdatetime.datetime.now().togregorian())
