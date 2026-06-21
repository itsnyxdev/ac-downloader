<p align="center">
  <img src="assets/banner.svg" alt="AC Downloader" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/itsnyxdev/ac-downloader" alt="License"></a>
  <a href="https://github.com/itsnyxdev/ac-downloader/releases"><img src="https://img.shields.io/github/v/release/itsnyxdev/ac-downloader" alt="Latest Release"></a>
  <a href="https://github.com/itsnyxdev/ac-downloader/releases"><img src="https://img.shields.io/github/v/release/itsnyxdev/ac-downloader?include_prereleases&label=pre--release&color=orange" alt="Pre-Release"></a>
  <a href="https://github.com/itsnyxdev/ac-downloader/actions/workflows/build.yml"><img src="https://img.shields.io/github/actions/workflow/status/itsnyxdev/ac-downloader/build.yml?branch=main" alt="Build Status"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.12-blue" alt="Python 3.12"></a>
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Platforms">
  <a href="https://github.com/itsnyxdev/ac-downloader/releases"><img src="https://img.shields.io/github/downloads/itsnyxdev/ac-downloader/total" alt="Downloads"></a>
</p>

<p align="center">
  <a href="README.md">English</a> | <strong>فارسی</strong>
</p>

<p align="center">
  <strong>تبدیل هوشمند جلسات ضبط‌شده‌ی Adobe Connect به ویدیوهای MP4 یکپارچه و استاندارد.</strong><br>
  ابزاری مبتنی بر خط فرمان (CLI) که با تحلیل فایل‌های ضبط‌شده‌ی ادوبی کانکت، جریان‌های رسانه‌ای FLV را ادغام کرده و یک خروجی ویدیویی MP4 با کیفیت بالا تولید می‌کند.
</p>

---

## فهرست مطالب

- [نمای کلی](#نمای-کلی)
- [امکانات](#امکانات)
- [پیش‌نیازها](#پیش‌نیازها)
- [نصب](#نصب)
- [شروع سریع](#شروع-سریع)
- [پیکربندی](#پیکربندی)
- [نحوهٔ استفاده](#نحوهٔ-استفاده)
- [عیب‌یابی](#عیب‌یابی)
- [پرسش‌های متداول](#پرسش‌های-متداول)
- [نقشهٔ راه](#نقشهٔ-راه)
- [مواردی که AC Downloader نیست](#مواردی-که-ac-downloader-نیست)
- [انتشارات](#انتشارات)
- [امنیت](#امنیت)
- [پشتیبانی](#پشتیبانی)
- [قدردانی‌ها](#قدردانی‌ها)
- [مجوز](#مجوز)

---

## نمای کلی

نرم‌افزار Adobe Connect جلسات ضبط‌شده را به‌صورت مجموعه‌ای از فایل‌های FLV قطعه‌قطعه شده به همراه یک فایل فراداده (Metadata) با نام `indexstream.xml` ذخیره می‌کند. بازسازی دستی این قطعات و تبدیل آن‌ها به یک ویدیوی قابل استفاده با استفاده از ابزارهایی نظیر FFmpeg، فرآیندی دشوار، زمان‌بر و مستعد خطا است.

**AC Downloader** این فرآیند را به‌طور کامل خودکارسازی می‌کند. کافی است مسیر پوشه‌ی ضبط‌شده را به برنامه معرفی کنید تا یک فایل MP4 واحد، شامل تمامی جریان‌های رسانه‌ای همگام‌سازی‌شده، مقیاس‌بندی‌شده و کدگذاری‌شده دریافت نمایید.

### نحوهٔ عملکرد

1. **تحلیل فراداده:** فایل `indexstream.xml` را جهت شناسایی تمامی جریان‌های رسانه‌ای (دوربین، VoIP، اشتراک‌گذاری صفحه) و برچسب‌های زمانی (Timestamps) آن‌ها تجزیه و تحلیل می‌کند.
2. **ایجاد بوم پایه:** یک بوم پایه (ویدیوی سیاه همراه با صدای خاموش) مطابق با مدت‌زمان کل جلسه ایجاد می‌نماید.
3. **هم‌پوشانی جریان‌ها:** هر جریان رسانه‌ای را در زمان شروع دقیق خود با استفاده از FFmpeg بر روی بوم پایه قرار می‌دهد.
4. **کدگذاری نهایی:** خروجی نهایی را با استفاده از کدک‌های H.264/AAC در قالب فرمت MP4 کدگذاری می‌کند.

### پلتفرم‌های پشتیبانی‌شده

| پلتفرم | معماری | وضعیت |
|---------|--------|-------|
| Windows | amd64 | پشتیبانی می‌شود (نصب‌کننده + نسخه قابل حمل) |
| Linux | amd64 | پشتیبانی می‌شود |
| macOS | arm64 | پشتیبانی می‌شود |

### فرمت‌های ورودی پشتیبانی‌شده

- فایل فراداده‌ی `indexstream.xml` ادوبی کانکت.
- قطعات رسانه‌ای `.flv` ادوبی کانکت (شامل جریان‌های cameraVoip، screenshare و سایر انواع جریان‌ها).

---

## ✨ امکانات

- تجزیه و پردازش هوشمند فراداده‌های ضبط‌شده (`indexstream.xml`).
- ادغام چندین جریان FLV مجزا در قالب یک فایل MP4 واحد.
- همگام‌سازی خودکار جریان‌ها از طریق هم‌پوشانی (Overlay) مبتنی بر برچسب زمانی.
- ارائه سه سطح کیفی پیش‌فرض: پایین (640x360)، متوسط (1280x720) و بالا (1920x1080).
- ترکیب و میکس چندین جریان صوتی با استفاده از فیلتر پیشرفته‌ی `amix`.
- کدگذاری ویدیویی H.264 و صوتی AAC (فرمت پیکسل yuv420p).
- قابلیت شخصی‌سازی پوشه‌ی خروجی و تنظیمات کیفیت تصویر.
- مدیریت تنظیمات از طریق فایل پیکربندی TOML در مسیر `~/.acdl/config.toml`.
- رابط کاربری متنی (CLI) غنی با پیام‌های وضعیت رنگی و تفکیک‌شده.
- کاملاً چندسکویی (Cross-platform): قابل اجرا در Windows، Linux و macOS.
- ارائه‌ی فایل‌های اجرایی مستقل (بدون نیاز به نصب پایتون برای کاربران نهایی).
- نسخه‌ی مخصوص ویندوز همراه با FFmpeg داخلی.

---

## 📋 پیش‌نیازها

### کاربران نسخه‌ی نصب‌کننده (ویندوز)

این نسخه فاقد هرگونه وابستگی خارجی است. نصب‌کننده (Inno Setup)، ابزارهای FFmpeg و FFprobe را به‌صورت داخلی ارائه می‌دهد.

### کاربران نسخه‌ی قابل حمل (Portable)

برای استفاده از نسخه‌های قابل حمل، ضروری است که **FFmpeg** و **FFprobe** در سیستم شما نصب شده و از طریق متغیر محیطی `PATH` در دسترس باشند.

- **ویندوز**: می‌توانید از [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds/releases) یا [ffmpeg.org](https://ffmpeg.org/download.html) دریافت کنید. پس از استخراج، پوشه‌ی `bin/` را به `PATH` سیستم اضافه نمایید.
- **لینوکس**: از طریق مدیر بسته‌ی توزیع خود نصب کنید (مثلاً `sudo apt install ffmpeg` یا `sudo dnf install ffmpeg`).
- **مک‌اواس**: از طریق Homebrew نصب کنید: `brew install ffmpeg`.

### کاربران نصب از سورس (Source)

- **Python 3.12** یا نسخه‌های جدیدتر.
- مدیر بسته‌ی **uv** ([راهنمای نصب](https://docs.astral.sh/uv/getting-started/installation/)).
- **FFmpeg** و **FFprobe** (مطابق توضیحات فوق).

---

## 🚀 نصب

### ویندوز

#### نصب‌کنندهٔ Inno Setup (توصیه‌شده)

1. فایل `ac-downloader-installer-amd64.exe` را از [آخرین انتشار](https://github.com/itsnyxdev/ac-downloader/releases/latest) دانلود کنید.
2. نصب‌کننده را اجرا نمایید (نیاز به دسترسی Administrator).
3. FFmpeg به‌صورت داخلی تعبیه شده است و نیاز به تنظیمات اضافی ندارد.
4. یک ترمینال جدید باز کرده و دستور `ac-downloader --version` را اجرا کنید.

#### نسخه قابل حمل (Portable)

1. فایل `ac-downloader-windows-amd64.zip` را از [آخرین انتشار](https://github.com/itsnyxdev/ac-downloader/releases/latest) دریافت کنید.
2. فایل آرشیو را استخراج نمایید.
3. از نصب بودن FFmpeg و حضور آن در `PATH` سیستم اطمینان حاصل کنید.
4. فایل `ac-downloader.exe` را اجرا کنید.

### لینوکس

#### فایل باینری

1. فایل `ac-downloader-linux-amd64.tar.gz` را از [آخرین انتشار](https://github.com/itsnyxdev/ac-downloader/releases/latest) دریافت کنید.
2. استخراج فایل: `tar -xzf ac-downloader-linux-amd64.tar.gz`
3. انتقال به مسیر اجرایی: `sudo mv ac-downloader /usr/local/bin/`
4. نصب FFmpeg: `sudo apt install ffmpeg`
5. تایید نصب: `ac-downloader --version`

#### نصب از سورس

```bash
git clone https://github.com/itsnyxdev/ac-downloader.git
cd ac-downloader
uv sync
uv run ac-downloader --version
```

### مک‌اواس (macOS)

#### فایل باینری

1. فایل `ac-downloader-macos-arm64.tar.gz` را از [آخرین انتشار](https://github.com/itsnyxdev/ac-downloader/releases/latest) دریافت کنید.
2. استخراج فایل: `tar -xzf ac-downloader-macos-arm64.tar.gz`
3. انتقال به مسیر اجرایی: `sudo mv ac-downloader /usr/local/bin/`
4. نصب FFmpeg: `brew install ffmpeg`
5. تایید نصب: `ac-downloader --version`

> **توجه**: در صورتی که سیستم‌عامل macOS مانع اجرای فایل شد (هشدار Gatekeeper)، دستور زیر را اجرا کنید:
> ```bash
> xattr -cr /path/to/ac-downloader
> ```

---

## 🎯 شروع سریع

سریع‌ترین روش برای تبدیل اولین فایل ضبط‌شده:

```bash
# تبدیل پوشه‌ی ضبط‌شده‌ی ادوبی کانکت
ac-downloader convert ./storage/my-recording

# فایل خروجی به‌صورت پیش‌فرض در مسیر ./output/output.mp4 ذخیره می‌شود
```

تمام! ابزار به‌صورت خودکار فراداده‌های XML را تحلیل کرده، جریان‌های FLV را پردازش نموده و یک فایل MP4 یکپارچه تولید می‌کند.

---

## ⚙️ پیکربندی

### آرگومان‌های خط فرمان

#### دستور `convert`

```
ac-downloader convert <input_dir> [OPTIONS]
```

| آرگومان | نوع | پیش‌فرض | توضیحات |
|---------|-----|---------|---------|
| `input_dir` | مسیر (اجباری) | — | پوشه‌ی حاوی فایل‌های ضبط‌شده‌ی ادوبی کانکت |
| `--output-dir`, `-o` | مسیر | `./output` | پوشه‌ی محل ذخیره‌ی فایل MP4 نهایی |
| `--quality`, `-q` | `low` \| `medium` \| `high` | `medium` | تنظیمات پیش‌فرض کیفیت ویدیو |

#### دستور `config`

```
ac-downloader config show           # نمایش تمامی مقادیر پیکربندی فعلی
ac-downloader config set <key> <value>  # تنظیم یک مقدار خاص در پیکربندی
ac-downloader config reset          # بازنشانی تنظیمات به مقادیر پیش‌فرض
```

#### گزینه‌های عمومی

| گزینه | توضیحات |
|-------|---------|
| `--version`, `-v` | نمایش نسخه‌ی برنامه و خروج |
| `--help`, `-h` | نمایش راهنمای استفاده |

### پیش‌تنظیم‌های کیفیت

| سطح کیفیت | وضوح تصویر | نرخ فریم (FPS) | موارد استفاده |
|-----------|------|---------|--------|
| `low` | 640x360 | 24 | حجم فایل بسیار کم، سرعت پردازش بالا |
| `medium` | 1280x720 | 30 | حالت متوازن (پیشنهادی) |
| `high` | 1920x1080 | 30 | حداکثر کیفیت تصویر |

### متغیرهای محیطی

| متغیر | توضیحات |
|-------|---------|
| `FFMPEG_PATH` | مسیر مستقیم فایل اجرایی FFmpeg (اولویت بالاتر نسبت به تنظیمات و PATH) |

---

## 📚 نحوهٔ استفاده

### تبدیل ساده

```bash
ac-downloader convert ./storage/my-recording
```

### تعیین پوشهٔ خروجی دلخواه

```bash
ac-downloader convert ./storage/my-recording --output-dir ./my-output
```

### خروجی با کیفیت حداکثری

```bash
ac-downloader convert ./storage/my-recording --quality high
```

### تبدیل دسته‌ای (Batch Conversion)

تبدیل هم‌زمان تمامی پوشه‌های موجود در یک مسیر:

```bash
for dir in ./storage/*/; do
  ac-downloader convert "$dir" --output-dir ./output
done
```

---

## 🛠️ عیب‌یابی

### عدم شناسایی FFmpeg

**خطا**: `FFmpeg not found. Install it or set FFMPEG_PATH environment variable.`

**راهکارها**:
1. نصب FFmpeg (به بخش [پیش‌نیازها](#پیش‌نیازها) مراجعه کنید).
2. اطمینان از حضور `ffmpeg` در `PATH` سیستم با دستور: `ffmpeg -version`.
3. تنظیم متغیر محیطی `FFMPEG_PATH` به مسیر مستقیم فایل اجرایی.
4. تنظیم مسیر از طریق پیکربندی برنامه: `ac-downloader config set ffmpeg_path /path/to/ffmpeg`.

### عدم شناسایی FFprobe

FFprobe معمولاً به همراه FFmpeg نصب می‌شود. در صورت بروز خطا:
1. بررسی وجود فایل: `ffprobe -version`.
2. اطمینان حاصل کنید که این فایل در همان پوشه‌ی FFmpeg یا در `PATH` سیستم قرار دارد.

### عدم یافتن فایل indexstream.xml

**خطا**: `No indexstream.xml found in <directory>`

پوشه‌ی ورودی حتماً باید حاوی فایل `indexstream.xml` باشد. این فایل کلید اصلی بازسازی جلسه است. مطمئن شوید که ضبط را به‌طور کامل دانلود کرده‌اید.

### عدم شناسایی جریان‌های رسانه‌ای

ممکن است فایل `indexstream.xml` خالی باشد یا حاوی رویدادهای معتبر نباشد. سلامت فایل XML و کامل بودن دانلود را بررسی کنید.

### خطاهای سطح دسترسی (Permissions)

- **ویندوز**: ترمینال را با دسترسی Administrator اجرا کنید یا از قابل نوشتن بودن پوشه‌ی خروجی مطمئن شوید.
- **لینوکس/مک**: دسترسی‌های پوشه را بررسی کنید: `ls -la <directory>`.

### توقف فرآیند تبدیل در میانه راه

خروجی خطای FFmpeg را در ترمینال بررسی کنید. دلایل رایج عبارتند از:
- کمبود فضای ذخیره‌سازی دیسک.
- وجود فایل‌های FLV آسیب‌دیده در پوشه‌ی ضبط.
- ناسازگاری نسخه‌ی FFmpeg (استفاده از نسخه‌ی 4.0 به بالا توصیه می‌شود).

---

## ❓ پرسش‌های متداول

**آیا برای استفاده از AC Downloader به نصب پایتون نیاز دارم؟**
خیر. فایل‌های اجرایی ارائه شده (نصب‌کننده یا قابل حمل) کاملاً مستقل هستند. پایتون تنها برای توسعه‌دهندگان یا نصب از سورس مورد نیاز است.

**آیا می‌توان جلسات میزبانی شده در سرورهای آنلاین را مستقیماً تبدیل کرد؟**
بله، به شرطی که ابتدا پوشه‌ی ضبط‌شده (شامل فایل‌های XML و FLV) را به‌صورت محلی دانلود کرده باشید. این ابزار در حال حاضر فایل‌های محلی را پردازش می‌کند و مستقیماً به سرورهای ادوبی متصل نمی‌شود.

**خروجی نهایی از چه کدک‌هایی استفاده می‌کند؟**
ویدیو با کدک H.264 (libx264) و صدا با کدک AAC در کانتینر MP4 با فرمت پیکسل yuv420p تولید می‌شود.

**فرآیند تبدیل چقدر زمان می‌برد؟**
این زمان به مدت‌زمان جلسه، تعداد جریان‌ها و کیفیت انتخابی بستگی دارد. به‌طور معمول، یک جلسه‌ی ۱ ساعته با کیفیت متوسط، روی سخت‌افزارهای امروزی ظرف چند دقیقه تبدیل می‌شود.

**آیا امکان تغییر نام فایل خروجی وجود دارد؟**
در نسخه‌ی فعلی خیر؛ نام خروجی همواره `output.mp4` است. این قابلیت در نسخه‌های آینده اضافه خواهد شد (به [نقشهٔ راه](#نقشهٔ-راه) مراجعه کنید).

**آیا AC Downloader اطلاعات من را به جایی ارسال می‌کند؟**
خیر. تمامی پردازش‌ها به‌صورت کاملاً محلی (Local) انجام می‌شود و برنامه هیچ‌گونه درخواست شبکه‌ای ارسال نمی‌کند.

---

## 🗺️ نقشهٔ راه

- [ ] طراحی رابط کاربری تعاملی در ترمینال (TUI).
- [ ] افزودن دانلودر داخلی (دریافت مستقیم از طریق URL جلسه).
- [ ] پشتیبانی از فرمت‌های خروجی بیشتر (WebM, MKV, MOV).
- [ ] قابلیت تعیین نام دلخواه برای فایل خروجی.
- [ ] پردازش موازی جریان‌ها جهت افزایش سرعت تبدیل.
- [ ] مدیریت بهتر فراداده‌ها (حفظ عنوان جلسه، تاریخ و غیره).
- [ ] نمایش نوار پیشرفت (Progress Bar) به همراه تخمین زمان باقی‌مانده.
- [ ] افزودن دستورات تشخیصی و اعتبارسنجی پیکربندی.
- [ ] ارائه‌ی تصویر Docker برای محیط‌های سروری.

---

## ❌ مواردی که AC Downloader نیست

جهت شفاف‌سازی دامنه عملکرد ابزار:
- **جایگزین Adobe Connect نیست**: این ابزار وظیفه‌ی میزبانی یا مدیریت جلسات را بر عهده ندارد.
- **هنوز یک دانلودر مستقیم نیست**: در حال حاضر فایل‌های از قبل دانلود شده را تبدیل می‌کند (قابلیت دانلود مستقیم در نقشه راه قرار دارد).
- **ویرایشگر ویدیو نیست**: قابلیت‌هایی نظیر برش (Trim)، تغییر محتوا یا افزودن جلوه‌های ویژه را ندارد.
- **پلتفرم پخش زنده نیست**: تنها جلسات از قبل ضبط‌شده را پردازش می‌کند.
- **سرور رسانه نیست**: هدف آن تولید فایل است، نه استریمینگ.

---

## 📦 انتشارات

آخرین نسخه‌ی پایدار را از [صفحه انتشارات GitHub](https://github.com/itsnyxdev/ac-downloader/releases) دریافت نمایید.

| بسته | توضیحات |
|------|---------|
| `ac-downloader-installer-amd64.exe` | نصب‌کننده ویندوز (شامل FFmpeg - پیشنهادی) |
| `ac-downloader-windows-amd64.zip` | نسخه قابل حمل ویندوز |
| `ac-downloader-linux-amd64.tar.gz` | نسخه باینری لینوکس |
| `ac-downloader-macos-arm64.tar.gz` | نسخه باینری macOS (معماری ARM64) |

نسخه‌بندی پروژه‌ بر اساس [Semantic Versioning](https://semver.org/) انجام می‌شود.

---

## 🔒 امنیت

برای گزارش هرگونه آسیب‌پذیری امنیتی، لطفاً یک [Issue در GitHub](https://github.com/itsnyxdev/ac-downloader/issues) با برچسب `security` ایجاد کنید یا مستقیماً با نگهدارندگان پروژه تماس بگیرید.

لطفاً تا زمان ارائه‌ی وصله‌ی امنیتی، از افشای عمومی جزئیات خودداری نمایید.

---

## 💬 پشتیبانی

- **گزارش باگ**: [GitHub Issues](https://github.com/itsnyxdev/ac-downloader/issues/new?template=bug_report.md)
- **درخواست قابلیت جدید**: [GitHub Issues](https://github.com/itsnyxdev/ac-downloader/issues/new?template=feature_request.md)
- **پرسش و پاسخ**: [GitHub Discussions](https://github.com/itsnyxdev/ac-downloader/discussions)

---

## 🙏 قدردانی‌ها

پروژه‌ی AC Downloader بر شانه‌های غول‌های متن‌باز بنا شده است:

- [FFmpeg](https://ffmpeg.org/) — موتور قدرتمند پردازش چندرسانه‌ای.
- [Typer](https://typer.tiangolo.com/) — چارچوب توسعه‌ی CLI.
- [Rich](https://rich.readthedocs.io/) — جهت زیباسازی خروجی ترمینال.
- [PyInstaller](https://pyinstaller.org/) — بسته‌بندی فایل‌های اجرایی.
- [Pydantic](https://docs.pydantic.dev/) — مدیریت و اعتبارسنجی داده‌ها.
- [Loguru](https://loguru.readthedocs.io/) — سیستم ثبت رخداد (Logging).
- [rtoml](https://github.com/samuelcolvin/rtoml) — پردازش فایل‌های TOML.

---

## 📄 مجوز

این پروژه تحت [مجوز MIT](LICENSE) منتشر شده است.