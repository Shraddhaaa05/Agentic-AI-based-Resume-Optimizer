# utils/salary_converter.py
class SalaryConverter:
    """Convert salaries based on country and role"""
    
    # Base salaries in USD for different roles and levels
    BASE_SALARIES = {
        'data_analyst': {
            'entry': 55000,
            'junior': 65000,
            'mid': 85000,
            'senior': 110000,
            'lead': 140000
        },
        'software_developer': {
            'entry': 60000,
            'junior': 75000,
            'mid': 95000,
            'senior': 120000,
            'lead': 150000
        },
        'data_scientist': {
            'entry': 70000,
            'junior': 85000,
            'mid': 110000,
            'senior': 140000,
            'lead': 170000
        }
    }
    
    # Country adjustment factors (multiplier from USD)
    COUNTRY_FACTORS = {
        'US': 1.0,
        'UK': 0.8,
        'Canada': 0.85,
        'Australia': 0.9,
        'Germany': 0.75,
        'France': 0.7,
        'India': 0.3,  # 30% of US salaries
        'Singapore': 0.7,
        'UAE': 0.9,
        'Remote': 0.8
    }
    
    # Currency symbols and conversions
    CURRENCIES = {
        'US': ('$', 1),
        'UK': ('£', 0.79),
        'India': ('₹', 83.0),  # INR to USD
        'Canada': ('C$', 1.35),
        'Australia': ('A$', 1.52),
        'Germany': ('€', 0.92),
        'France': ('€', 0.92),
        'Singapore': ('S$', 1.35),
        'UAE': ('AED', 3.67),
        'Remote': ('$', 1)
    }
    
    @classmethod
    def convert_salary(cls, role: str, experience: str, country: str = 'India') -> str:
        """Convert salary based on role, experience level, and country"""
        role_key = cls._get_role_key(role)
        exp_key = cls._get_experience_key(experience)
        country_key = country if country in cls.COUNTRY_FACTORS else 'India'
        
        # Get base salary in USD
        base_salary = cls.BASE_SALARIES.get(role_key, {}).get(exp_key, 60000)
        
        # Apply country factor
        adjusted_salary = base_salary * cls.COUNTRY_FACTORS[country_key]
        
        # Convert to local currency
        currency_symbol, conversion_rate = cls.CURRENCIES[country_key]
        local_salary = adjusted_salary * conversion_rate
        
        # Format salary range (±20%)
        low_end = local_salary * 0.8
        high_end = local_salary * 1.2
        
        if country_key == 'India':
            # Format INR salaries in lakhs
            low_lakhs = low_end / 100000
            high_lakhs = high_end / 100000
            return f"{currency_symbol}{low_lakhs:.1f}L - {currency_symbol}{high_lakhs:.1f}L PA"
        else:
            # Format other currencies normally
            return f"{currency_symbol}{low_end:,.0f} - {currency_symbol}{high_end:,.0f}"
    
    @classmethod
    def _get_role_key(cls, role: str) -> str:
        """Map role to salary key"""
        role_lower = role.lower()
        if 'data' in role_lower and 'scientist' in role_lower:
            return 'data_scientist'
        elif 'data' in role_lower and 'analyst' in role_lower:
            return 'data_analyst'
        elif 'developer' in role_lower or 'engineer' in role_lower:
            return 'software_developer'
        else:
            return 'data_analyst'  # Default
    
    @classmethod
    def _get_experience_key(cls, experience: str) -> str:
        """Map experience level to key"""
        exp_lower = experience.lower()
        if 'entry' in exp_lower:
            return 'entry'
        elif 'junior' in exp_lower:
            return 'junior'
        elif 'senior' in exp_lower:
            return 'senior'
        elif 'lead' in exp_lower or 'principal' in exp_lower:
            return 'lead'
        else:
            return 'mid'