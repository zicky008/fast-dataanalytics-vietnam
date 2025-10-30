"""
Vietnam Benchmark Data Loader
Loads 300+ realistic Vietnam market benchmarks from CSV files
Domains: HR, Marketing, E-commerce, Sales
"""

import pandas as pd
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class VietnamBenchmarkLoader:
    """
    Loads and provides access to Vietnam benchmark data from CSV files.

    Files loaded:
    - vietnam_hr_salary_benchmarks_2024.csv (48 roles)
    - vietnam_marketing_benchmarks_2024.csv (85+ metrics)
    - vietnam_ecommerce_benchmarks_2024.csv (95+ metrics)
    - vietnam_sales_benchmarks_2024.csv (97+ metrics)
    """

    def __init__(self, sample_data_path: Optional[str] = None):
        """
        Initialize benchmark loader.

        Args:
            sample_data_path: Path to sample_data directory.
                            If None, auto-detects from project structure.
        """
        if sample_data_path is None:
            # Auto-detect: Look for sample_data relative to this file
            current_dir = Path(__file__).parent
            sample_data_path = current_dir.parent / "sample_data"

        self.sample_data_path = Path(sample_data_path)

        # Benchmark dataframes
        self.hr_benchmarks = None
        self.marketing_benchmarks = None
        self.ecommerce_benchmarks = None
        self.sales_benchmarks = None

        # Load status
        self.loaded = False
        self.load_errors = []

    def load_all_benchmarks(self) -> Dict[str, bool]:
        """
        Load all 4 Vietnam benchmark CSV files.

        Returns:
            Dict with load status for each file: {'hr': True, 'marketing': False, ...}
        """
        status = {}

        # HR Benchmarks
        hr_path = self.sample_data_path / "vietnam_hr_salary_benchmarks_2024.csv"
        try:
            self.hr_benchmarks = pd.read_csv(hr_path)
            status['hr'] = True
        except Exception as e:
            self.load_errors.append(f"HR: {str(e)}")
            status['hr'] = False

        # Marketing Benchmarks
        marketing_path = self.sample_data_path / "vietnam_marketing_benchmarks_2024.csv"
        try:
            self.marketing_benchmarks = pd.read_csv(marketing_path)
            status['marketing'] = True
        except Exception as e:
            self.load_errors.append(f"Marketing: {str(e)}")
            status['marketing'] = False

        # E-commerce Benchmarks
        ecommerce_path = self.sample_data_path / "vietnam_ecommerce_benchmarks_2024.csv"
        try:
            self.ecommerce_benchmarks = pd.read_csv(ecommerce_path)
            status['ecommerce'] = True
        except Exception as e:
            self.load_errors.append(f"E-commerce: {str(e)}")
            status['ecommerce'] = False

        # Sales Benchmarks
        sales_path = self.sample_data_path / "vietnam_sales_benchmarks_2024.csv"
        try:
            self.sales_benchmarks = pd.read_csv(sales_path)
            status['sales'] = True
        except Exception as e:
            self.load_errors.append(f"Sales: {str(e)}")
            status['sales'] = False

        self.loaded = any(status.values())
        return status

    def get_hr_salary_benchmark(
        self,
        role: str = None,
        city: str = None,
        experience_level: str = None
    ) -> Optional[pd.DataFrame]:
        """
        Get HR salary benchmarks filtered by role, city, experience.

        Args:
            role: Job role (e.g., "Software Engineer", "HR Manager")
            city: City (e.g., "Ho Chi Minh", "Hanoi")
            experience_level: Experience (e.g., "3-5 years", "5-7 years")

        Returns:
            Filtered DataFrame or None if no data loaded
        """
        if self.hr_benchmarks is None:
            return None

        df = self.hr_benchmarks.copy()

        if role:
            df = df[df['role'].str.contains(role, case=False, na=False)]
        if city:
            df = df[df['city'].str.contains(city, case=False, na=False)]
        if experience_level:
            df = df[df['experience_level'] == experience_level]

        return df if len(df) > 0 else None

    def get_marketing_benchmark(
        self,
        metric_name: str = None,
        channel: str = None,
        industry: str = None
    ) -> Optional[pd.DataFrame]:
        """
        Get marketing benchmarks filtered by metric, channel, industry.

        Args:
            metric_name: Metric (e.g., "CPA", "CTR", "ROAS")
            channel: Channel (e.g., "Facebook Ads", "Google Ads", "TikTok Ads")
            industry: Industry (e.g., "E-commerce", "SaaS", "Education")

        Returns:
            Filtered DataFrame or None if no data loaded
        """
        if self.marketing_benchmarks is None:
            return None

        df = self.marketing_benchmarks.copy()

        if metric_name:
            df = df[df['metric_name'].str.contains(metric_name, case=False, na=False)]
        if channel:
            df = df[df['channel'].str.contains(channel, case=False, na=False)]
        if industry:
            df = df[df['industry'].str.contains(industry, case=False, na=False)]

        return df if len(df) > 0 else None

    def get_ecommerce_benchmark(
        self,
        metric_name: str = None,
        category: str = None,
        platform: str = None
    ) -> Optional[pd.DataFrame]:
        """
        Get e-commerce benchmarks filtered by metric, category, platform.

        Args:
            metric_name: Metric (e.g., "AOV", "Conversion Rate", "Cart Abandonment")
            category: Category (e.g., "Fashion", "Electronics", "Beauty")
            platform: Platform (e.g., "Shopee", "Lazada", "TikTok Shop")

        Returns:
            Filtered DataFrame or None if no data loaded
        """
        if self.ecommerce_benchmarks is None:
            return None

        df = self.ecommerce_benchmarks.copy()

        if metric_name:
            df = df[df['metric_name'].str.contains(metric_name, case=False, na=False)]
        if category:
            df = df[df['category'].str.contains(category, case=False, na=False)]
        if platform:
            df = df[df['platform'].str.contains(platform, case=False, na=False)]

        return df if len(df) > 0 else None

    def get_sales_benchmark(
        self,
        metric_name: str = None,
        sales_type: str = None,
        industry: str = None
    ) -> Optional[pd.DataFrame]:
        """
        Get sales benchmarks filtered by metric, type, industry.

        Args:
            metric_name: Metric (e.g., "Win Rate", "Sales Cycle", "Deal Size")
            sales_type: Type (e.g., "B2B", "B2C")
            industry: Industry (e.g., "Software (SaaS)", "Consulting", "Real Estate")

        Returns:
            Filtered DataFrame or None if no data loaded
        """
        if self.sales_benchmarks is None:
            return None

        df = self.sales_benchmarks.copy()

        if metric_name:
            df = df[df['metric_name'].str.contains(metric_name, case=False, na=False)]
        if sales_type:
            df = df[df['sales_type'] == sales_type]
        if industry:
            df = df[df['industry'].str.contains(industry, case=False, na=False)]

        return df if len(df) > 0 else None

    def compare_value_to_benchmark(
        self,
        domain: str,
        metric_name: str,
        user_value: float,
        filters: Dict[str, str] = None
    ) -> Optional[Dict]:
        """
        Compare user's metric value against Vietnam benchmark.

        Args:
            domain: 'hr', 'marketing', 'ecommerce', or 'sales'
            metric_name: Name of the metric to compare
            user_value: User's actual value
            filters: Additional filters (e.g., {'city': 'Ho Chi Minh', 'role': 'Developer'})

        Returns:
            Dict with comparison results:
            {
                'user_value': 85000,
                'benchmark_median': 82000,
                'benchmark_q1': 65000,
                'benchmark_q3': 110000,
                'percentile': 55,  # User is at 55th percentile
                'status': 'above_average',  # or 'average', 'below_average', 'excellent'
                'message': 'Cao hơn 55% thị trường Vietnam'
            }
        """
        filters = filters or {}

        # Get benchmark data
        if domain == 'hr':
            benchmark_df = self.get_hr_salary_benchmark(**filters)
        elif domain == 'marketing':
            benchmark_df = self.get_marketing_benchmark(metric_name=metric_name, **filters)
        elif domain == 'ecommerce':
            benchmark_df = self.get_ecommerce_benchmark(metric_name=metric_name, **filters)
        elif domain == 'sales':
            benchmark_df = self.get_sales_benchmark(metric_name=metric_name, **filters)
        else:
            return None

        if benchmark_df is None or len(benchmark_df) == 0:
            return None

        # Extract benchmark values (try different column names)
        # For HR: median_salary_vnd_monthly, percentile_25, percentile_75
        # For others: median_value, percentile_25, percentile_75

        median_col = None
        q1_col = None
        q3_col = None

        for col in benchmark_df.columns:
            if 'median' in col.lower():
                median_col = col
            elif '25' in col or 'q1' in col.lower():
                q1_col = col
            elif '75' in col or 'q3' in col.lower():
                q3_col = col

        if median_col is None:
            return None

        # Get benchmark values (take first row if multiple matches)
        benchmark_median = benchmark_df[median_col].iloc[0]
        benchmark_q1 = benchmark_df[q1_col].iloc[0] if q1_col else benchmark_median * 0.8
        benchmark_q3 = benchmark_df[q3_col].iloc[0] if q3_col else benchmark_median * 1.2

        # Calculate percentile (approximate)
        if user_value <= benchmark_q1:
            percentile = 25 * (user_value / benchmark_q1)
        elif user_value <= benchmark_median:
            percentile = 25 + 25 * ((user_value - benchmark_q1) / (benchmark_median - benchmark_q1))
        elif user_value <= benchmark_q3:
            percentile = 50 + 25 * ((user_value - benchmark_median) / (benchmark_q3 - benchmark_median))
        else:
            percentile = 75 + 25 * min((user_value - benchmark_q3) / (benchmark_q3 - benchmark_median), 1)

        # Determine status
        if percentile >= 75:
            status = 'excellent'
            message = f'Xuất sắc! Cao hơn {percentile:.0f}% thị trường Vietnam'
        elif percentile >= 50:
            status = 'above_average'
            message = f'Tốt! Cao hơn {percentile:.0f}% thị trường Vietnam'
        elif percentile >= 25:
            status = 'average'
            message = f'Trung bình thị trường Vietnam ({percentile:.0f}th percentile)'
        else:
            status = 'below_average'
            message = f'Thấp hơn {100-percentile:.0f}% thị trường Vietnam'

        return {
            'user_value': user_value,
            'benchmark_median': benchmark_median,
            'benchmark_q1': benchmark_q1,
            'benchmark_q3': benchmark_q3,
            'percentile': percentile,
            'status': status,
            'message': message,
            'benchmark_source': benchmark_df['source'].iloc[0] if 'source' in benchmark_df.columns else 'Vietnam Market Data 2024',
            'vietnam_context': benchmark_df['notes'].iloc[0] if 'notes' in benchmark_df.columns else ''
        }

    def get_domain_summary(self, domain: str) -> Dict:
        """
        Get summary statistics for a domain's benchmarks.

        Args:
            domain: 'hr', 'marketing', 'ecommerce', or 'sales'

        Returns:
            Dict with summary: {'total_metrics': 85, 'industries': [...], 'last_updated': '2024-12'}
        """
        if domain == 'hr' and self.hr_benchmarks is not None:
            df = self.hr_benchmarks
            return {
                'total_roles': len(df),
                'cities': df['city'].unique().tolist(),
                'industries': df['industry'].unique().tolist(),
                'experience_levels': df['experience_level'].unique().tolist(),
                'last_updated': df['last_updated'].iloc[0] if 'last_updated' in df.columns else '2024-12'
            }
        elif domain == 'marketing' and self.marketing_benchmarks is not None:
            df = self.marketing_benchmarks
            return {
                'total_metrics': len(df),
                'channels': df['channel'].unique().tolist(),
                'industries': df['industry'].unique().tolist(),
                'last_updated': df['last_updated'].iloc[0] if 'last_updated' in df.columns else '2024-12'
            }
        elif domain == 'ecommerce' and self.ecommerce_benchmarks is not None:
            df = self.ecommerce_benchmarks
            return {
                'total_metrics': len(df),
                'platforms': df['platform'].unique().tolist() if 'platform' in df.columns else [],
                'categories': df['category'].unique().tolist(),
                'last_updated': df['last_updated'].iloc[0] if 'last_updated' in df.columns else '2024-12'
            }
        elif domain == 'sales' and self.sales_benchmarks is not None:
            df = self.sales_benchmarks
            return {
                'total_metrics': len(df),
                'sales_types': df['sales_type'].unique().tolist(),
                'industries': df['industry'].unique().tolist(),
                'last_updated': df['last_updated'].iloc[0] if 'last_updated' in df.columns else '2024-12'
            }
        else:
            return {}


# Singleton instance for easy import
_benchmark_loader = None

def get_benchmark_loader() -> VietnamBenchmarkLoader:
    """
    Get singleton instance of VietnamBenchmarkLoader.
    Automatically loads all benchmarks on first call.

    Returns:
        VietnamBenchmarkLoader instance with data loaded
    """
    global _benchmark_loader
    if _benchmark_loader is None:
        _benchmark_loader = VietnamBenchmarkLoader()
        _benchmark_loader.load_all_benchmarks()
    return _benchmark_loader


# Quick test if run directly
if __name__ == "__main__":
    loader = VietnamBenchmarkLoader()
    status = loader.load_all_benchmarks()

    print("📊 Vietnam Benchmark Loader - Load Status:")
    print(f"✅ HR Benchmarks: {status.get('hr', False)} ({len(loader.hr_benchmarks) if loader.hr_benchmarks is not None else 0} rows)")
    print(f"✅ Marketing Benchmarks: {status.get('marketing', False)} ({len(loader.marketing_benchmarks) if loader.marketing_benchmarks is not None else 0} rows)")
    print(f"✅ E-commerce Benchmarks: {status.get('ecommerce', False)} ({len(loader.ecommerce_benchmarks) if loader.ecommerce_benchmarks is not None else 0} rows)")
    print(f"✅ Sales Benchmarks: {status.get('sales', False)} ({len(loader.sales_benchmarks) if loader.sales_benchmarks is not None else 0} rows)")

    if loader.load_errors:
        print(f"\n❌ Errors: {loader.load_errors}")

    # Test HR lookup
    print("\n🧪 Test: HR Salary for Software Engineer in HCMC")
    hr_data = loader.get_hr_salary_benchmark(role="Software Engineer", city="Ho Chi Minh")
    if hr_data is not None and len(hr_data) > 0:
        print(f"Found {len(hr_data)} matching roles")
        print(hr_data[['role', 'city', 'experience_level', 'median_salary_vnd_monthly']].head())

    # Test comparison
    print("\n🧪 Test: Compare user's CPA against Vietnam benchmark")
    comparison = loader.compare_value_to_benchmark(
        domain='marketing',
        metric_name='CPA',
        user_value=95000,
        filters={'channel': 'Facebook Ads', 'industry': 'E-commerce'}
    )
    if comparison:
        print(f"User value: {comparison['user_value']:,.0f} VND")
        print(f"Benchmark median: {comparison['benchmark_median']:,.0f} VND")
        print(f"Status: {comparison['status']}")
        print(f"Message: {comparison['message']}")
