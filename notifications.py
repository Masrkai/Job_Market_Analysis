"""
Email Notification System for LinkedIn Job Scraper
Sends alerts for new jobs matching criteria
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import json


class JobNotifier:
    """Send email notifications for new job postings"""
    
    def __init__(self, config_path: str = "notification_config.json"):
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: str) -> Dict:
        """Load email configuration"""
        default_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "your_email@gmail.com",
            "sender_password": "your_app_password",
            "recipient_emails": ["recipient@example.com"],
            "alert_criteria": {
                "keywords": ["Machine Learning", "Data Scientist"],
                "min_salary": 50000,
                "remote_only": False,
                "easy_apply_only": False
            }
        }
        
        config_file = Path(config_path)
        if not config_file.exists():
            # Create default config
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"Created default notification config: {config_path}")
            return default_config
        
        with open(config_file, 'r') as f:
            return json.load(f)
    
    def send_new_jobs_alert(self, jobs: List[Dict], summary: Dict):
        """Send email alert for new jobs"""
        if not jobs:
            print("No new jobs to notify")
            return
        
        subject = f"🚨 {len(jobs)} New Jobs Found - LinkedIn Scraper"
        body = self._create_email_body(jobs, summary)
        
        try:
            self._send_email(subject, body, is_html=True)
            print(f"✅ Email notification sent to {len(self.config['recipient_emails'])} recipients")
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
    
    def _create_email_body(self, jobs: List[Dict], summary: Dict) -> str:
        """Create HTML email body"""
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #0077b5; color: white; padding: 20px; text-align: center; }}
                .summary {{ background-color: #f4f4f4; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .job-card {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .job-title {{ color: #0077b5; font-size: 18px; font-weight: bold; }}
                .company {{ color: #666; font-size: 14px; }}
                .salary {{ color: #28a745; font-weight: bold; }}
                .tag {{ display: inline-block; padding: 5px 10px; margin: 5px 5px 5px 0; 
                        background-color: #e7f3ff; border-radius: 3px; font-size: 12px; }}
                .footer {{ text-align: center; color: #666; margin-top: 30px; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 New Job Opportunities Found!</h1>
                <p>LinkedIn CS/AI/ML Job Scraper Alert</p>
            </div>
            
            <div class="summary">
                <h2>📊 Summary</h2>
                <p><strong>Total New Jobs:</strong> {len(jobs)}</p>
                <p><strong>Unique Companies:</strong> {summary.get('unique_companies', 0)}</p>
                <p><strong>Jobs with Easy Apply:</strong> {summary.get('easy_apply_count', 0)}</p>
                <p><strong>Jobs with Salary Info:</strong> {summary.get('jobs_with_salary', 0)}</p>
                <p><strong>Scraped:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <h2>🔥 Top Opportunities</h2>
        """
        
        # Add job cards (limit to top 20)
        for i, job in enumerate(jobs[:20], 1):
            salary_str = ""
            if job.get('salary_min') and job.get('salary_max'):
                salary_str = f"<p class='salary'>💰 {job.get('salary_currency', 'USD')} {job['salary_min']:,.0f} - {job['salary_max']:,.0f}</p>"
            
            easy_apply = "⚡ Easy Apply" if job.get('easy_apply') else ""
            remote = "🏠 Remote" if 'REMOTE' in str(job.get('remote_type', '')).upper() else ""
            
            skills = job.get('skills_required', '').split(',')[:5]
            skills_tags = ''.join([f"<span class='tag'>{s.strip()}</span>" for s in skills if s.strip()])
            
            html += f"""
            <div class="job-card">
                <div class="job-title">{i}. {job.get('job_title', 'N/A')}</div>
                <div class="company">🏢 {job.get('company_name', 'N/A')} | 📍 {job.get('location', 'N/A')}</div>
                {salary_str}
                <p>
                    <span class='tag'>{job.get('experience_level', 'N/A')}</span>
                    <span class='tag'>{job.get('job_type', 'N/A')}</span>
                    {f"<span class='tag'>{easy_apply}</span>" if easy_apply else ""}
                    {f"<span class='tag'>{remote}</span>" if remote else ""}
                </p>
                {f"<p><strong>Skills:</strong> {skills_tags}</p>" if skills_tags else ""}
                <p><a href="{job.get('job_url', '#')}" style="color: #0077b5;">View Job →</a></p>
            </div>
            """
        
        if len(jobs) > 20:
            html += f"<p><em>... and {len(jobs) - 20} more jobs</em></p>"
        
        html += """
            <div class="footer">
                <p>This is an automated notification from your LinkedIn Job Scraper</p>
                <p>To stop receiving these emails, update your notification_config.json</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _send_email(self, subject: str, body: str, is_html: bool = False, attachment_path: Optional[str] = None):
        """Send email via SMTP"""
        msg = MIMEMultipart()
        msg['From'] = self.config['sender_email']
        msg['To'] = ', '.join(self.config['recipient_emails'])
        msg['Subject'] = subject
        
        # Attach body
        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
        
        # Attach file if provided
        if attachment_path and Path(attachment_path).exists():
            with open(attachment_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={Path(attachment_path).name}'
                )
                msg.attach(part)
        
        # Send email
        with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
            server.starttls()
            server.login(self.config['sender_email'], self.config['sender_password'])
            server.send_message(msg)
    
    def send_scraping_report(self, total_jobs: int, new_jobs: int, duration: float, csv_path: Optional[str] = None):
        """Send summary report after scraping session"""
        subject = f"📊 Scraping Complete: {new_jobs} New Jobs Found"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>✅ Scraping Session Complete</h2>
            <p><strong>Total Jobs Scraped:</strong> {total_jobs}</p>
            <p><strong>New Jobs Added:</strong> {new_jobs}</p>
            <p><strong>Duration:</strong> {duration/60:.1f} minutes</p>
            <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            {f'<p>📎 Results attached as CSV</p>' if csv_path else ''}
            
            <p>Check your dashboard for detailed analysis!</p>
        </body>
        </html>
        """
        
        try:
            self._send_email(subject, body, is_html=True, attachment_path=csv_path)
            print("✅ Scraping report sent")
        except Exception as e:
            print(f"❌ Failed to send report: {str(e)}")
    
    def check_and_alert(self, jobs: List[Dict]):
        """Check jobs against alert criteria and send notifications"""
        criteria = self.config.get('alert_criteria', {})
        matching_jobs = []
        
        for job in jobs:
            # Check keywords
            keywords = criteria.get('keywords', [])
            if keywords:
                job_text = f"{job.get('job_title', '')} {job.get('description', '')}".lower()
                if not any(keyword.lower() in job_text for keyword in keywords):
                    continue
            
            # Check salary
            min_salary = criteria.get('min_salary')
            if min_salary and job.get('salary_min'):
                if job['salary_min'] < min_salary:
                    continue
            
            # Check remote
            if criteria.get('remote_only', False):
                if 'REMOTE' not in str(job.get('remote_type', '')).upper():
                    continue
            
            # Check Easy Apply
            if criteria.get('easy_apply_only', False):
                if not job.get('easy_apply'):
                    continue
            
            matching_jobs.append(job)
        
        if matching_jobs:
            summary = {
                'unique_companies': len(set(j.get('company_name') for j in matching_jobs)),
                'easy_apply_count': sum(1 for j in matching_jobs if j.get('easy_apply')),
                'jobs_with_salary': sum(1 for j in matching_jobs if j.get('salary_min'))
            }
            self.send_new_jobs_alert(matching_jobs, summary)
        else:
            print("No jobs matched alert criteria")


# ==================== NOTIFICATION CONFIG SETUP ====================

def setup_notifications():
    """Interactive setup for email notifications"""
    print("📧 Email Notification Setup")
    print("=" * 50)
    
    print("\nFor Gmail, you need an 'App Password':")
    print("1. Go to Google Account Settings")
    print("2. Security → 2-Step Verification → App Passwords")
    print("3. Generate password for 'Mail' app")
    
    config = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587
    }
    
    config['sender_email'] = input("\nYour email address: ").strip()
    config['sender_password'] = input("App password (hidden): ").strip()
    
    recipients = input("Recipient emails (comma-separated): ").strip()
    config['recipient_emails'] = [email.strip() for email in recipients.split(',')]
    
    print("\n⚙️  Alert Criteria (press Enter to skip)")
    keywords = input("Keywords to monitor (comma-separated): ").strip()
    config['alert_criteria'] = {
        "keywords": [k.strip() for k in keywords.split(',')] if keywords else [],
        "min_salary": None,
        "remote_only": False,
        "easy_apply_only": False
    }
    
    min_sal = input("Minimum salary (or Enter to skip): ").strip()
    if min_sal.isdigit():
        config['alert_criteria']['min_salary'] = int(min_sal)
    
    remote = input("Remote only? (y/n): ").strip().lower()
    config['alert_criteria']['remote_only'] = (remote == 'y')
    
    easy = input("Easy Apply only? (y/n): ").strip().lower()
    config['alert_criteria']['easy_apply_only'] = (easy == 'y')
    
    # Save config
    with open('notification_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Configuration saved to notification_config.json")
    
    # Test email
    test = input("\nSend test email? (y/n): ").strip().lower()
    if test == 'y':
        notifier = JobNotifier()
        try:
            notifier._send_email(
                "✅ Test Email - LinkedIn Job Scraper",
                "<h2>Success!</h2><p>Your notifications are configured correctly.</p>",
                is_html=True
            )
            print("✅ Test email sent successfully!")
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")


# ==================== USAGE EXAMPLE ====================

def example_usage():
    """Example of using the notification system"""
    
    # Initialize notifier
    notifier = JobNotifier()
    
    # Example: Check new jobs and send alerts
    from database import JobDatabase
    
    with JobDatabase() as db:
        # Get recent jobs (last 24 hours)
        recent_jobs = db.search_jobs()
        
        # Check against criteria and alert
        notifier.check_and_alert(recent_jobs)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'setup':
        setup_notifications()
    else:
        example_usage()
