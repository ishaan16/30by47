import os
import requests
from typing import Dict, Any, Optional
import json
from ai_config import LLM_PROVIDER, LOCAL_LLM_URL, LOCAL_LLM_MODEL


def get_ai_insight(sector_name: str, percentage: float, sector_data: Dict[str, Any]) -> str:
    """
    Get AI-powered insight for a sector using the configured LLM provider.
    
    Args:
        sector_name: Name of the sector
        percentage: Percentage contribution of the sector
        sector_data: Complete sector data for context
        
    Returns:
        str: AI-generated insight
    """
    if LLM_PROVIDER == "openai":
        return get_openai_insight(sector_name, percentage, sector_data)
    elif LLM_PROVIDER == "huggingface":
        return get_huggingface_insight(sector_name, percentage, sector_data)
    elif LLM_PROVIDER == "local_llm":
        return get_local_llm_insight(sector_name, percentage, sector_data)
    else:
        # Default to enhanced static insights
        return get_enhanced_static_insight(sector_name, percentage, sector_data)


def get_enhanced_static_insight(sector_name: str, percentage: float, sector_data: Dict[str, Any]) -> str:
    """
    Enhanced static insights with more contextual analysis.
    This provides dynamic insights based on sector performance and context.
    """
    sector_lower = sector_name.lower().replace(' ', '_')
    
    # Get overall context
    year = list(sector_data.values())[0].get('year', 2023) if sector_data else 2023
    
    # Get sector-specific insights with dynamic context
    if sector_lower == 'agriculture':
        if percentage > 25:
            return f"High agriculture dependence ({percentage:.1f}%) - typical of developing economies with strong rural employment."
        elif percentage < 10:
            return f"Low agriculture share ({percentage:.1f}%) - India has successfully transitioned to industrialization and services."
        else:
            return f"Moderate agriculture ({percentage:.1f}%) - balanced sector typical of emerging economies."
    
    elif sector_lower == 'manufacturing':
        if percentage < 15:
            return f"Manufacturing gap ({percentage:.1f}%) - below 25% target for economic development and job creation."
        elif percentage > 25:
            return f"Strong manufacturing ({percentage:.1f}%) - well-developed and competitive sector driving exports."
        else:
            return f"Growing manufacturing ({percentage:.1f}%) - shows positive development trends and industrialization."
    
    elif sector_lower == 'construction':
        strength = "strong" if percentage > 7 else "moderate"
        return f"Infrastructure development ({percentage:.1f}%) - shows {strength} construction activity and urbanization."
    
    elif sector_lower == 'mining':
        return f"Resource extraction ({percentage:.1f}%) - essential for industrial inputs and energy production."
    
    elif sector_lower == 'utilities':
        return f"Critical infrastructure ({percentage:.1f}%) - power and water supply essential for economic growth."
    
    elif sector_lower == 'trade_hotels':
        return f"Domestic consumption ({percentage:.1f}%) - key driver of tourism and retail services."
    
    elif sector_lower == 'financial_services':
        strength = "strong" if percentage > 7 else "moderate"
        return f"Financial markets ({percentage:.1f}%) - shows {strength} financial sector development and capital access."
    
    elif sector_lower == 'real_estate':
        return f"Urban development ({percentage:.1f}%) - important for investment and housing market growth."
    
    elif sector_lower == 'public_admin':
        return f"Government services ({percentage:.1f}%) - public sector employment and administrative support."
    
    elif sector_lower == 'other_services':
        return f"Diverse services ({percentage:.1f}%) - includes IT, education, healthcare, and emerging sectors."
    
    else:
        return f"{sector_name} sector ({percentage:.1f}%) - contributes to economic diversification and growth."


def get_openai_insight(sector_name: str, percentage: float, sector_data: Dict[str, Any]) -> str:
    """
    Get insight using OpenAI GPT API.
    Requires OPENAI_API_KEY environment variable.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return get_enhanced_static_insight(sector_name, percentage, sector_data)
    
    prompt = f"""
    Analyze India's {sector_name} sector which contributes {percentage:.1f}% to GDP.
    
    Context:
    - Year: {list(sector_data.values())[0].get('year', 2023)}
    - Total sectors: {len(sector_data)}
    - Sector data: {json.dumps(sector_data, indent=2)}
    
    Provide a brief, insightful analysis (1-2 sentences) about this sector's:
    1. Current performance and significance
    2. Development stage and potential
    3. Economic implications for India
    
    Focus on being informative and actionable.
    """
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 150,
                "temperature": 0.7
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            return get_enhanced_static_insight(sector_name, percentage, sector_data)
            
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return get_enhanced_static_insight(sector_name, percentage, sector_data)


def get_huggingface_insight(sector_name: str, percentage: float, sector_data: Dict[str, Any]) -> str:
    """
    Get insight using Hugging Face API.
    Requires HUGGINGFACE_API_KEY environment variable.
    """
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key:
        return get_enhanced_static_insight(sector_name, percentage, sector_data)
    
    prompt = f"Analyze India's {sector_name} sector ({percentage:.1f}% of GDP) in {list(sector_data.values())[0].get('year', 2023)}. Provide brief economic insight:"
    
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"inputs": prompt},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result[0]['generated_text'][len(prompt):].strip()
        else:
            return get_enhanced_static_insight(sector_name, percentage, sector_data)
            
    except Exception as e:
        print(f"Hugging Face API error: {e}")
        return get_enhanced_static_insight(sector_name, percentage, sector_data)


def get_local_llm_insight(sector_name: str, percentage: float, sector_data: Dict[str, Any]) -> str:
    """
    Get insight using local LLM (e.g., Ollama).
    Requires Ollama to be running locally.
    """
    prompt = f"""
    Analyze India's {sector_name} sector which contributes {percentage:.1f}% to GDP in {list(sector_data.values())[0].get('year', 2023)}.
    
    Provide a brief, insightful economic analysis (1-2 sentences) about this sector's performance and significance for India's economy.
    """
    
    try:
        response = requests.post(
            LOCAL_LLM_URL,
            json={
                "model": LOCAL_LLM_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['response'].strip()
        else:
            return get_enhanced_static_insight(sector_name, percentage, sector_data)
            
    except Exception as e:
        print(f"Local LLM error: {e}")
        return get_enhanced_static_insight(sector_name, percentage, sector_data) 