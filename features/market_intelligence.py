# features/market_intelligence.py
class MarketIntelligenceAgent:
    def get_market_insights(self, target_role: str, location: str = "") -> dict:
        return {
            'salary_range':   '$65,000 – $95,000',
            'demand_level':   'High',
            'top_companies':  ['Google','Microsoft','Amazon','Salesforce'],
            'required_skills':['SQL','Python','Tableau','Statistics'],
            'growth_outlook': '22% growth expected over 5 years',
        }