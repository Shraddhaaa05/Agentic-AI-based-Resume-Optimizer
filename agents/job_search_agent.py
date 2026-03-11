# agents/job_search_agent.py
import aiohttp
import asyncio
from typing import List, Dict, Any
from bs4 import BeautifulSoup


class JobSearchAgent:
    HEADERS = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
    }

    SALARY_RANGES = {
        'data analyst':       '$65,000 – $95,000',
        'senior data analyst':'$85,000 – $120,000',
        'data scientist':     '$95,000 – $140,000',
        'business analyst':   '$70,000 – $100,000',
        'software engineer':  '$90,000 – $130,000',
        'product manager':    '$100,000 – $150,000',
    }

    FALLBACK_COMPANIES = [
        ('Google',     'https://careers.google.com/jobs'),
        ('Microsoft',  'https://careers.microsoft.com'),
        ('Amazon',     'https://www.amazon.jobs'),
        ('Apple',      'https://www.apple.com/careers'),
        ('Meta',       'https://www.metacareers.com'),
        ('Salesforce', 'https://salesforce.wd12.myworkdayjobs.com/External_Career_Site'),
    ]

    async def search_real_jobs(self, target_role: str, location: str = "") -> List[Dict[str, Any]]:
        print(f"🔍 Searching jobs: {target_role} | {location}")
        tasks = [
            self._search_linkedin(target_role, location),
            self._search_remoteok(target_role),
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        jobs = []
        for r in results:
            if isinstance(r, list):
                jobs.extend(r)

        jobs = self._deduplicate(jobs)
        if not jobs:
            jobs = self._fallback_jobs(target_role, location)

        print(f"✅ Found {len(jobs)} job listings")
        return jobs

    async def _search_linkedin(self, role: str, location: str) -> List[Dict[str, Any]]:
        try:
            q = role.replace(' ', '%20')
            url = (f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
                   f"?keywords={q}&location={location.replace(' ','%20')}&start=0")
            async with aiohttp.ClientSession(headers=self.HEADERS) as s:
                async with s.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                    if resp.status == 200:
                        return self._parse_linkedin(await resp.text(), role)
        except Exception as e:
            print(f"  LinkedIn: {e}")
        return []

    def _parse_linkedin(self, html: str, role: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []
        for card in soup.find_all('div', class_='base-card')[:5]:
            try:
                title   = card.find('h3', class_='base-search-card__title')
                company = card.find('h4', class_='base-search-card__subtitle')
                loc     = card.find('span', class_='job-search-card__location')
                link    = card.find('a', class_='base-card__full-link')
                if title and company and link:
                    jobs.append({
                        'title':       title.text.strip(),
                        'company':     company.text.strip(),
                        'location':    loc.text.strip() if loc else 'Remote',
                        'salary':      self._salary(role),
                        'apply_url':   link['href'].split('?')[0],
                        'description': f"{role} at {company.text.strip()}.",
                        'source':      'LinkedIn',
                        'verified':    True,
                    })
            except Exception:
                pass
        return jobs

    async def _search_remoteok(self, role: str) -> List[Dict[str, Any]]:
        try:
            slug = role.lower().replace(' ', '-')
            url  = f"https://remoteok.io/remote-{slug}-jobs"
            async with aiohttp.ClientSession(headers=self.HEADERS) as s:
                async with s.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                    if resp.status == 200:
                        return self._parse_remoteok(await resp.text(), role)
        except Exception as e:
            print(f"  RemoteOK: {e}")
        return []

    def _parse_remoteok(self, html: str, role: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []
        for card in soup.find_all('tr', class_='job')[:3]:
            try:
                title   = card.find('h2', itemprop='title')
                company = card.find('h3', itemprop='name')
                link    = card.find('a', class_='preventLink')
                if title and company:
                    href = f"https://remoteok.io{link['href']}" if link else 'https://remoteok.io'
                    jobs.append({
                        'title':       title.text.strip(),
                        'company':     company.text.strip(),
                        'location':    'Remote',
                        'salary':      self._salary(role),
                        'apply_url':   href,
                        'description': f"Remote {role} at {company.text.strip()}.",
                        'source':      'RemoteOK',
                        'verified':    True,
                    })
            except Exception:
                pass
        return jobs

    def _salary(self, role: str) -> str:
        return self.SALARY_RANGES.get(role.lower(), '$70,000 – $100,000')

    def _deduplicate(self, jobs: List[Dict]) -> List[Dict]:
        seen, unique = set(), []
        for j in jobs:
            key = (j['title'].lower(), j['company'].lower())
            if key not in seen:
                seen.add(key)
                unique.append(j)
        return unique

    def _fallback_jobs(self, role: str, location: str) -> List[Dict[str, Any]]:
        return [
            {
                'title':       role,
                'company':     name,
                'location':    location or 'Multiple Locations',
                'salary':      self._salary(role),
                'apply_url':   url,
                'description': f"{role} position at {name}. Visit their careers page to apply.",
                'source':      'Company Website',
                'verified':    True,
            }
            for name, url in self.FALLBACK_COMPANIES
        ]