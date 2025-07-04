from datetime import datetime

import pandas as pd
import streamlit as st

from utils import (calculate_required_growth, fetch_india_dependency_ratio,
                   fetch_india_median_age, fetch_india_population,
                   fetch_india_sector_gdp, fetch_latest_gdp_growth,
                   get_india_gdp_usd, project_median_age_evidence_based,
                   project_population, fetch_sector_growth_projections,
                   get_sector_growth_insights, fetch_country_sector_gdp,
                   get_country_code)
from plotting_utils import create_sector_sunburst_chart, get_sector_data, create_projected_sector_pie_chart, create_comparison_country_pie_chart

st.title("Required GDP Growth Calculator")

st.write(
    """
This app calculates the per annum growth required to reach India's target GDP value over a specified number of years.
"""
)

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
        growth = calculate_required_growth(current, target, time)

        # Fetch latest GDP growth rate of India
        latest_growth, latest_year = fetch_latest_gdp_growth()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<b>Required Per Annum Growth (%)</b>", unsafe_allow_html=True)
            if growth is not None:
                st.markdown(
                    f"<span style='font-size:2em;'><b>{growth:.2f}%</b></span>", unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<span style='font-size:2em; color:red;'><b>Error</b></span>", unsafe_allow_html=True
                )
        with col2:
            if latest_growth is not None and growth is not None:
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

        # Fetch India's population (latest) from World Bank
        india_pop, india_pop_year = fetch_india_population()
        projected_pop = None
        if india_pop and india_pop_year and target_year > india_pop_year:
            projected_pop = project_population(india_pop, india_pop_year, target_year)

        if india_pop:
            current_per_capita = current / india_pop
            # Use projected population if available, otherwise use current population
            population_for_projection = projected_pop if projected_pop else india_pop
            projected_per_capita = target / population_for_projection
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f"<b>Current Per Capita GDP (India, {india_pop_year}):</b>",
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
                    f"<br/><b>Countries with current GDP per capita closest to India's projected GDP per capita in {target_year}:</b>",
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

        # --- Sector-wise GDP Analysis Section ---
        st.markdown("---")
        st.header(":factory: Sector-wise GDP Analysis")
        
        # Current sector distribution (sunburst chart)
        fig_current = create_sector_sunburst_chart()
        if fig_current:
            st.plotly_chart(fig_current, use_container_width=True)
        else:
            st.warning("Could not fetch current sector data.")
        
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)  # Small vertical gap
        
        # Projected sector distribution (pie chart)
        with st.spinner("Fetching sector growth projections..."):
            projections = fetch_sector_growth_projections(target_year)
        if projections:
            fig_projected = create_projected_sector_pie_chart(projections, target_year)
            if fig_projected:
                st.plotly_chart(fig_projected, use_container_width=True)
            else:
                st.warning("Could not create projected sector chart.")
        else:
            st.warning("Could not fetch sector growth projections.")
        
        # --- Comparison Countries Section ---
        st.markdown("<br/>", unsafe_allow_html=True)
        st.subheader(":globe_with_meridians: International Sector Comparison")
        
        # Get the closest 5 countries from the per capita comparison
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
            
            # Create two rows: 3 charts on top, 2 charts below
            # Top row with 3 charts
            top_cols = st.columns(3)
            
            # Convert to list to avoid generator issues
            closest_5_list = closest_5.to_dict('records')
            
            for i in range(min(3, len(closest_5_list))):
                row = closest_5_list[i]
                country_name = row['country']
                country_code = get_country_code(country_name)
                
                if country_code:
                    with st.spinner(f"Fetching sector data for {country_name}..."):
                        sector_data = fetch_country_sector_gdp(country_code)
                        
                        if sector_data:
                            fig = create_comparison_country_pie_chart(country_name, sector_data)
                            if fig:
                                with top_cols[i]:
                                    st.plotly_chart(fig, use_container_width=True)
                        else:
                            with top_cols[i]:
                                st.markdown(f"<div style='text-align:center; color:gray;'>{country_name}<br/>No data</div>", unsafe_allow_html=True)
                else:
                    with top_cols[i]:
                        st.markdown(f"<div style='text-align:center; color:gray;'>{country_name}<br/>No code</div>", unsafe_allow_html=True)
            
            # Bottom row with 2 charts (centered)
            bottom_cols = st.columns([1, 2, 2, 1])  # Creates space, chart, chart, space
            
            for i in range(3, min(5, len(closest_5_list))):
                row = closest_5_list[i]
                country_name = row['country']
                country_code = get_country_code(country_name)
                
                if country_code:
                    with st.spinner(f"Fetching sector data for {country_name}..."):
                        sector_data = fetch_country_sector_gdp(country_code)
                        
                        if sector_data:
                            fig = create_comparison_country_pie_chart(country_name, sector_data)
                            if fig:
                                with bottom_cols[i-2]:  # Use columns 1 and 2 (skip the spacer columns)
                                    st.plotly_chart(fig, use_container_width=True)
                        else:
                            with bottom_cols[i-2]:
                                st.markdown(f"<div style='text-align:center; color:gray;'>{country_name}<br/>No data</div>", unsafe_allow_html=True)
                else:
                    with bottom_cols[i-2]:
                        st.markdown(f"<div style='text-align:center; color:gray;'>{country_name}<br/>No code</div>", unsafe_allow_html=True)
                        
        except Exception as e:
            st.warning(f"Could not fetch comparison country data: {e}")

        # --- Demographic Information Section ---
        if india_pop and projected_pop:
            st.markdown("---")
            st.header(":busts_in_silhouette: Demographic Information")
            
            # Fetch demographic data
            median_age, median_age_year = fetch_india_median_age()
            dependency_ratio, dep_ratio_year = fetch_india_dependency_ratio()
            
            # Current demographic information
            st.markdown("<br/>", unsafe_allow_html=True)
            st.subheader(":calendar: Current Demographics")
            st.markdown("<br/>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<b>Population ({india_pop_year}):</b>", unsafe_allow_html=True)
                st.markdown(
                    f"<div style='font-size:1.5em; font-weight:bold; color:#1f77b4;'>{india_pop:,.0f}</div>",
                    unsafe_allow_html=True,
                )
            with col2:
                if median_age:
                    st.markdown(f"<b>Median Age ({median_age_year}):</b>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='font-size:1.5em; font-weight:bold; color:#ff7f0e;'>{median_age:.1f} years</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown("<b>Median Age:</b>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='font-size:1.5em; font-weight:bold; color:gray;'>N/A</div>",
                        unsafe_allow_html=True,
                    )
            with col3:
                if dependency_ratio:
                    st.markdown(f"<b>Dependency Ratio ({dep_ratio_year}):</b>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='font-size:1.5em; font-weight:bold; color:#9467bd;'>{dependency_ratio:.1f}%</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown("<b>Dependency Ratio:</b>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='font-size:1.5em; font-weight:bold; color:gray;'>N/A</div>",
                        unsafe_allow_html=True,
                    )
            
            # Population category and dependency level
            st.markdown("<br/>", unsafe_allow_html=True)
            if median_age or dependency_ratio:
                col1, col2 = st.columns(2)
                with col1:
                    if median_age:
                        # Calculate age category
                        if median_age < 30:
                            age_category = "Young Population"
                            category_color = "#2ca02c"
                        elif median_age < 40:
                            age_category = "Middle-aged Population"
                            category_color = "#ff7f0e"
                        else:
                            age_category = "Aging Population"
                            category_color = "#d62728"
                        
                        st.markdown("<b>Population Category:</b>", unsafe_allow_html=True)
                        st.markdown(
                            f"<div style='font-size:1.5em; font-weight:bold; color:{category_color};'>{age_category}</div>",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown("<b>Population Category:</b>", unsafe_allow_html=True)
                        st.markdown(
                            f"<div style='font-size:1.5em; font-weight:bold; color:gray;'>N/A</div>",
                            unsafe_allow_html=True,
                        )
                with col2:
                    if dependency_ratio:
                        # Interpret dependency ratio
                        if dependency_ratio < 50:
                            dep_category = "Low Dependency"
                            dep_color = "#2ca02c"
                        elif dependency_ratio < 70:
                            dep_category = "Moderate Dependency"
                            dep_color = "#ff7f0e"
                        else:
                            dep_category = "High Dependency"
                            dep_color = "#d62728"
                        
                        st.markdown("<b>Dependency Level:</b>", unsafe_allow_html=True)
                        st.markdown(
                            f"<div style='font-size:1.5em; font-weight:bold; color:{dep_color};'>{dep_category}</div>",
                            unsafe_allow_html=True,
                        )
            

                    else:
                        st.markdown("<b>Dependency Level:</b>", unsafe_allow_html=True)
                        st.markdown(
                            f"<div style='font-size:1.5em; font-weight:bold; color:gray;'>N/A</div>",
                            unsafe_allow_html=True,
                        )
            
            # Projected demographic information
            st.markdown("<br/>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("<br/>", unsafe_allow_html=True)
            st.subheader(":chart_with_upwards_trend: Projected Demographics")
            st.markdown("<br/>", unsafe_allow_html=True)
            
            # Calculate projected median age if current age is available
            projected_median_age = None
            if median_age and median_age_year:
                projected_median_age = project_median_age_evidence_based(median_age, median_age_year, target_year)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<b>Projected Population ({target_year}):</b>", unsafe_allow_html=True)
                st.markdown(
                    f"<div style='font-size:1.5em; font-weight:bold; color:#2ca02c;'>{projected_pop:,.0f}</div>",
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(f"<b>Projected Median Age ({target_year}):</b>", unsafe_allow_html=True)
                if projected_median_age:
                    st.markdown(
                        f"<div style='font-size:1.5em; font-weight:bold; color:#ff7f0e;'>{projected_median_age:.1f} years</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<div style='font-size:1.5em; font-weight:bold; color:gray;'>N/A</div>",
                        unsafe_allow_html=True,
                    )
            

    except Exception as e:
        st.error(f"Error in calculation: {e}")
else:
    st.warning(
        "Please enter positive values for all inputs and ensure target year is in the future."
    )
