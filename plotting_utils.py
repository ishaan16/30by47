import plotly.graph_objects as go
from utils import fetch_india_sector_gdp
from ai_insights import get_ai_insight


def create_sector_sunburst_chart():
    """
    Create a sunburst chart showing India's GDP sector distribution.
    
    Returns:
        plotly.graph_objects.Figure: The sunburst chart figure
    """
    # Fetch sector-wise GDP data
    sector_data = fetch_india_sector_gdp()
    
    if not sector_data:
        return None
    
    # Color scheme for grouped sectors
    agriculture_color = '#8B4513'  # Brown for agriculture
    industry_color = '#4169E1'     # Blue for industry
    services_color = '#32CD32'     # Green for services
    
    # Color scheme for detailed sectors
    detailed_colors_scheme = {
        'agriculture': '#8B4513',
        'manufacturing': '#4169E1',
        'construction': '#4682B4',
        'mining': '#5F9EA0',
        'utilities': '#20B2AA',
        'trade_hotels': '#32CD32',
        'financial_services': '#228B22',
        'real_estate': '#006400',
        'public_admin': '#90EE90',
        'other_services': '#98FB98'
    }
    
    # Calculate grouped values
    agriculture_total = sector_data.get('agriculture', {}).get('percentage', 0)
    
    # Industry sectors (manufacturing, construction, mining, utilities)
    industry_sectors = ['manufacturing', 'construction', 'mining', 'utilities']
    industry_total = sum(sector_data.get(sector, {}).get('percentage', 0) for sector in industry_sectors)
    
    # Services sectors (trade_hotels, financial_services, real_estate, public_admin, other_services)
    services_sectors = ['trade_hotels', 'financial_services', 'real_estate', 'public_admin', 'other_services']
    services_total = sum(sector_data.get(sector, {}).get('percentage', 0) for sector in services_sectors)
    
    # Create hierarchical data for sunburst chart
    labels = []
    parents = []
    values = []
    colors = []
    hover_texts = []
    
    # Add main sectors
    labels.extend(['Agriculture', 'Industry', 'Services'])
    parents.extend(['', '', ''])
    values.extend([agriculture_total, industry_total, services_total])
    colors.extend([agriculture_color, industry_color, services_color])
    hover_texts.extend([
        get_ai_insight("Agriculture", agriculture_total, sector_data),
        get_ai_insight("Industry", industry_total, sector_data),
        get_ai_insight("Services", services_total, sector_data)
    ])
    
    # Add detailed sectors (including farming as child of agriculture)
    for sector, data in sector_data.items():
        if isinstance(data, dict) and 'percentage' in data:
            if sector == 'agriculture':
                # Add farming as child of agriculture
                labels.append('Farming')
                values.append(data['percentage'])
                colors.append(detailed_colors_scheme.get(sector, '#808080'))
                parents.append('Agriculture')
                hover_texts.append(get_ai_insight("Agriculture", data['percentage'], sector_data))
            else:
                # Add other sectors as before
                sector_name = sector.replace('_', ' ').title()
                labels.append(sector_name)
                values.append(data['percentage'])
                colors.append(detailed_colors_scheme.get(sector, '#808080'))
                
                # Determine parent
                if sector in ['manufacturing', 'construction', 'mining', 'utilities']:
                    parents.append('Industry')
                else:
                    parents.append('Services')
                
                # Create dynamic AI-powered hover text
                sector_name = sector.replace('_', ' ').title()
                hover_texts.append(get_ai_insight(sector_name, data['percentage'], sector_data))
    
    # Create sunburst chart
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(colors=colors),
        textinfo='label',
        textfont=dict(size=12),
        hovertemplate='<b>%{label}</b><br><br>%{customdata}<extra></extra>',
        customdata=hover_texts,
        branchvalues='total',
        hoverlabel=dict(font_size=10, font_family="Arial")
    ))
    
    # Update layout for sunburst chart
    fig.update_layout(
        title={
            'text': f"Current GDP Sector Distribution ({list(sector_data.values())[0]['year']})",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        showlegend=False,
        width=600,
        height=450,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig


def get_sector_data():
    """
    Get processed sector data for analysis.
    
    Returns:
        dict: Dictionary containing grouped and detailed sector data
    """
    sector_data = fetch_india_sector_gdp()
    
    if not sector_data:
        return None
    
    # Calculate grouped values
    agriculture_total = sector_data.get('agriculture', {}).get('percentage', 0)
    
    # Industry sectors (manufacturing, construction, mining, utilities)
    industry_sectors = ['manufacturing', 'construction', 'mining', 'utilities']
    industry_total = sum(sector_data.get(sector, {}).get('percentage', 0) for sector in industry_sectors)
    
    # Services sectors (trade_hotels, financial_services, real_estate, public_admin, other_services)
    services_sectors = ['trade_hotels', 'financial_services', 'real_estate', 'public_admin', 'other_services']
    services_total = sum(sector_data.get(sector, {}).get('percentage', 0) for sector in services_sectors)
    
    return {
        'raw_data': sector_data,
        'grouped': {
            'agriculture': agriculture_total,
            'industry': industry_total,
            'services': services_total
        },
        'year': list(sector_data.values())[0]['year'] if sector_data else None
    }


def create_projected_sector_pie_chart(projections: dict, target_year: int = 2047):
    """
    Create a pie chart showing projected sector contributions for the target year.
    
    Args:
        projections: Dictionary with sector projections from fetch_sector_growth_projections
        target_year: Target year for projections (default 2047)
        
    Returns:
        plotly.graph_objects.Figure: The pie chart figure
    """
    if not projections:
        return None
    
    # Extract projected values
    labels = []
    values = []
    colors = []
    hover_texts = []
    
    # Color scheme for sectors
    sector_colors = {
        'agriculture': '#8B4513',  # Brown
        'industry': '#4169E1',     # Blue
        'services': '#32CD32'      # Green
    }
    
    for sector, data in projections.items():
        if 'projected_value' in data:
            sector_name = sector.replace('_', ' ').title()
            labels.append(sector_name)
            values.append(data['projected_value'])
            colors.append(sector_colors.get(sector, '#808080'))
            
            # Create hover text with growth information
            current = data['current_value']
            projected = data['projected_value']
            growth_rate = data['annual_growth_rate']
            change_percentage = ((projected - current) / current) * 100
            
            hover_text = f"{sector_name}<br>"
            hover_text += f"Projected: {projected:.1f}%<br>"
            hover_text += f"Current: {current:.1f}%<br>"
            hover_text += f"Annual Growth: {growth_rate:.2f}%<br>"
            hover_text += f"Change: {change_percentage:+.1f}%"
            
            hover_texts.append(hover_text)
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(size=12),
        hovertemplate='<b>%{customdata}</b><extra></extra>',
        customdata=hover_texts,
        hoverlabel=dict(font_size=10, font_family="Arial")
    )])
    
    # Update layout for projected pie chart
    fig.update_layout(
        title={
            'text': f"Projected Sector Contributions ({target_year})",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        showlegend=False,
        width=600,
        height=450,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig


def create_comparison_country_pie_chart(country_name: str, sector_data: dict, size: tuple = (200, 200)):
    """
    Create a small pie chart for a comparison country's sector distribution.
    
    Args:
        country_name: Name of the country
        sector_data: Dictionary with sector data
        size: Tuple of (width, height) for the chart
        
    Returns:
        plotly.graph_objects.Figure: The pie chart figure
    """
    if not sector_data:
        return None
    
    # Extract sector data (excluding metadata like '_year')
    labels = []
    values = []
    
    for sector, data in sector_data.items():
        if sector != '_year' and isinstance(data, dict) and 'percentage' in data:
            sector_name = sector.replace('_', ' ').title()
            labels.append(sector_name)
            values.append(data['percentage'])
    
    if not values:
        return None
    
    # Color scheme for sectors
    sector_colors = {
        'agriculture': '#8B4513',  # Brown
        'industry': '#4169E1',     # Blue
        'services': '#32CD32'      # Green
    }
    
    colors = [sector_colors.get(label.lower(), '#808080') for label in labels]
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='percent',
        textfont=dict(size=10),
        hovertemplate='<b>%{label}</b><br>%{value:.1f}%<extra></extra>'
    )])
    
    # Update layout for small size
    fig.update_layout(
        title={
            'text': country_name,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 12}
        },
        showlegend=False,
        width=size[0],
        height=size[1],
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig 