import streamlit as st
from data_visualizer import DataVisualizer

def main():
    st.set_page_config(layout="wide")

    st.title("Forecastly")

    # TODO: Column sizing is dodgy in different screen sizes
    col1, col2, col3, col4, col5, col6 = st.columns(
        [1, 1, 2, 1, 1.2, 1], vertical_alignment="bottom"
    )
    with col1:
        ticker = st.text_input("Ticker", placeholder="MS", value="MS")
    with col2:
        location = st.text_input("City", placeholder="New York", value="New York")
    with col3:
        weather_attributes = st.multiselect(
            "Weather Attributes",
            ["Temperature", "Humidity", "Precipitation", "Wind Speed", "UV Light"],
            default=["Temperature"],
        )
    with col4:
        action = st.segmented_control(
            "Action", ["Correlate", "Forecast"], default="Correlate"
        )
    with col5:
        if action == "Correlate":
            date_range = st.date_input(
                "Date Range", value=[], format="DD/MM/YYYY", max_value="today"
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
    
    if submit:
        if action == "Correlate":
            data = DataVisualizer(date_range, ticker, location, weather_attributes)
            fig = data.create_figure()
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
