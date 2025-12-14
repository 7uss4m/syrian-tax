# دليل اختبار مودل الضرائب السوري

## نظرة عامة

هذا الدليل يوضح كيفية اختبار مودل الضرائب السوري باستخدام خادم mock محلي بدلاً من الاتصال بالنظام الفعلي.

## المتطلبات

- Python 3.7+
- مكتبة Flask
- Postman (اختياري)

## خطوة 1: تثبيت المتطلبات

```bash
pip install -r requirements-mock.txt
```

أو يدوياً:
```bash
pip install Flask==2.3.3 requests==2.31.0
```

## خطوة 2: تشغيل خادم الاختبار

### على Windows:
```cmd
run_mock_server.bat
```

### على Linux/Mac:
```bash
chmod +x run_mock_server.sh
./run_mock_server.sh
```

أو مباشرة:
```bash
python mock_server.py
```

## خطوة 3: إعداد Odoo للاختبار

### 3.1 إعدادات الشركة
1. اذهب إلى **Settings > Companies > Your Company**
2. في تبويب **Syria Tax API Configuration**:
   - Tax API Username: `testpos3`
   - Tax API Password: `A@123456789`
   - Tax Number: `000000000000`

### 3.2 إعدادات اليومية
1. اذهب إلى **Accounting > Accounting > Journals**
2. افتح يومية المبيعات
3. في تبويب **Syria Tax API**:
   - ✅ فعل **"Use Mock Server for Testing"**
   - POS Number: `001`
4. في تبويب **Advanced Settings**:
   - أضف **Syria Tax API** إلى قائمة EDI Formats

## خطوة 4: اختبار API مع Postman

### 4.1 استيراد Collection
1. افتح Postman
2. اضغط **Import**
3. اختر ملف `mock_server.postman_collection.json`

### 4.2 اختبار الـ Login
1. افتح طلب **Login**
2. اضغط **Send**
3. يجب أن تحصل على استجابة تحتوي على token

### 4.3 اختبار إضافة فاتورة
1. افتح طلب **Add Full Bill**
2. في الـ Headers، غير الـ Authorization ليستخدم الـ token من الخطوة السابقة
3. اضغط **Send**
4. يجب أن تحصل على random number

### 4.4 اختبار التحقق من الفاتورة
1. استخدم **Check Bill - GUID** مع GUID من الخطوة السابقة
2. أو استخدم **Check Bill - Random Number** مع random number

## خطوة 5: اختبار المودل في Odoo

### 5.1 إنشاء فاتورة عميل
1. اذهب إلى **Accounting > Customers > Invoices**
2. اضغط **Create**
3. أضف منتج وعميل
4. اضغط **Confirm**

### 5.2 مراقبة العملية
1. في الفاتورة، ستجد تبويب **Tax Information**
2. يجب أن ترى:
   - Bill GUID: تم توليده
   - Submission Status: sent
   - Tax Verification Code: تم توليده
   - API Response: تفاصيل الاستجابة

## خطوة 6: التحقق من النتائج

### في خادم الاختبار
افتح `http://localhost:5000/mock/status` لرؤية:
- عدد الفواتير المحفوظة
- عدد التوكن المفعلة
- وقت الخادم

### في Odoo
تحقق من:
- ✅ GUID فريد لكل فاتورة
- ✅ Random Number من API
- ✅ رمز التحقق الضريبي بالصيغة الصحيحة
- ✅ حالة الإرسال = sent

## استكشاف الأخطاء

### خطأ في الاتصال
- تأكد من أن خادم الاختبار يعمل على المنفذ 5000
- تحقق من إعدادات الـ firewall

### خطأ في المصادقة
- تأكد من إدخال بيانات الاعتماد الصحيحة
- تحقق من صحة الـ token

### خطأ في إضافة الفاتورة
- تأكد من أن GUID فريد
- تحقق من صحة البيانات المرسلة

## سيناريوهات اختبار متقدمة

### اختبار فاتورة مكررة
1. أرسل فاتورة بنفس GUID مرتين
2. يجب أن تحصل على خطأ "BillAlreadyExists"

### اختبار فاتورة غير موجودة
1. ابحث عن GUID غير موجود
2. يجب أن تحصل على "BillNotFound"

### اختبار بدون توكن
1. أرسل طلب Add Bill بدون Authorization header
2. يجب أن تحصل على خطأ "Unauthorized"

## إيقاف الاختبار

للعودة للنظام الفعلي:
1. في اليومية، أزل علامة **"Use Mock Server for Testing"**
2. أدخل URLs الفعلية للنظام الضريبي
3. استخدم بيانات الاعتماد الحقيقية

## ملاحظات مهمة

- الـ Mock Server يحفظ البيانات في الذاكرة فقط
- عند إعادة تشغيل الخادم، تُمسح جميع البيانات
- هذا للاختبار فقط، لا تستخدم في الإنتاج
- تأكد من إيقاف الخادم بعد الانتهاء من الاختبار