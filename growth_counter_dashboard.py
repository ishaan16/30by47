import streamlit as st
import math
import requests
from datetime import datetime
import pandas as pd

st.title("Required GDP Growth Calculator")

st.write(
    """
This app calculates the per annum growth required to reach India's target GDP value over a specified number of years.
"""
)


def get_india_gdp_usd():
    # World Bank API for India's GDP (NY.GDP.MKTP.CD) in USD, most recent year
    url = "https://api.worldbank.org/v2/country/IN/indicator/NY.GDP.MKTP.CD?format=json&per_page=1"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 1 and data[1]:
                gdp = data[1][0].get("value")
                if gdp:
                    return float(gdp)
    except Exception as e:
        st.warning(f"Could not fetch latest GDP value: {e}")
    # Fallback to IMF/StatisticsTimes.com 2025 estimate
    return 10000.0  # 4271920000000.0


current_gdp = get_india_gdp_usd()

# Accept current and target GDP in billion dollars for user input
current_billion = st.number_input(
    "Current GDP of India (Billion $)",
    min_value=0.0,
    value=current_gdp / 1e9,
    step=500.0,
    format="%.2f",
)
target_billion = st.number_input(
    "Target GDP of India (Billion $)", min_value=0.0, value=30000.0, step=500.0, format="%.2f"
)

# Convert back to raw numbers for calculation
current = current_billion * 1e9
target = target_billion * 1e9


current_year = datetime.now().year
target_year = st.number_input("Target year", min_value=current_year + 1, value=2047, step=1)
time = target_year - current_year

if current > 0 and target > 0 and time > 0:
    try:
        growth = 100 * (10 ** (math.log10(target / current) / time) - 1)

        # Fetch latest GDP growth rate of India
        def fetch_latest_gdp_growth():
            url = "https://api.worldbank.org/v2/country/IN/indicator/NY.GDP.MKTP.KD.ZG?format=json&per_page=2"
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list) and len(data) > 1 and data[1]:
                        for entry in data[1]:
                            if entry.get("value") is not None:
                                return float(entry["value"]), entry.get("date")
            except Exception as e:
                st.warning(f"Could not fetch latest GDP growth rate: {e}")
            return None, None

        latest_growth, latest_year = fetch_latest_gdp_growth()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<b>Required Per Annum Growth (%)</b>", unsafe_allow_html=True)
            st.markdown(
                f"<span style='font-size:2em;'><b>{growth:.2f}%</b></span>", unsafe_allow_html=True
            )
        with col2:
            if latest_growth is not None:
                color = "green" if latest_growth >= growth else "red"
                st.markdown(
                    f"<b>Latest GDP Growth Rate ({latest_year})</b>", unsafe_allow_html=True
                )
                st.markdown(
                    f"<span style='font-size:2em; color:{color};'><b>{latest_growth:.2f}%</b></span>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("<b>Latest GDP Growth Rate</b>", unsafe_allow_html=True)
                st.markdown(
                    f"<span style='font-size:2em; color:gray;'><b>N/A</b></span>",
                    unsafe_allow_html=True,
                )

        # --- Per Capita GDP Comparison Section ---
        st.markdown("---")
        st.header(":money_with_wings: Per Capita GDP Comparison")

        # Fetch India's population (latest)
        def fetch_india_population():
            url = "https://api.worldbank.org/v2/country/IN/indicator/SP.POP.TOTL?format=json&per_page=2"
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list) and len(data) > 1 and data[1]:
                        for entry in data[1]:
                            if entry.get("value") is not None:
                                return float(entry["value"]), entry.get("date")
            except Exception as e:
                st.warning(f"Could not fetch India's population: {e}")
            return None, None

        india_pop, india_pop_year = fetch_india_population()
        if india_pop:
            current_per_capita = current / india_pop
            projected_per_capita = target / india_pop
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    "<b>Current Per Capita GDP (India, {year}):</b>".format(year=india_pop_year),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='font-size:2.5em; font-weight:bold; color:#1f77b4;'>$ {current_per_capita:,.2f}</div>",
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(
                    f"<b>Projected Per Capita GDP (India, {target_year}):</b>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='font-size:2.5em; font-weight:bold; color:#2ca02c;'>$ {projected_per_capita:,.2f}</div>",
                    unsafe_allow_html=True,
                )

            # Use local CSV for per capita GDP comparison
            try:
                df = pd.read_csv("gdp-per-capita-by-country-2025.csv")
                df = df.dropna(subset=["GDPPerCapita_GDPPerCapitaViaIMF_usd_2025"])
                df["GDPPerCapita_GDPPerCapitaViaIMF_usd_2025"] = (
                    df["GDPPerCapita_GDPPerCapitaViaIMF_usd_2025"]
                    .replace("[\$,]", "", regex=True)
                    .astype(float)
                )
                closest_5 = df.iloc[
                    (df["GDPPerCapita_GDPPerCapitaViaIMF_usd_2025"] - projected_per_capita)
                    .abs()
                    .argsort()[:5]
                ]
                st.markdown(
                    f"<br/><b>5 Countries with most similar per capita GDP to India's projected ({target_year}):</b>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<ul style='font-size:1.2em;'>"
                    + "\n".join(
                        [
                            f"<li><b>{row['country']}</b>: <span style='font-size:1.3em; color:#ff7f0e;'>$ {row['GDPPerCapita_GDPPerCapitaViaIMF_usd_2025']:,.2f}</span></li>"
                            for _, row in closest_5.iterrows()
                        ]
                    )
                    + "</ul>",
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.warning(f"Could not read per capita GDP CSV: {e}")
        else:
            st.warning("Could not fetch India's population for per capita GDP calculation.")
    except Exception as e:
        st.error(f"Error in calculation: {e}")
else:
    st.warning(
        "Please enter positive values for all inputs and ensure target year is in the future."
    )
