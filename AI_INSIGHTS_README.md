# Dynamic AI Insights for Sector Analysis

This feature provides dynamic, AI-powered insights for India's GDP sector distribution analysis.

## Features

### 🔄 **Dynamic Insights**
- **Contextual Analysis**: Insights adapt based on sector rankings, percentages, and year
- **Real-time Updates**: Insights change as data updates
- **Sector-specific**: Each sector gets tailored analysis

### 🤖 **Multiple LLM Providers**
- **Enhanced Static**: Smart contextual insights (default)
- **OpenAI GPT**: Real AI-powered insights (requires API key)
- **Hugging Face**: Alternative AI provider (requires API key)
- **Local LLM**: Run locally with Ollama (requires local setup)

## Configuration

### 1. **Basic Setup** (Enhanced Static - Recommended)
```python
# In ai_config.py
LLM_PROVIDER = "enhanced_static"
```

### 2. **OpenAI GPT Setup**
```python
# In ai_config.py
LLM_PROVIDER = "openai"

# Set environment variable
export OPENAI_API_KEY="your_api_key_here"
```

### 3. **Hugging Face Setup**
```python
# In ai_config.py
LLM_PROVIDER = "huggingface"

# Set environment variable
export HUGGINGFACE_API_KEY="your_api_key_here"
```

### 4. **Local LLM Setup (Ollama)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2

# In ai_config.py
LLM_PROVIDER = "local_llm"
LOCAL_LLM_MODEL = "llama2"
```

## Usage

### **Automatic Integration**
The insights are automatically integrated into the sunburst chart. No additional code needed!

### **Manual Usage**
```python
from ai_insights import get_ai_insight

# Get insight for a sector
insight = get_ai_insight("Manufacturing", 13.0, sector_data)
print(insight)
# Output: "Manufacturing gap (13.0%) - below 25% target for economic development. Currently 2nd largest sector."
```

## Example Insights

### **Enhanced Static Insights** (Current)
- **Agriculture**: "Moderate agriculture (16.2%) - balanced sector typical of emerging economies. Ranks 2nd in GDP contribution."
- **Manufacturing**: "Manufacturing gap (13.0%) - below 25% target for economic development. Currently 2nd largest sector."
- **Services**: "Diverse services (58.0%) - includes IT, education, healthcare, and emerging sectors. 1st largest sector."

### **AI-Powered Insights** (with OpenAI)
- More nuanced analysis
- Real-time economic context
- Actionable recommendations

## Benefits

### 📊 **Data-Driven**
- Insights based on actual sector rankings
- Contextual percentage analysis
- Year-specific information

### 🎯 **Actionable**
- Clear economic implications
- Development stage analysis
- Growth potential insights

### 🔧 **Flexible**
- Easy to switch between providers
- Configurable insight styles
- Extensible for new sectors

## File Structure

```
├── ai_insights.py          # Main AI insights module
├── ai_config.py            # Configuration settings
├── plotting_utils.py       # Updated with dynamic insights
└── AI_INSIGHTS_README.md   # This file
```

## Troubleshooting

### **API Key Issues**
- Ensure environment variables are set correctly
- Check API key validity
- Verify provider configuration

### **Local LLM Issues**
- Ensure Ollama is running: `ollama serve`
- Check model availability: `ollama list`
- Verify local URL in config

### **Fallback Behavior**
- All providers fallback to enhanced static insights
- No errors will break the application
- Graceful degradation ensures functionality

## Future Enhancements

- [ ] **Multi-language Support**: Insights in different languages
- [ ] **Historical Analysis**: Compare insights across years
- [ ] **Custom Models**: Fine-tuned models for economic analysis
- [ ] **Real-time Updates**: Live insights as data changes
- [ ] **Interactive Insights**: Click to get detailed analysis 