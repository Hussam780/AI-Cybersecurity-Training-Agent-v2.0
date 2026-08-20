# 🤖 وكيل تدريب الأمن السيبراني المتقدم v2.0
# AI Cybersecurity Training Agent v2.0

## 📋 الوصف / Description

منصة تدريب احترافية متكاملة للأمن السيبراني باستخدام الذكاء الاصطناعي (Gemini API). تدعم 10 مجالات تدريبية رئيسية مع دمج أدوات Kali Linux.

A professional integrated cybersecurity training platform using AI (Gemini API). Supports 10 main training domains with Kali Linux tools integration.

---

## 🎯 المجالات التدريبية / Training Domains

| # | المجال (عربي) | Domain (English) | الادوات |
|---|--------------|------------------|---------|
| 1 | فحص انظمة التشغيل وكشف الثغرات | OS Scanning & Vuln Detection | nmap, openvas, nessus |
| 2 | اختبار اختراق الشبكات | Network Penetration Testing | metasploit, wireshark, aircrack-ng |
| 3 | حماية الشبكات وطرد المخترقين | Network Protection & Hacker Expulsion | snort, suricata, iptables |
| 4 | استغلال ثغرات ويندوز | Exploiting Windows Vulnerabilities | empire, mimikatz, powersploit |
| 5 | حماية الانظمة من الهجمات المشهورة | Protecting from Popular Attacks | modsecurity, ossec, fail2ban |
| 6 | انشاء حمولة للاندرويد | Create Android Payload | msfvenom, apktool, jadx |
| 7 | الهندسة العكسية لتطبيقات الهواتف | Reverse Engineering Mobile Apps | ghidra, jadx, frida |
| 8 | تخطي الجدران النارية | Bypass Firewalls | proxychains, iodine, hping3 |
| 9 | البحث والمسح وجمع المعلومات | Research & Information Gathering | theharvester, shodan, maltego |
| 10 | زرع برمجية باكدور في الانظمة | Planting Backdoor Software | metasploit, netcat, powershell |

---

## 🚀 التثبيت على Kali Linux / Installation

### الخطوة 1: تحديث النظام
```bash
sudo apt update && sudo apt upgrade -y
```

### الخطوة 2: تثبيت المتطلبات
```bash
sudo apt install -y python3 python3-pip nmap nikto gobuster hydra sqlmap \
    aircrack-ng ettercap-common bettercap apktool jadx proxychains netcat \
    tcpdump snort theharvester wireshark
```

### الخطوة 3: تثبيت مكتبات Python
```bash
pip3 install google-generativeai requests
```

### الخطوة 4: الحصول على مفتاح Gemini API
1. انتقل الى: https://aistudio.google.com/
2. سجل دخول بحساب Google
3. احصل على مفتاح API مجاني
4. انسخ المفتاح

### الخطوة 5: تعيين مفتاح API
```bash
export GEMINI_API_KEY="your_api_key_here"
```

لجعله دائماً، اضفه الى `~/.bashrc`:
```bash
echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### الخطوة 6: تشغيل الوكيل
```bash
python3 ai_cybersecurity_agent_v2.py
```

---

## 📁 هيكل الملفات / File Structure

```
ai_cybersecurity_agent_v2.py
├── training_data/          # قاعدة بيانات التدريب
│   ├── os_vuln_scanning.json
│   ├── network_pentest.json
│   ├── network_protection.json
│   ├── windows_exploitation.json
│   ├── attack_protection.json
│   ├── android_payload.json
│   ├── mobile_reversing.json
│   ├── firewall_bypass.json
│   ├── reconnaissance.json
│   └── backdoor_implant.json
├── reports/                # التقارير المولدة
├── payloads/               # البايلودات المحفوظة
└── logs/                   # سجلات التشغيل
```

---

## 🎮 الاستخدام / Usage

### القائمة الرئيسية

عند تشغيل السكريبت، ستظهر القائمة الرئيسية:

```
[1]  🖥️  فحص انظمة التشغيل وكشف الثغرات
[2]  🌐 اختبار اختراق الشبكات
[3]  🛡️ حماية الشبكات وطرد المخترقين
[4]  🪟 استغلال ثغرات ويندوز
[5]  🔒 حماية الانظمة من الهجمات المشهورة
[6]  📱 انشاء حمولة للاندرويد
[7]  🔧 الهندسة العكسية لتطبيقات الهواتف
[8]  🔥 تخطي الجدران النارية
[9]  🔍 البحث والمسح وجمع المعلومات
[10] 🚪 زرع برمجية باكدور في الانظمة
[11] 📚 ادارة قاعدة بيانات التدريب
[12] 🤖 تشغيل الوكيل الذكي على هدف محدد
[13] 📊 انشاء تقرير تدريبي شامل
[14] ⚙️  فحص متطلبات النظام
[99] 🚪 خروج
```

### اضافة تقرير تدريبي

1. اختر رقم المجال (1-10)
2. اختر [2] لاضافة تقرير جديد
3. ادخل نوع التقرير: report / payload / scenario
4. ادخل العنوان
5. الصق المحتوى
6. اكتب `END` في سطر منفصل للحفظ

### تشغيل الوكيل الذكي

1. اختر [12] من القائمة الرئيسية
2. اختر نوع الهدف:
   - [1] موقع ويب
   - [2] نظام تشغيل
   - [3] شبكة
   - [4] تطبيق موبايل
   - [5] نظام Windows
   - [6] تحليل تقرير يدوي
3. ادخل بيانات الهدف
4. انتظر تحليل الذكاء الاصطناعي
5. احفظ التقرير اذا اردت

---

## ⚠️ تحذير قانوني / Legal Warning

**هذه الاداة مخصصة للتدريب والتعليم فقط!**

- لا تستخدم على انظمة لا تمتلك صلاحية الوصول اليها
- استخدم فقط في بيئات مختبرية معزولة
- التجاوز القانوني مسؤوليتك الشخصية
- This tool is for educational purposes only
- Only use on systems you own or have explicit permission to test

---

## 🛠️ الميزات / Features

- ✅ 10 مجالات تدريبية شاملة
- ✅ دمج مع 20+ اداة Kali Linux
- ✅ تحليل ذكاء اصطناعي متقدم (Gemini)
- ✅ قاعدة بيانات تدريبية قابلة للتوسع
- ✅ تقارير تدريبية جاهزة
- ✅ بايلودات جاهزة للاستخدام
- ✅ سيناريوهات تدريبية واقعية
- ✅ واجهة عربية/انجليزية
- ✅ حفظ التقارير تلقائياً
- ✅ فحص متطلبات النظام

---

## 📞 الدعم / Support

للاستفسارات والدعم الفني:
- GitHub Issues
- Telegram: @cybersec_support

---

**صنع بـ ❤️ للمجتمع الامني العربي**
**Made with ❤️ for the Arab Security Community**
