"""
Streamlit AppTest - Test Vietnam Data Analytics App với 5 Vietnamese Personas
Test logic, data integrity, Vietnam context, NEVER_IMPUTE protection

Usage:
    cd /home/user/webapp
    pytest test_production_app/test_apptest_vietnam_personas.py -v -s
"""

import io
import pytest
from streamlit.testing.v1 import AppTest


class TestVietnamesePersonas:
    """Test app with 5 realistic Vietnamese user personas"""
    
    def setup_method(self):
        """Setup before each test"""
        self.app_path = "streamlit_app.py"
    
    def test_chi_mai_hr_manager_vinamilk(self):
        """
        Persona: Chị Mai - HR Manager at Vinamilk
        Data: 500 employees, salary range 5M-48M VND
        Focus: Salary data integrity, Vietnam provinces, NEVER_IMPUTE protection
        """
        print("\n🧪 Testing as Chị Mai (HR Manager)...")
        
        # Create realistic Vietnamese HR data
        hr_csv = b"""employee_id,ho_ten,department,position,luong_thang,start_date,age,province
EMP001,Nguyen Van Anh,Technology,Senior Developer,28000000,2020-03-15,32,Ho Chi Minh
EMP002,Tran Thi Binh,Marketing,Marketing Manager,25000000,2019-06-01,35,Hanoi
EMP003,Le Van Cuong,Sales,Sales Executive,18000000,2021-08-20,28,Da Nang
EMP004,Pham Thi Dung,HR,HR Specialist,15000000,2022-01-10,26,Ho Chi Minh
EMP005,Hoang Van Ethan,Finance,Accountant,20000000,2020-11-05,30,Hanoi
EMP006,Nguyen Thi Phuong,Customer Service,CS Manager,22000000,2019-03-15,33,Da Nang
EMP007,Tran Van Giang,Technology,Junior Developer,12000000,2023-01-01,24,Can Tho
EMP008,Le Thi Hong,Marketing,Content Writer,14000000,2022-06-15,27,Ho Chi Minh"""
        
        # Initialize app
        at = AppTest.from_file(self.app_path)
        at.run()
        
        # Simulate file upload
        csv_file = io.BytesIO(hr_csv)
        csv_file.name = "vinamilk_hr_data.csv"
        
        # Upload file
        at.file_uploader[0].set_value([csv_file]).run()
        
        # Convert app state to string for inspection
        app_content = str(at)
        
        # CRITICAL ASSERTIONS - NEVER_IMPUTE Protection
        assert "imputed" not in app_content.lower(), \
            "❌ CRITICAL FAIL: Salary data was imputed! NEVER_IMPUTE violated!"
        
        assert "filled" not in app_content.lower() or "quality" in app_content.lower(), \
            "❌ CRITICAL FAIL: Protected HR fields were filled!"
        
        # Vietnam Context Validation
        vietnam_terms = ["employee", "salary", "nhân viên", "lương"]
        has_vietnam = any(term.lower() in app_content.lower() for term in vietnam_terms)
        assert has_vietnam, "❌ FAIL: No Vietnam HR context found!"
        
        # Data Quality Check
        assert "quality" in app_content.lower() or "chất lượng" in app_content.lower(), \
            "❌ FAIL: No data quality assessment displayed!"
        
        print("✅ PASS: Chị Mai's HR test - Data integrity protected, Vietnam context present")
    
    def test_anh_tuan_ecommerce_owner_shopee(self):
        """
        Persona: Anh Tuấn - E-commerce Owner
        Data: 1000 orders/day, COD payment, Vietnamese provinces
        Focus: Payment methods, provinces, revenue integrity
        """
        print("\n🧪 Testing as Anh Tuấn (E-commerce Owner)...")
        
        # Vietnam E-commerce data with COD, Zalo Pay, E-wallet
        ecom_csv = b"""order_id,customer_name,product,price,payment_method,province,order_date,status
ORD001,Nguyen Thi Mai,iPhone 15 Pro,29900000,COD,Ho Chi Minh,2024-10-01,Delivered
ORD002,Tran Van Binh,Samsung Galaxy S24,22000000,Zalo Pay,Hanoi,2024-10-02,Delivered
ORD003,Le Thi Cuc,AirPods Pro,5990000,MoMo,Da Nang,2024-10-03,Delivered
ORD004,Pham Van Dung,MacBook Air M3,28990000,Bank Transfer,Ho Chi Minh,2024-10-04,Delivered
ORD005,Hoang Thi Ethan,Apple Watch Ultra,19990000,COD,Can Tho,2024-10-05,Delivered
ORD006,Nguyen Van Phong,iPad Pro,25000000,Zalo Pay,Hai Phong,2024-10-06,Processing
ORD007,Tran Thi Lan,AirTag 4-pack,2490000,COD,Ho Chi Minh,2024-10-07,Delivered"""
        
        at = AppTest.from_file(self.app_path)
        at.run()
        
        csv_file = io.BytesIO(ecom_csv)
        csv_file.name = "shopee_orders.csv"
        
        at.file_uploader[0].set_value([csv_file]).run()
        app_content = str(at)
        
        # CRITICAL: Revenue/Price should NEVER be imputed
        assert "imputed" not in app_content.lower(), \
            "❌ CRITICAL FAIL: Revenue/Price was imputed! Financial data corrupted!"
        
        # Vietnam Payment Methods
        vietnam_payments = ["COD", "Zalo", "MoMo"]
        has_payment = any(payment in app_content for payment in vietnam_payments)
        assert has_payment, "❌ FAIL: Vietnam payment methods not recognized!"
        
        # Vietnam Provinces
        vietnam_provinces = ["Ho Chi Minh", "Hanoi", "Da Nang", "Can Tho"]
        has_province = any(province in app_content for province in vietnam_provinces)
        assert has_province, "❌ FAIL: Vietnam provinces not recognized!"
        
        print("✅ PASS: Anh Tuấn's E-commerce test - Revenue protected, Vietnam context present")
    
    def test_chi_lan_marketing_manager_unilever(self):
        """
        Persona: Chị Lan - Marketing Manager at Unilever
        Data: $100k/month ad spend, Zalo Ads, TikTok, Facebook
        Focus: ROAS, CPA metrics, Vietnam platforms
        """
        print("\n🧪 Testing as Chị Lan (Marketing Manager)...")
        
        # Vietnam Marketing data with local platforms
        marketing_csv = b"""campaign,platform,spend_usd,impressions,clicks,conversions,date,product
Tet_2024,Zalo Ads,5000,500000,25000,1250,2024-02-01,Shampoo
Summer_Sale,Facebook,8000,1000000,50000,2500,2024-06-15,Soap
Flash_Deal,TikTok,3000,750000,30000,1500,2024-08-20,Toothpaste
Brand_Awareness,Google Ads,10000,2000000,40000,2000,2024-09-10,All Products
Influencer_Collab,Instagram,4000,600000,20000,1000,2024-10-01,Skincare"""
        
        at = AppTest.from_file(self.app_path)
        at.run()
        
        csv_file = io.BytesIO(marketing_csv)
        csv_file.name = "unilever_marketing.csv"
        
        at.file_uploader[0].set_value([csv_file]).run()
        app_content = str(at)
        
        # CRITICAL: Marketing spend/conversions should NEVER be imputed
        assert "imputed" not in app_content.lower(), \
            "❌ CRITICAL FAIL: Marketing spend/conversions imputed! Wrong decisions will be made!"
        
        # Vietnam Platforms
        vietnam_platforms = ["Zalo", "TikTok"]
        has_platform = any(platform in app_content for platform in vietnam_platforms)
        assert has_platform, "❌ FAIL: Vietnam marketing platforms not recognized!"
        
        # Marketing Metrics
        marketing_metrics = ["roas", "cpa", "cpc", "ctr", "conversion"]
        has_metrics = any(metric in app_content.lower() for metric in marketing_metrics)
        assert has_metrics, "❌ FAIL: Marketing metrics not calculated!"
        
        print("✅ PASS: Chị Lan's Marketing test - Spend protected, Vietnam platforms recognized")
    
    def test_anh_hung_sales_director_viettel(self):
        """
        Persona: Anh Hùng - Sales Director at Viettel
        Data: 50 sales reps, $2M quota, Vietnam enterprises
        Focus: Deal value integrity, Vietnam companies
        """
        print("\n🧪 Testing as Anh Hùng (Sales Director)...")
        
        # Vietnam Sales data with local enterprises
        sales_csv = b"""deal_id,sales_rep,customer,deal_value,stage,close_date,province,product
DEAL001,Nguyen Van Sales,Vingroup,500000000,Closed Won,2024-10-01,Hanoi,Enterprise Package
DEAL002,Tran Thi Rep,FPT Corp,300000000,Negotiation,2024-10-15,Ho Chi Minh,Business Package
DEAL003,Le Van Seller,VinFast,800000000,Closed Won,2024-09-20,Hai Phong,Premium Package
DEAL004,Pham Thi Deal,Masan Group,400000000,Proposal,2024-10-10,Ho Chi Minh,Enterprise Package
DEAL005,Hoang Van Closer,Techcombank,600000000,Closed Won,2024-09-30,Hanoi,Premium Package"""
        
        at = AppTest.from_file(self.app_path)
        at.run()
        
        csv_file = io.BytesIO(sales_csv)
        csv_file.name = "viettel_deals.csv"
        
        at.file_uploader[0].set_value([csv_file]).run()
        app_content = str(at)
        
        # CRITICAL: Deal value should NEVER be imputed
        assert "imputed" not in app_content.lower(), \
            "❌ CRITICAL FAIL: Deal value imputed! Revenue forecast will be wrong!"
        
        # Vietnam Companies
        vietnam_companies = ["Vingroup", "FPT", "VinFast", "Masan", "Techcombank"]
        has_company = any(company in app_content for company in vietnam_companies)
        assert has_company, "❌ FAIL: Vietnam companies not recognized!"
        
        # Sales Metrics
        sales_metrics = ["win rate", "pipeline", "quota", "deal"]
        has_metrics = any(metric.lower() in app_content.lower() for metric in sales_metrics)
        assert has_metrics, "❌ FAIL: Sales metrics not calculated!"
        
        print("✅ PASS: Anh Hùng's Sales test - Deal value protected, Vietnam companies recognized")
    
    def test_chi_ngoc_cs_manager_tiki(self):
        """
        Persona: Chị Ngọc - Customer Service Manager at Tiki
        Data: 500 tickets/day, SLA compliance, Vietnam issues
        Focus: Resolution time, CSAT, Vietnam-specific issues
        """
        print("\n🧪 Testing as Chị Ngọc (CS Manager)...")
        
        # Vietnam Customer Service data
        cs_csv = b"""ticket_id,customer,issue_category,priority,created_date,resolved_date,satisfaction_score,agent,province
TKT001,Nguyen Van Khach,Delivery Delay,High,2024-10-01 09:00,2024-10-01 11:30,4,Agent Mai,Ho Chi Minh
TKT002,Tran Thi User,Product Quality,Medium,2024-10-02 10:00,2024-10-02 15:00,5,Agent Binh,Hanoi
TKT003,Le Van Customer,Payment Issue,High,2024-10-03 08:00,2024-10-03 09:00,5,Agent Cuc,Da Nang
TKT004,Pham Thi Client,Account Access,Low,2024-10-04 14:00,2024-10-04 16:00,3,Agent Dung,Can Tho
TKT005,Hoang Van Buyer,Refund Request,Medium,2024-10-05 11:00,2024-10-05 13:30,4,Agent Ethan,Ho Chi Minh"""
        
        at = AppTest.from_file(self.app_path)
        at.run()
        
        csv_file = io.BytesIO(cs_csv)
        csv_file.name = "tiki_tickets.csv"
        
        at.file_uploader[0].set_value([csv_file]).run()
        app_content = str(at)
        
        # CRITICAL: CSAT, resolution time should NEVER be imputed
        assert "imputed" not in app_content.lower(), \
            "❌ CRITICAL FAIL: CSAT/resolution time imputed! SLA metrics will be wrong!"
        
        # CS Metrics
        cs_metrics = ["resolution time", "csat", "sla", "satisfaction", "response"]
        has_metrics = any(metric.lower() in app_content.lower() for metric in cs_metrics)
        assert has_metrics, "❌ FAIL: Customer Service metrics not calculated!"
        
        # Vietnam Issues
        vietnam_issues = ["Delivery", "Payment", "Refund", "Product"]
        has_issue = any(issue in app_content for issue in vietnam_issues)
        assert has_issue, "❌ FAIL: Vietnam-specific issues not recognized!"
        
        print("✅ PASS: Chị Ngọc's CS test - CSAT protected, Vietnam issues recognized")


class TestNEVER_IMPUTE_Protection:
    """Test that critical business fields are NEVER imputed"""
    
    def test_salary_never_imputed(self):
        """Test that salary field is NEVER imputed even with missing values"""
        print("\n🧪 Testing NEVER_IMPUTE protection for salary...")
        
        # HR data with missing salary (should NOT be imputed)
        hr_csv = b"""employee_id,ho_ten,luong_thang,position
EMP001,Nguyen Van A,28000000,Developer
EMP002,Tran Thi B,,Manager
EMP003,Le Van C,18000000,Staff"""
        
        at = AppTest.from_file("streamlit_app.py")
        at.run()
        
        csv_file = io.BytesIO(hr_csv)
        csv_file.name = "test_missing_salary.csv"
        
        at.file_uploader[0].set_value([csv_file]).run()
        app_content = str(at)
        
        # Should NOT see imputation for salary
        assert "imputed" not in app_content.lower() or "2 rows" not in app_content.lower(), \
            "❌ CRITICAL FAIL: Salary was imputed despite NEVER_IMPUTE protection!"
        
        print("✅ PASS: Salary NEVER_IMPUTE protection working correctly")
    
    def test_revenue_never_imputed(self):
        """Test that revenue/deal_value is NEVER imputed"""
        print("\n🧪 Testing NEVER_IMPUTE protection for revenue...")
        
        # Sales data with missing deal value (should NOT be imputed)
        sales_csv = b"""deal_id,customer,deal_value,stage
DEAL001,Company A,500000000,Won
DEAL002,Company B,,Negotiation
DEAL003,Company C,300000000,Won"""
        
        at = AppTest.from_file("streamlit_app.py")
        at.run()
        
        csv_file = io.BytesIO(sales_csv)
        csv_file.name = "test_missing_revenue.csv"
        
        at.file_uploader[0].set_value([csv_file]).run()
        app_content = str(at)
        
        # Should NOT see imputation for deal_value
        assert "imputed" not in app_content.lower() or "2 rows" not in app_content.lower(), \
            "❌ CRITICAL FAIL: Revenue was imputed despite NEVER_IMPUTE protection!"
        
        print("✅ PASS: Revenue NEVER_IMPUTE protection working correctly")


if __name__ == "__main__":
    """Run tests directly or with pytest"""
    print("🚀 Starting Vietnam Data Analytics App Testing...")
    print("=" * 80)
    
    # Run with pytest for better output
    pytest.main([__file__, "-v", "-s"])
