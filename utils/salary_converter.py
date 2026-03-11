# utils/salary_converter.py

class SalaryConverter:
    """Convert salaries based on country and role."""

    BASE_SALARIES = {
        'data_analyst':       {'entry': 55000, 'junior': 65000, 'mid': 85000,  'senior': 110000, 'lead': 140000},
        'software_developer': {'entry': 60000, 'junior': 75000, 'mid': 95000,  'senior': 120000, 'lead': 150000},
        'data_scientist':     {'entry': 70000, 'junior': 85000, 'mid': 110000, 'senior': 140000, 'lead': 170000},
    }

    COUNTRY_FACTORS = {
        'US': 1.0, 'UK': 0.8, 'Canada': 0.85, 'Australia': 0.9,
        'Germany': 0.75, 'France': 0.7, 'India': 0.3,
        'Singapore': 0.7, 'UAE': 0.9, 'Remote': 0.8,
    }

    CURRENCIES = {
        'US': ('$', 1), 'UK': ('£', 0.79), 'India': ('₹', 83.0),
        'Canada': ('C$', 1.35), 'Australia': ('A$', 1.52),
        'Germany': ('€', 0.92), 'France': ('€', 0.92),
        'Singapore': ('S$', 1.35), 'UAE': ('AED', 3.67), 'Remote': ('$', 1),
    }

    @classmethod
    def convert_salary(cls, role: str, experience: str, country: str = 'India') -> str:
        role_key = cls._get_role_key(role)
        exp_key = cls._get_experience_key(experience)
        country_key = country if country in cls.COUNTRY_FACTORS else 'India'

        base = cls.BASE_SALARIES.get(role_key, {}).get(exp_key, 60000)
        adjusted = base * cls.COUNTRY_FACTORS[country_key]
        symbol, rate = cls.CURRENCIES[country_key]
        local = adjusted * rate

        low, high = local * 0.8, local * 1.2
        if country_key == 'India':
            return f"{symbol}{low/100000:.1f}L - {symbol}{high/100000:.1f}L PA"
        return f"{symbol}{low:,.0f} - {symbol}{high:,.0f}"

    @classmethod
    def _get_role_key(cls, role: str) -> str:
        r = role.lower()
        if 'scientist' in r: return 'data_scientist'
        if 'analyst' in r:   return 'data_analyst'
        return 'software_developer'

    @classmethod
    def _get_experience_key(cls, experience: str) -> str:
        e = experience.lower()
        if 'entry' in e:             return 'entry'
        if 'junior' in e:            return 'junior'
        if 'senior' in e:            return 'senior'
        if 'lead' in e or 'principal' in e: return 'lead'
        return 'mid'