# GDP Growth Calculator Dashboard

A comprehensive Streamlit web application that calculates the required annual GDP growth rate for India to reach its target GDP by a specified year, with detailed demographic and economic analysis.

## 🎯 Purpose

This dashboard helps policymakers, economists, and researchers understand:
- The annual growth rate required for India to achieve its GDP targets
- Current vs. projected demographic trends
- Per capita GDP comparisons with other countries
- Population and dependency ratio analysis

## 📊 Features

### 1. **GDP Growth Rate Calculator**
- Calculates required annual growth rate using compound growth formula
- Compares with India's latest actual GDP growth rate
- Visual indicators (green/red) for performance comparison

### 2. **Per Capita GDP Analysis**
- Current vs. projected per capita GDP calculations
- Population projections using UN growth rates
- Country comparisons showing which nations have similar per capita GDP to India's projected values

### 3. **Demographic Information**
- **Current Demographics**: Population, median age, dependency ratio
- **Population Categories**: Young/Middle-aged/Aging population classification
- **Dependency Levels**: Low/Moderate/High dependency ratio interpretation
- **Projected Demographics**: Future population and median age projections

## 🏗️ Project Structure

```
thirtybyfortyseven/
├── growth_counter_dashboard.py    # Main Streamlit application
├── utils.py                       # Utility functions and API calls
├── requirements.txt               # Python dependencies
├── gdp-per-capita-by-country-2025.csv  # Country comparison data
├── test_population_apis.py        # API testing script
├── test_population.xlsx           # Population test data
└── README.md                      # This file
```

## 🔧 Technical Architecture

### **Main Application (`growth_counter_dashboard.py`)**
- **Streamlit Interface**: User-friendly web interface
- **Input Validation**: Ensures positive values and future target years
- **Error Handling**: Graceful handling of API failures and calculation errors
- **Responsive Layout**: Multi-column design for better data presentation

### **Utility Functions (`utils.py`)**
- **API Integration**: World Bank API for real-time economic and demographic data
- **Data Processing**: Population projections and demographic calculations
- **Fallback Mechanisms**: Reliable estimates when APIs are unavailable

## 📈 Data Sources

### **World Bank API Endpoints**
- **GDP Data**: `NY.GDP.MKTP.CD` - India's current GDP in USD
- **GDP Growth**: `NY.GDP.MKTP.KD.ZG` - Latest GDP growth rate
- **Population**: `SP.POP.TOTL` - India's total population
- **Dependency Ratio**: `SP.POP.DPND` - Population dependency ratio
- **Youth Population**: `SP.POP.0014.TO.ZS` - Population under 14 (proxy for median age)

### **Local Data**
- **Country Comparisons**: CSV file with GDP per capita data for 200+ countries
- **Fallback Estimates**: UN World Population Prospects data for median age

## 🧮 Key Calculations

### **Required Growth Rate**
```
Growth Rate = 100 * (10^(log10(target_gdp / current_gdp) / years) - 1)
```

### **Population Projection**
Uses UN growth rates:
- 2025: 1.0% annual growth
- 2030: 0.8% annual growth  
- 2040: 0.5% annual growth
- Beyond: 0.3% annual growth

### **Median Age Estimation**
Converts population under 14% to median age:
```
Estimated Median Age = 28.5 + (25 - under_14_percentage) * 0.3
```

### **Per Capita GDP**
```
Per Capita GDP = Total GDP / Population
```

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8+
- pip package manager

### **Installation Steps**

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd thirtybyfortyseven
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv growth_dashboard_env
   source growth_dashboard_env/bin/activate  # On Windows: growth_dashboard_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run growth_counter_dashboard.py
   ```

5. **Access the dashboard**
   - Open your browser and go to `http://localhost:8501`
   - The dashboard will automatically open in your default browser

## 📋 Dependencies

### **Core Dependencies**
- `streamlit` - Web application framework
- `pandas` - Data manipulation and analysis
- `requests` - HTTP library for API calls

## 🎮 Usage Guide

### **Basic Usage**
1. **Enter Current GDP**: Use the default value or input India's current GDP in billion USD
2. **Set Target GDP**: Specify the desired GDP target in billion USD
3. **Choose Target Year**: Select the year by which you want to achieve the target
4. **View Results**: The dashboard will display:
   - Required annual growth rate
   - Comparison with current growth rate
   - Per capita GDP analysis
   - Demographic projections

### **Understanding the Results**
- **Green Indicators**: Current performance meets or exceeds required growth
- **Red Indicators**: Current performance below required growth
- **Population Categories**: 
  - Young Population: < 30 years median age
  - Middle-aged: 30-40 years median age
  - Aging Population: > 40 years median age
- **Dependency Levels**:
  - Low: < 50% dependency ratio
  - Moderate: 50-70% dependency ratio
  - High: > 70% dependency ratio

## 🔮 Future Enhancements

### **Potential Additions**
- Interactive charts and visualizations
- Historical trend analysis
- Regional comparisons within India
- Sector-wise GDP analysis
- Export functionality for reports
- Mobile-responsive design improvements

### **Data Improvements**
- Real-time median age data from World Bank
- More granular demographic projections
- Additional economic indicators
- International comparison enhancements

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### **Code Standards**
- Follow PEP 8 style guidelines
- Add docstrings for new functions
- Include error handling
- Test API integrations

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions, issues, or contributions:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common solutions

## 🔗 Related Resources

- [World Bank API Documentation](https://datahelpdesk.worldbank.org/knowledgebase/articles/889386-developer-information-overview)
- [UN World Population Prospects](https://population.un.org/wpp/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

**Note**: This dashboard is designed for educational and research purposes. For official economic analysis, please consult with professional economists and use official government data sources. 