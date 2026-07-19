# Siber Güvenlik ve Ağ Yönetimi Dersi Projesi

import datetime
import re

class SecurityLogAnalyzer:
    def __init__(self, log_filename="network_security_logs.txt"):
        self.log_filename = log_filename
        self.malicious_ips = set()
        self.attack_signatures = {
            "SQL_Injection": r"(UNION|SELECT|INSERT|DELETE|DROP|' OR '1'='1)",
            "XSS": r"(<script>|javascript:|alert\()",
            "Brute_Force": r"(admin/login|wp-login|failed_login)"
        }

    def generate_mock_logs(self):
        """Analiz için örnek bir güvenlik log dosyası oluşturur."""
        mock_data = [
            f"[{datetime.datetime.now()}] IP: 192.168.1.50 - REQUEST: GET /index.php HTTP/1.1 - STATUS: 200",
            f"[{datetime.datetime.now()}] IP: 185.220.101.5 - REQUEST: POST /admin/login.php?user=' OR '1'='1 HTTP/1.1 - STATUS: 401",
            f"[{datetime.datetime.now()}] IP: 192.168.1.55 - REQUEST: GET /dashboard HTTP/1.1 - STATUS: 200",
            f"[{datetime.datetime.now()}] IP: 45.132.22.11 - REQUEST: GET /<script>alert(1)</script> HTTP/1.1 - STATUS: 400",
            f"[{datetime.datetime.now()}] IP: 185.220.101.5 - REQUEST: POST /admin/login.php - STATUS: 401 - MSG: Password Failed",
        ]
        with open(self.log_filename, "w", encoding="utf-8") as file:
            for log in mock_data:
                file.write(log + "\n")
        print(f"[+] Örnek log dosyası başarıyla oluşturuldu: {self.log_filename}\n")

    def analyze_logs(self):
        """Log dosyasını satır satır tarar ve tehditleri tespit eder."""
        print("="*60)
        print(" SİBER GÜVENLİK LOG ANALİZİ BAŞLATILDI ")
        print("="*60)

        try:
            with open(self.log_filename, "r", encoding="utf-8") as file:
                for line in file:
                    ip_match = re.search(r"IP:\s*([\d\.]+)", line)
                    if not ip_match:
                        continue
                    
                    current_ip = ip_match.group(1)
                    

                    for attack_type, pattern in self.attack_signatures.items():
                        if re.search(pattern, line, re.IGNORECASE):
                            print(f"[ TEHDİT TESPİT EDİLDİ] Tür: {attack_type} | Kaynak IP: {current_ip}")
                            print(f"--> Log Satırı: {line.strip()}\n")
                            self.malicious_ips.add(current_ip)
                            
        except FileNotFoundError:
            print("[-] Log dosyası bulunamadı. Lütfen önce log üretin.")

        self._generate_incident_report()

    def _generate_incident_report(self):
        """Analiz sonucunda şüpheli IP'leri raporlar."""
        print("="*60)
        print(" OLAY MÜDAHALE RAPORU (INCIDENT REPORT)")
        print("="*60)
        if self.malicious_ips:
            print(f"[!] Güvenlik duvarına (Firewall) engellenmesi önerilen IP adresleri:")
            for ip in self.malicious_ips:
                print(f"     {ip} (Engellendi/Zararlı)")
        else:
            print("[+] Sistem temiz. Herhangi bir siber tehdit izine rastlanmadı.")
        print("="*60)

if __name__ == "__main__":
    analyzer = SecurityLogAnalyzer()
    analyzer.generate_mock_logs()  
    analyzer.analyze_logs()        
