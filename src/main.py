"""Central streamlit file for Forecastly"""

import datetime
import streamlit as st
from data_visualiser import DataVisualiser
from constants import WEATHER_ATTRIBUTES


def main():
    """Main function for the Streamlit app"""
    st.set_page_config(layout="wide", page_title="Forecastly", page_icon="📊")
    st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

    st.title("Forecastly")

    # TODO: Column sizing is dodgy in different screen sizes
    col1, col2, col3, col4, col5, col6 = st.columns(
        [1, 1, 2, 1, 1.2, 1], vertical_alignment="bottom"
    )
    with col1:
        ticker = st.text_input("Ticker", placeholder="MS")
    with col2:
        location = st.text_input("City", placeholder="New York")
    with col3:
        weather_attributes = st.multiselect(
            "Weather Attributes",
            WEATHER_ATTRIBUTES,
        )
    with col4:
        action = st.segmented_control(
            "Action", ["Correlate", "Forecast"], default="Correlate"
        )
    with col5:
        if action == "Correlate":
            date_range = st.date_input(
                "Date Range",
                value=[],
                format="DD/MM/YYYY",
                max_value="today",
                min_value=datetime.date(1979, 1, 1),
            )
            with col6:
                submit = st.button(
                    "Submit",
                    disabled=not ticker
                    or not location
                    or not weather_attributes
                    or not date_range,
                    use_container_width=True,
                )
        else:
            submit = st.button(
                "Submit",
                disabled=not ticker or not location or not weather_attributes,
                use_container_width=True,
            )

    st.divider()

    if submit:
        if action == "Correlate":
            try:
                data = DataVisualiser(date_range, ticker, location, weather_attributes)
                fig = data.create_figure()

            except ValueError as e:
                st.error(e)

            else:
                graph_col, cor_col = st.columns(
                    [3.5, 1], border=True, vertical_alignment="center"
                )

                with graph_col:
                    st.plotly_chart(fig)

                with cor_col:
                    title, message = data.get_correlation()
                    st.markdown(
                        f"""
                        <style>
                            h3 a.anchor-link {{
                                display: none !important;
                            }}
                        </style>
                        <h3 style='text-align: center;'>{title}</h3>
                        <p style='text-align: center;'>{message}</p>
                        """,
                        unsafe_allow_html=True,
                    )


if __name__ == "__main__":
    main()
