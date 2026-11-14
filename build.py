"""Builds the static celiac site: shared header/footer around each page body."""
import pathlib, sys, re

OUT = pathlib.Path(sys.argv[1])
SITE = "צליאק – מדריך להורים"
AUTHOR = "מרב להב"
EMAIL = "lahavcom@gmail.com"
DOMAIN = "https://celiackids.co.il"
HOST = "GitHub Pages"         # או Netlify, לפי איפה שמעלים
UPDATED = "14.11.2026"
UPDATED_MONTH = "נובמבר 2026"

NAV = [
    ("index.html", "דף הבית"),
    ("diagnosis.html", "קיבלנו אבחנה"),
    ("hosts.html", "עושים יום הולדת"),
    ("playdate.html", "מארחים ילד/ה לשחק"),
]
GUIDE_NAV = [
    ("diagnosis.html", "שלב אחר שלב"),
    ("manage.html", "בבית ומחוץ לבית"),
    ("birthdays.html", "ימי הולדת: איך מתכוננים"),
    ("rights.html", "זכויות ומקורות"),
]

GUIDE = "https://celiacrights.org.il/wp-content/uploads/המדריך-המלא-להורים-המתחילים-צליאק.pdf"
L = {
    "guide": f'<a href="{GUIDE}">המדריך המלא להורים המתחילים – ארגון זכויות הצליאק</a>',
    "org": '<a href="https://celiacrights.org.il/">ארגון זכויות הצליאק</a>',
    "kz": '<a href="https://www.kolzchut.org.il/he/צליאק">כל זכות – צליאק</a>',
    "kzparents": '<a href="https://www.kolzchut.org.il/he/מדריך_להורים_של_ילדים_עם_צרכים_מיוחדים">כל זכות – מדריך להורים לילדים עם צרכים מיוחדים</a>',
    "kzclaim": '<a href="https://www.kolzchut.org.il/he/הגשת_תביעה_לגמלת_ילד_נכה">כל זכות – הגשת תביעה לגמלת ילד נכה</a>',
    "circ": '<a href="https://celiacrights.org.il/public-institutions/%d7%97%d7%95%d7%96%d7%a8-%d7%9e%d7%a0%d7%9b%d7%9c-%d7%9e%d7%a9%d7%a8%d7%93-%d7%94%d7%97%d7%99%d7%a0%d7%95%d7%9a">חוזר מנכ"ל משרד החינוך (באתר ארגון זכויות הצליאק)</a>',
    "sim_gan": '<a href="https://meyda.education.gov.il/files/briut/2026briut/Celiac/modelceliac-ganim.pdf">שמים לצליאק – גני ילדים</a>',
    "sim_yes": '<a href="https://meyda.education.gov.il/files/briut/2026briut/Celiac/modelceliac-yesodi.pdf">שמים לצליאק – יסודי</a>',
    "sim_al": '<a href="https://meyda.education.gov.il/files/briut/2026briut/Celiac/modelceliac-alyesodi.pdf">שמים לצליאק – על-יסודי</a>',
    "edu": '<a href="https://meyda.education.gov.il/files/MinhalPedagogy/briut/tzeliak.pdf">משרד החינוך – צליאק במוסדות חינוך</a>',
    "maccabi": '<a href="https://www.maccabi4u.co.il/kosher/31390/celiac_disease/">מכבי – אובחנתם בצליאק? אלו הכללים</a>',
    "ynet": '<a href="https://www.ynet.co.il/economy/article/5457160">ynet – סבסוד קמח ללא גלוטן</a>',
    "bhol": '<a href="https://www.bhol.co.il/news/1372097">בחדרי חרדים – המדינה תסבסד קמח ללא גלוטן (יולי 2026)</a>',
    "maariv": '<a href="https://www.maariv.co.il/news/health/article-1320157">מעריב – דיון בוועדת הבריאות על סבסוד הקמח</a>',
    "newpat": '<a href="https://celiacrights.org.il/lifestyle/%d7%9c%d7%99%d7%95%d7%95%d7%99-%d7%a6%d7%9c%d7%99%d7%90%d7%a7%d7%99%d7%9d-%d7%97%d7%93%d7%a9%d7%99%d7%9d">ליווי צליאקים חדשים – ארגון זכויות הצליאק</a>',
    "diag": '<a href="https://celiacrights.org.il/the-celiac/%d7%90%d7%91%d7%97%d7%95%d7%9f-%d7%9e%d7%97%d7%9c%d7%aa-%d7%94%d7%a6%d7%9c%d7%99%d7%90%d7%a7">אבחון מחלת הצליאק – ארגון זכויות הצליאק</a>',
    "mom": "סיכום מעשי של אמא לילדה עם צליאק (מסמך שהועבר בין הורים)",
}

DISCLAIMER = ("האתר נכתב בהתנדבות ואינו מייצג אף עמותה, ארגון, קופת חולים או גוף ממשלתי. "
              f"המידע באתר כללי, נכון לתאריך העדכון ({UPDATED}) בלבד, ויכול להשתנות בכל רגע. המידע אינו ייעוץ רפואי, תזונתי או משפטי, "
              "ואינו מחליף פנייה לרופא, לדיאטנית או לגורם מוסמך. אין בו התחייבות לנכונות המידע, לשלמותו או לזכאות כלשהי. "
              "רכיבי מוצרים משתנים: האחריות לבדוק כל פרט מול התווית, המקור הרשמי או הגורם המטפל היא של המשתמש/ת.")


def og_image(fname):
    if not DOMAIN.startswith("http"):
        return ""
    img = "og-hosts.png" if fname in ("hosts.html", "playdate.html") else "og.png"
    base = DOMAIN.rstrip("/")
    return (f'<meta property="og:image" content="{base}/{img}">\n'
            '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta property="og:url" content="{base}/{fname}">\n<meta name="twitter:card" content="summary_large_image">')


def mail():
    if "@" in EMAIL:
        return f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    return EMAIL


def subnav(fname):
    if fname not in [h for h, _ in GUIDE_NAV]:
        return ""
    items = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{t}</a></li>' for h, t in GUIDE_NAV)
    return f'<nav class="sub" aria-label="המדריך למאובחנים"><div class="sub-in"><b>המדריך:</b><ul>{items}</ul></div></nav>\n'


def footnotes(body, single=False):
    """Collect source markers per section and show one quiet line under each section: 'מקורות: א · ב'."""
    import re as _re
    src = _V0.SRC
    body = _re.sub(r'</td><td>\s*(<span class="srcm" data-k="[^"]*"></span>)\s*</td></tr>', r'\1</td></tr>', body)
    body = body.replace("<th>מקור</th>", "")
    body = _re.sub(r'<p>\s*(<span class="srcm" data-k="[^"]*"></span>)\s*</p>', r'\1', body)
    def line(keys):
        if not keys:
            return ""
        parts = []
        for k in keys:
            name, url = src[k]
            parts.append(f'<a href="{url}">{name}</a>' if url else f'<span>{name}</span>')
        return '<p class="srcline">מקורות: ' + " · ".join(parts) + '</p>\n'
    if single:
        keys = []
        for m in _re.finditer(r'<span class="srcm" data-k="([^"]*)"></span>', body):
            for k in m.group(1).split(","):
                if k not in keys:
                    keys.append(k)
        for k in ("guide", "mac", "mom"):
            if k not in keys:
                keys.append(k)
        body = _re.sub(r'\s*<span class="srcm" data-k="[^"]*"></span>', '', body)
        return body.replace("</article>", line(keys) + "</article>", 1)
    # split before every h2/h3 and before the trailing share block
    pieces = _re.split(r'(?=<section class="labels")|(?=<h[23][ >])|(?=<div class="share-box)', body)
    out = []
    for piece in pieces:
        keys = []
        for m in _re.finditer(r'<span class="srcm" data-k="([^"]*)"></span>', piece):
            for k in m.group(1).split(","):
                if k not in keys:
                    keys.append(k)
        piece = _re.sub(r'\s*<span class="srcm" data-k="[^"]*"></span>', '', piece)
        # put the line after the section's content but before a closing article/section wrapper
        m = _re.search(r'(\s*(?:</section>|</article>)\s*)$', piece)
        if m and keys:
            piece = piece[:m.start()] + "\n" + line(keys) + piece[m.start():]
        else:
            piece = piece + line(keys)
        out.append(piece)
    return "".join(out)

def page(fname, title, body, wide=False, desc=""):
    share_page = fname in ("hosts.html", "playdate.html")
    body = footnotes(body, single=share_page)
    nav = "".join(
        f'<li><a href="{h}"'
        f'{" aria-current=\"page\"" if h == fname or (h == "diagnosis.html" and fname in [g for g, _ in GUIDE_NAV]) else ""}>{t}</a></li>'
        for h, t in NAV)
    t = SITE if fname == "index.html" else f"{title} | {SITE}"
    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{desc or title}">
<meta property="og:title" content="{OG.get(fname, (t,))[0]}">
<meta property="og:description" content="{OG.get(fname, (t, desc or title))[-1]}">
<meta property="og:locale" content="he_IL">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
{og_image(fname)}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Secular+One&family=Assistant:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">דילוג לתוכן</a>
<header class="bar{' slim' if share_page else ''}"><div class="bar-in">
  <a class="logo" href="index.html">{SITE}</a>
  <nav class="nav-desk" aria-label="תפריט ראשי"><ul>{nav}</ul></nav>
  <details class="nav-mob"><summary>תפריט</summary><nav aria-label="תפריט ראשי (נייד)"><ul>{nav}</ul></nav></details>
</div></header>
{subnav(fname)}<main id="main" tabindex="-1"{' class="wide"' if wide else ''}>
{body}
</main>
<footer><div class="foot-in">
  <p class="foot-key">האתר נכתב בהתנדבות. אין התחייבות לתוכן, המידע יכול להשתנות בכל רגע, ואין בו ייעוץ רפואי או משפטי.</p>
  <p>{DISCLAIMER}</p>
  <p>נכתב בהתנדבות על ידי {AUTHOR} · לעדכונים והצעות: {mail()}</p>
  <nav aria-label="מידע על האתר"><ul class="foot-nav">
    <li><a href="about.html">על האתר</a></li>
    <li><a href="terms.html">תנאי שימוש</a></li>
    <li><a href="privacy.html">מדיניות פרטיות</a></li>
    <li><a href="accessibility.html">הצהרת נגישות</a></li>
  </ul></nav>
</div></footer>
</body>
</html>
"""


def sources(*keys):
    items = "".join(f"<li>{L[k]}</li>" for k in keys)
    return f'<div class="sources"><b>מקורות לעמוד הזה</b><ul>{items}</ul></div>'


PAGES = {}
import importlib.util as _ilu0, os as _os0
_sp0 = _ilu0.spec_from_file_location("verified", _os0.path.join(_os0.path.dirname(_os0.path.abspath(__file__)), "verified.py"))
_V0 = _ilu0.module_from_spec(_sp0); _sp0.loader.exec_module(_V0)
V_HOSTS_BASED = ""
SHARE = """<div class="share-box noprint">
  <p class="share-title">שולחים את הדף להורים אחרים?</p>
  <div class="share">
    <a class="btn wa" id="wa" href="https://wa.me/" rel="noopener">שליחה בוואטסאפ</a>
    <button class="btn ghost" type="button" id="copy-link">העתקת קישור</button>
    <button class="btn ghost desk-only" type="button" id="print">הדפסה</button>
  </div>
  <p class="status" id="status" role="status"></p>
</div>
<p class="noprint back"><a href="index.html">לאתר המלא: צליאק – מדריך להורים</a></p>
<script>
(function () {
  var s = document.getElementById('status');
  var url = location.href.split('#')[0];
  var title = document.querySelector('h1') ? document.querySelector('h1').textContent.trim() : document.title;
  document.getElementById('wa').href = 'https://wa.me/?text=' + encodeURIComponent(title + '\\n' + url);
  function say(t) { s.textContent = t; setTimeout(function () { s.textContent = ''; }, 4000); }
  document.getElementById('copy-link').addEventListener('click', function () {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () { say('הקישור הועתק. אפשר להדביק בוואטסאפ.'); },
        function () { say('ההעתקה נחסמה. העתיקו את הכתובת משורת הדפדפן.'); });
    } else { say('העתיקו את הכתובת משורת הדפדפן.'); }
  });
  document.getElementById('print').addEventListener('click', function () {
    var d = document.querySelector('details.more'); if (d) d.open = true;
    try { window.print(); } catch (e) { say('ההדפסה לא זמינה כאן. נסו מהדפדפן.'); }
  });
})();
</script>"""
OG = {"hosts.html": ("הילד/ה שלנו מגיע/ה ליום ההולדת!", "יש לו/לה צליאק. 3 דברים פשוטים לפני שקונים חטיפים. דקה קריאה."),
      "playdate.html": ("הילד/ה שלנו בא/ה אליכם לשחק!", "יש לו/לה צליאק. 3 דברים קטנים לפני שמגישים אוכל. דקה קריאה.")}

# ---------------- HOME ----------------
PAGES["index.html"] = ("דף הבית", True, """
<h1>צליאק: מה עושים?</h1>
<p class="lead">האתר מחבר בין הורים לילדים עם צליאק לבין ההורים שמארחים אותם, לטובת הילדים. בחרו מה מתאים לכם.</p>

<div class="doors">
  <a class="door" href="diagnosis.html">
    <span class="who">להורים</span>
    <h2>קיבלנו אבחנה של צליאק</h2>
    <p>מדריך מסודר מהיום הראשון: מה עושים בשבוע הראשון, איך מתנהלים בבית ובחוץ, ומה מגיע לכם.</p>
    <span class="go">למדריך ←</span>
  </a>
  <a class="door" href="hosts.html">
    <span class="who">לחוגגים</span>
    <h2>עושים יום הולדת ומגיע ילד/ה עם צליאק</h2>
    <p>3 דברים פשוטים ורשימת קניות. דקה קריאה.</p>
    <span class="go">לדף יום הולדת ←</span>
  </a>
  <a class="door" href="playdate.html">
    <span class="who">למארחים</span>
    <h2>ילד/ה עם צליאק בא/ה אלינו לשחק</h2>
    <p>מה אפשר להגיש, ואיך שומרים שהילד/ה לא ייחשף/תיחשף לגלוטן. דקה קריאה.</p>
    <span class="go">לדף ביקור ←</span>
  </a>
</div>

<div class="callout green send">
  <p><b>הורים לילד/ה עם צליאק?</b> שולחים את הדף בוואטסאפ, לקבוצת הכיתה או להורים של החבר:</p>
  <div class="share" style="justify-content:flex-start">
    <a class="btn wa" data-wa="hosts.html" href="hosts.html">שליחת הדף לחוגגים</a>
    <a class="btn wa" data-wa="playdate.html" href="playdate.html">שליחת הדף למארחים</a>
  </div>
</div>
<script>
(function () {
  var base = location.href.split('#')[0].replace(/[^/]*$/, '');
  document.querySelectorAll('[data-wa]').forEach(function (a) {
    var t = a.dataset.wa === 'hosts.html' ? 'הילד/ה שלנו מגיע/ה ליום ההולדת! ריכזנו כאן בקצרה מה עוזר:' : 'הילד/ה שלנו בא/ה אליכם לשחק! כמה מילים קטנות על אוכל:';
    a.href = 'https://wa.me/?text=' + encodeURIComponent(t + '\\n' + base + a.dataset.wa);
  });
})();
</script>

<div class="byline">
  <p>האתר נכתב בהתנדבות על ידי """ + AUTHOR + """, אמא לשני ילדים עם צליאק · <a href="about.html#story">הסיפור שלי ולמה הקמתי את האתר</a></p>
  <p class="asof">המידע באתר נכון ל-""" + UPDATED + """ ואינו מחליף בדיקה מול רופא, דיאטנית או הגוף הרשמי.</p>
</div>
""")

# ---------------- DIAGNOSIS ----------------
PAGES["diagnosis.html"] = ("מרגע האבחון", False, f"""
<h1>קיבלנו אבחנה: שלב אחר שלב</h1>
<p class="lead">הימים הראשונים מבלבלים. הנה הסדר שהיה עוזר לנו: מה עושים בשבוע הראשון, בחודשים הראשונים, ולאורך זמן.</p>
<div class="toc"><b>בעמוד הזה</b><ol>
<li><a href="#what">מה זה צליאק, בשתי דקות</a></li>
<li><a href="#week">השבוע הראשון</a></li>
<li><a href="#months">החודשים הראשונים</a></li>
<li><a href="#long">לאורך זמן</a></li>
</ol></div>

<h2 id="what">מה זה צליאק, בשתי דקות</h2>
<p>צליאק היא מחלה אוטואימונית: כשהגוף פוגש גלוטן, מערכת החיסון תוקפת את רירית המעי הדק. גלוטן הוא חלבון שנמצא בחיטה, שעורה, שיפון וכוסמין.</p>
<ul>
<li><b>אין דרגות.</b> צליאק היא לא אלרגיה שיכולה להיות "קלה". כל מי שיש לו צליאק צריך להימנע לגמרי מגלוטן.</li>
<li><b>אין "קצת".</b> גם כשאין תסמינים, חשיפה לגלוטן גורמת נזק שמצטבר.</li>
<li><b>זו לא אשמתכם.</b> צליאק נובעת משילוב של גנטיקה וגורמים נוספים. שום דבר שעשיתם לא גרם לה.</li>
<li><b>שיבולת שועל:</b> שנויה במחלוקת, ובדרך כלל לא מאשרים אותה לילדים. מתייעצים עם הרופא.</li>
</ul>

<h2 id="week">השבוע הראשון</h2>
<ol class="steps">
<li><b>לקבוע תור לדיאטנית</b>דרך קופת החולים. היא תעזור לבנות תפריט מאוזן ותענה על שאלות על מוצרים.</li>
<li><b>לנשום ולספר לילד</b>בשפה פשוטה: "צליאק היא מחלה, אבל כשאנחנו אוכלים בלי גלוטן, אנחנו בריאים". מדגישים מה כן אפשר, לא רק מה אסור.</li>
<li><b>לנקות את המטבח</b>מחליפים כפות עץ, קרש חיתוך מפלסטיק ומסננת, ומנקים מגירות, תנור ומקפיא מפירורים. הפירוט המלא בעמוד <a href="home.html">בבית</a>.</li>
<li><b>לעבור על המזווה</b>מה שלא מסומן "ללא גלוטן" ולא בטוח, מפרידים או מעבירים הלאה. תבלינים פתוחים מחליפים בחדשים ומסומנים.</li>
<li><b>לבדוק את האחים ואת ההורים</b>לבני משפחה מדרגה ראשונה יש סיכון גבוה יותר לצליאק. מבקשים מרופא המשפחה בדיקת דם. אצלנו, אחרי האבחון של הבן, גילינו צליאק גם אצל הבת, לירון.</li>
<li><b>להתקין את האפליקציה "חופשי מגלוטן"</b>סורקים ברקוד בסופר ובודקים אם המוצר מתאים.</li>
</ol>

<h2 id="months">החודשים הראשונים</h2>
<ul>
<li><b>גן ובית ספר:</b> פגישה עם המחנכת, היועצת והמנהלת, עם חוזר המנכ"ל ביד. ראו <a href="school.html">גן ובית ספר</a>.</li>
<li><b>הורי הכיתה:</b> שולחים בקבוצה את <a href="hosts.html">הדף לחוגגים</a>, עוד לפני יום ההולדת הראשון.</li>
<li><b>ללמוד לקרוא תוויות:</b> קוראים את רשימת הרכיבים ולא רק את תיבת האלרגנים. "עלול להכיל" = לא אוכלים.</li>
<li><b>כאבי בטן בתקופת המעבר</b> יכולים להופיע ולחלוף. אם הם נמשכים, מדברים עם הרופא.</li>
<li><b>מקפיא חירום:</b> מאפינס, בסיסי פיצה ופיתות ללא גלוטן, לכל הפתעה.</li>
<li><b>זכויות:</b> מה מגיע ומה לא, כולל הקמח המסובסד. ראו <a href="rights.html">זכויות</a>.</li>
<li><b>ליווי:</b> לארגון זכויות הצליאק יש פרויקט ליווי למשפחות חדשות.</li>
</ul>

<h2 id="long">לאורך זמן</h2>
<ul>
<li><b>מעקב רפואי:</b> בדיקות דם תקופתיות אצל רופא הגסטרו, לפי ההנחיה שלו. ירידת הנוגדנים מראה שהדיאטה עובדת.</li>
<li><b>הילד לוקח אחריות לפי הגיל:</b> קורא תוויות, שואל במסעדה, אומר "לא תודה". מחמיאים על הבגרות והסבלנות.</li>
<li><b>חגים:</b> סופגניות בחנוכה, משלוח מנות בפורים, מצות בסדר הכיתתי. מתכוננים מראש, יש פתרון לכל דבר.</li>
<li><b>צבא:</b> מתגייסים כרגיל, עם סעיף צליאק בפרופיל, ומקבלים דמי כלכלה. פירוט בעמוד <a href="rights.html">זכויות</a>.</li>
<li><b>הצד הרגשי:</b> "למה רק אני?" היא שאלה שתחזור. מקשיבים, מכירים בתסכול, ומוצאים יחד את הדבר הטעים שכן מתאים.</li>
</ul>
{sources("guide", "maccabi", "diag", "newpat", "mom")}
""")

# ---------------- HOME / KITCHEN ----------------
PAGES["home.html"] = ("בבית", False, f"""
<h1>בבית: המטבח, הקניות והתוויות</h1>
<p class="lead">אפשר לנהל בית "מעורב", עם וגם בלי גלוטן. העיקר הוא הפרדה נכונה והרגלים קבועים.</p>

<h2>המטבח: מה מחליפים ומה מספיק לשטוף</h2>
<div class="tbl"><table>
<thead><tr><th>כלי</th><th>מה עושים</th><th>למה</th></tr></thead>
<tbody>
<tr><td>כפות עץ וקרש עץ</td><td>זורקים, קונים חדשים רק ללא גלוטן</td><td>גלוטן נתקע בחריצים ולא יוצא בשטיפה</td></tr>
<tr><td>קרש חיתוך מפלסטיק</td><td>קונים חדש לירקות ולמזון ללא גלוטן</td><td>שריטות שומרות פירורים</td></tr>
<tr><td>מסננת פסטה, נפה</td><td>אחת נפרדת ללא גלוטן</td><td>אי אפשר לנקות את כל החורים</td></tr>
<tr><td>טוסטר קופץ</td><td>נפרד, או טוסטר לחיצה עם נייר אפייה נקי</td><td>פירורים נשארים בפנים</td></tr>
<tr><td>מיקסר, מעבד מזון</td><td>מנקים היטב, ומעתה רק ללא גלוטן</td><td>קמח עף ונכנס לחריצים</td></tr>
<tr><td>קערות פלסטיק שרוטות</td><td>עוברים לנירוסטה, זכוכית או קרמיקה</td><td>גלוטן נתקע בשריטות</td></tr>
<tr><td>סכו"ם וסירים ממתכת</td><td>מדיח או שטיפה רגילה מספיקים</td><td>משטח חלק נשטף היטב</td></tr>
<tr><td>מקפיא ומזווה</td><td>מגירה ומדף נפרדים</td><td>פירורים "מטיילים"</td></tr>
</tbody></table></div>

<h2>הרגלי עבודה</h2>
<ul>
<li><b>עובדים מהנקי למלוכלך:</b> קודם מכינים את האוכל ללא גלוטן, אחר כך את הרגיל.</li>
<li><b>שוטפים ידיים</b> בין נגיעה בלחם רגיל לבין הכנת אוכל ללא גלוטן. גם מגבת וסמרטוט יכולים להעביר פירורים.</li>
<li><b>ממרחים:</b> סכין שנגעה בלחם רגיל לא חוזרת לקופסה. מוציאים בכפית נקייה לצלחת, או מחזיקים קופסה נפרדת.</li>
<li><b>בתנור:</b> מחממים מאפה רגיל על נייר אפייה, ומכסים כשמחממים יחד.</li>
</ul>

<h2>קניות</h2>
<ul>
<li><b>רק מוצרים ארוזים ומסומנים.</b> לא קונים בתפזורת: פיצוחים, פירות יבשים, ממתקים, תבלינים וזיתים מערימות.</li>
<li><b>קמח מסתתר במקומות לא צפויים:</b> בקימוח אגוזים ופירות יבשים, בתבלינים, ברוטב סויה רגיל.</li>
<li><b>קטניות יבשות:</b> בוררים ושוטפים לפני בישול. לפעמים נמצאים בהן גרגירי חיטה מהשדה.</li>
<li><b>ממתקים מיובאים בלי סימון ברור</b> (לרוב בשקיות קטנות במשלוחי מנות) לא אוכלים.</li>
</ul>

<h2>קריאת תווית</h2>
<div class="yesno">
<div class="y"><h3>מותר</h3><ul><li>"ללא גלוטן" או "נטול גלוטן"</li><li>"עד 20ppm" (20 חלקים למיליון)</li></ul></div>
<div class="n"><h3>אסור</h3><ul><li>חיטה, שעורה, שיפון, כוסמין, לתת, סובין ברכיבים</li><li>"מכיל גלוטן"</li><li>"עלול להכיל" או "חשש לעקבות"</li></ul></div>
</div>
<div class="callout"><p><b>אין סימון בכלל?</b> בודקים באפליקציה "חופשי מגלוטן". לא מופיע? הכלל הוא: אם יש ספק, אין ספק. לא אוכלים.</p>
<p>קוראים תמיד את רשימת הרכיבים, לא רק את תיבת האלרגנים.</p></div>

<h2>קמחים ואפייה</h2>
<ul>
<li><b>קמחי מקור:</b> אורז, חומוס, כוסמת, שקדים. <b>עמילנים:</b> קורנפלור, תפוח אדמה, טפיוקה. <b>תערובות</b> משלבות ביניהם.</li>
<li>כדאי להתחיל עם 2–3 תערובות מוכרות ומתכונים שעובדים, ורק אחר כך להתנסות.</li>
<li>בצק ללא גלוטן דביק יותר ומתייבש מהר. מאפים נשמרים טוב במקפיא.</li>
<li>קמח קונדיטור ללא גלוטן מסובסד על ידי משרד הבריאות ונמכר בזול בסופר. ראו <a href="rights.html#flour">זכויות</a>.</li>
</ul>
{sources("guide", "mom", "kz")}
""")

# ---------------- BIRTHDAYS ----------------
PAGES["birthdays.html"] = ("ימי הולדת", False, f"""
<h1>ימי הולדת</h1>
<p class="lead">העמוד הזה בשבילנו, ההורים לילד/ה עם צליאק: איך מתכוננים לכל יום הולדת, ומה שולחים להורים החוגגים.</p>

<div class="callout green">
<p><b>הדף לשליחה להורים החוגגים:</b> <a href="hosts.html">דף לחוגגים</a>. בדף שלושה כללים פשוטים ורשימת קניות.</p>
<div class="share" style="justify-content:flex-start"><a class="btn wa" data-wa="hosts.html" href="hosts.html">שליחה בוואטסאפ</a></div>
</div>
<script>
(function () {{
  var base = location.href.split('#')[0].replace(/[^/]*$/, '');
  document.querySelectorAll('[data-wa]').forEach(function (a) {{
    a.href = 'https://wa.me/?text=' + encodeURIComponent('הילד/ה שלנו מגיע/ה ליום ההולדת! ריכזנו כאן בקצרה מה עוזר:\\n' + base + a.dataset.wa);
  }});
}})();
</script>

<div class="story">
<h3>מה קרה לתומר</h3>
<p>תומר, הבן שלי, הוזמן ליום הולדת. ההורים החוגגים ידעו שיש לו צליאק, ואפילו הזמינו לו פיצה מיוחדת. אבל על השולחן היה גם ביסלי, ליד חטיף שהיה אמור להיות בטוח. הילדים אכלו ביסלי, ואז הכניסו את אותן ידיים לקערה השנייה. תומר אכל ממנה וחזר הביתה עם כאבי בטן.</p>
<p>זה נקרא <b>זיהום משני</b>: המזון עצמו לא מכיל גלוטן, אבל פירורים של מזון עם גלוטן הגיעו אליו. לילד/ה עם צליאק זה כאילו אכל גלוטן.</p>
</div>

<h2>איך מתכוננים</h2>
<ol class="steps">
<li><b>בתחילת השנה</b>שולחים לקבוצת הורי הכיתה את <a href="hosts.html">הדף לחוגגים</a>. בדף יש קישור ל<a href="snacks.html">רשימת החטיפים</a>.</li>
<li><b>שבועיים לפני כל מסיבה</b>מתקשרים ושואלים מה יוגש: חטיפים, פיצה, עוגה, שקית הפתעות.</li>
<li><b>מביאים מה שההורים החוגגים לא יכולים לספק</b>מאפין מהמקפיא עם קישוט, פיצה מהבית, והכי דומה למה שכולם מקבלים.</li>
<li><b>כשהשולחן מעורב</b>מגיעים מוקדם, ממלאים לילד צלחת משקיות שרק נפתחו, ומבקשים לשמור לו שקית סגורה.</li>
<li><b>מכינים את הילד</b>מה יהיה שם, מה שלו ומה לא. מלמדים אותו לא לאכול מקערה שכולם מכניסים אליה ידיים.</li>
<li><b>בלי כעס</b>לא לכולם יש זמן או ידע. כשאין שיתוף פעולה, שולחים אוכל מהבית שהילד בחר.</li>
</ol>
<div class="callout"><p><b>טיפ למקפיא:</b> אופים עוגת שוקולד ללא גלוטן בתבניות מאפינס ומקפיאים. ביום ההולדת מוסיפים בצק סוכר וסוכריות (גם הם ללא גלוטן), ויש עוגה אישית כמו לכולם.</p></div>
{sources("guide", "mom")}
""")

# ---------------- HOSTS (fixed sheet) ----------------
PAGES["hosts.html"] = ("דף לחוגגים", False, """
<article class="host" aria-labelledby="h-title">
  <header class="host-top">
    <h1 id="h-title">הילד/ה שלנו מגיע/ה ליום ההולדת!</h1>
    <p>תודה שאתם דואגים שירגיש/תרגיש כמו כולם. ריכזנו כאן בקצרה מה עוזר.</p>
  </header>
  <div class="what">
    <b>קצת עלינו</b>
    <p>יש לו/לה צליאק. זה אומר שהגוף נפגע מגלוטן, חלבון שיש בחיטה, שעורה ושיפון. אין תרופה, והדרך היחידה לשמור עליו/ה היא לא לאכול גלוטן בכלל, אפילו לא פירור. זה נשמע מסובך, אבל בפועל אלה 3 דברים פשוטים:</p>
  </div>

  <ol class="three">
    <li>
      <span class="num" aria-hidden="true">1</span>
      <div>
        <h2>נשמח שתקנו חטיפים וממתקים שכתוב עליהם <span class="tag">ללא גלוטן</span></h2>
        <p>לכל הילדים, לא רק לו/לה. ככה כולם אוכלים מאותן קערות, ואף אחד לא מרגיש שונה.</p>
      </div>
    </li>
    <li class="stop">
      <span class="num" aria-hidden="true">2</span>
      <div>
        <h2>נבקש בלי ביסלי, בייגלה ועוגיות על שולחן החטיפים</h2>
        <p>גם לא רק לשאר הילדים: ילד שאכל ביסלי והכניס יד לקערת הצ׳יפס, והצ׳יפס כבר לא בטוח לו/לה. יש להם תחליפים ללא גלוטן במדף "ללא גלוטן" ברשתות.</p>
      </div>
    </li>
    <li>
      <span class="num" aria-hidden="true">3</span>
      <div>
        <h2>פיצה ועוגה? נתאם מראש</h2>
        <p>פיצה ועוגה רגילות לשאר הילדים זה בסדר, רק צריך לדאוג גם לו/לה. אתם יכולים להזמין לו/לה פיצה ללא גלוטן (נשמח להמליץ מאיפה), או שאנחנו נביא פיצה ועוגה ללא גלוטן. מה שנוח לכם, רק נתאם מראש. בכל מקרה, נשמח שתחממו על נייר אפייה נקי, ותגישו לו/לה ראשונים בצלחת נפרדת.</p>
      </div>
    </li>
  </ol>

""" + _V0.label_box() + """
  <section class="shop" aria-label="רשימת קניות">
    <div class="col y">
      <h2>✓ מה כדאי לקנות</h2>
      <ul>
        <li><b>חטיפים שבדקנו:</b> במבה (בלי מילוי), אפרופו, דובונים, תפוצ'יפס, צ'יטוס, שוקולד פרה</li>
        <li><b>סוכריות גומי, מרשמלו, שלוקים וקרטיבים:</b> רק כשכתוב עליהם "ללא גלוטן"</li>
        <li><b>תמיד מתאים:</b> פירות וירקות</li>
      </ul>
      <p class="note">יש עוד הרבה חטיפים מתאימים, וכל הזמן יוצאים חדשים. מה שקובע הוא מה שכתוב על האריזה: "ללא גלוטן" קונים, "עלול להכיל גלוטן" לא. <a href="snacks.html">לרשימה המלאה, עם מקור לכל מוצר</a></p>
    </div>
    <div class="col n">
      <h2>✗ על מה לוותר</h2>
      <ul>
        <li>ביסלי, בייגלה רגיל, קרקרים</li>
        <li>עוגיות וופלים רגילים. יש להם תחליפים ללא גלוטן במדף "ללא גלוטן" בסופר</li>
        <li>מוצרים שכתוב עליהם "עלול להכיל גלוטן"</li>
        <li>ממתקים בתפזורת</li>
      </ul>
    </div>
  </section>

  <p class="call">לא בטוחים במשהו? <b>שלחו לנו תמונה של האריזה בוואטסאפ</b>, נענה מהר. אין שאלה מיותרת.</p>

  <details class="more">
    <summary>עוד כמה דברים קטנים שעוזרים לנו</summary>
    <ul>
      <li>נשמח שתגישו לו/לה <b>ראשונים</b>, משקית שרק נפתחה, לפני שכל הידיים בפנים. אפשר גם לשמור לו/לה שקית סגורה בצד.</li>
      <li><b>פעילויות עם קמח</b> (משחקי קמח, בצק משחק רגיל, אפיית עוגיות) מפזרות גלוטן בכל הסביבה, ולכן מוותרים עליהן.</li>
      <li><b>בעמדת איפור:</b> בלי שפתון.</li>
      <li><b>בשקית ההפתעות:</b> רק ממתקים ארוזים, עם סימון בעברית.</li>
    </ul>
  </details>

  <p class="thanks">תודה ענקית! זה באמת עושה לנו את היום.</p>
""" + V_HOSTS_BASED + """
  <p class="sm">הדף נכתב בהתנדבות על ידי הורים לילדים עם צליאק. אינו ייעוץ רפואי. רכיבים משתנים, תמיד בודקים את האריזה.</p>
</article>

""" + SHARE + """
""")

PAGES["playdate.html"] = ("מגיע אליכם לשחק", False, """
<article class="host" aria-labelledby="p-title">
  <header class="host-top">
    <h1 id="p-title">הילד/ה שלנו בא/ה אליכם לשחק!</h1>
    <p>איזה כיף. כמה מילים קטנות על אוכל, כדי שיהיה לכם קל.</p>
  </header>
  <div class="what">
    <b>קצת עלינו</b>
    <p>יש לו/לה צליאק. זה אומר שהגוף נפגע מגלוטן, חלבון שיש בחיטה, שעורה ושיפון. אין תרופה, והדרך היחידה לשמור עליו/ה היא לא לאכול גלוטן בכלל, אפילו לא פירור. זה נשמע מסובך, אבל בפועל אלה 3 דברים פשוטים:</p>
  </div>

  <ol class="three">
    <li>
      <span class="num" aria-hidden="true">1</span>
      <div>
        <h2>ידיים וכלים נקיים</h2>
        <p>אם נגעתם בלחם או בפסטה, נשמח שתשטפו ידיים לפני שמכינים לו/לה. סכין שנגעה בלחם לא חוזרת לממרח, וירקות חותכים על צלחת ולא על הקרש.</p>
      </div>
    </li>
    <li>
      <span class="num" aria-hidden="true">2</span>
      <div>
        <h2>מגישים לו/לה קודם, על צלחת נקייה</h2>
        <p>עוד לפני שמניחים לחם או חלה על השולחן. פירור לחם שנופל על הצלחת מספיק כדי להזיק.</p>
      </div>
    </li>
    <li>
      <span class="num" aria-hidden="true">3</span>
      <div>
        <h2>שלחנו לחם בתיק? אתם רק ממלאים</h2>
        <p>בדרך כלל נשלח איתו/ה לחם או סנדוויץ' ללא גלוטן, כדי שלא תצטרכו לחפש.</p>
      </div>
    </li>
  </ol>

""" + _V0.label_box() + """
  <section class="shop" aria-label="מה אפשר להגיש">
    <div class="col y">
      <h2>✓ מה אפשר להגיש</h2>
      <ul>
        <li>פירות וירקות</li>
        <li>חביתה, ביצה, אורז, תפוח אדמה</li>
        <li>גבינות וממרחים מקופסה שעוד לא נפתחה</li>
        <li>חטיפים שבדקנו: במבה (בלי מילוי), אפרופו, תפוצ'יפס, שוקולד פרה</li>
      </ul>
      <p class="note">יש עוד הרבה חטיפים מתאימים, וכל הזמן יוצאים חדשים. מה שקובע הוא מה שכתוב על האריזה: "ללא גלוטן" קונים, "עלול להכיל גלוטן" לא. <a href="snacks.html">לרשימה המלאה, עם מקור לכל מוצר</a></p>
    </div>
    <div class="col n">
      <h2>✗ על מה לוותר</h2>
      <ul>
        <li>לחם, פיתה, פסטה, שניצל</li>
        <li>עוגיות, עוגה, קורנפלקס</li>
        <li>אבקת מרק, רוטב סויה רגיל</li>
        <li>מוצרים שכתוב עליהם "עלול להכיל גלוטן"</li>
      </ul>
    </div>
  </section>

  <p class="call">לא בטוחים? <b>שלחו לנו תמונה של האריזה בוואטסאפ</b>, נענה מהר. וגם הילד/ה שלנו יודע/ת מה מותר.</p>

  <details class="more">
    <summary>עוד קצת הסבר (למי שרוצה)</summary>
    <ul>
      <li>הרבה פעמים הבעיה היא לא האוכל עצמו. מספיק שהאוכל נגע במשהו שנגע קודם בלחם: סכין, קרש חיתוך, מגבת או יד.</li>
      <li>תבלינים, רטבים ואבקות מרק לפעמים מכילים קמח. אם לא כתוב עליהם "ללא גלוטן", מוותרים עליהם.</li>
    </ul>
  </details>

  <p class="thanks">תודה שאתם מארחים אותו/ה באהבה!</p>
""" + V_HOSTS_BASED + """
  <p class="sm">הדף נכתב בהתנדבות על ידי הורים לילדים עם צליאק. אינו ייעוץ רפואי. רכיבים משתנים, תמיד בודקים את האריזה.</p>
</article>
""" + SHARE)

PAGES["snacks.html"] = ("רשימת חטיפים ללא גלוטן", False, f"""
<h1>מה אפשר לקנות? רשימת חטיפים וממתקים</h1>
<p class="lead">דוגמאות לחטיפים וממתקים שמוכרים בכל סופר ומתאימים לילדים עם צליאק. אפשר לקנות מהם לכל הילדים, ביום הולדת וגם כשמארחים בבית.</p>

<div class="callout red">
<p><b>הכלל שמעל הרשימה:</b> קונים רק אריזה שכתוב עליה <b>"ללא גלוטן"</b>, או שיש עליה את סמל הפרח של שטראוס-עלית. לפעמים רק חלק מהטעמים בסדרה מתאים, ויצרנים משנים רכיבים. מה שכתוב על האריזה קובע, לא הרשימה.</p>
</div>

<div class="legend">
<p><span class="chip ok">יש מקור</span> מופיע בהודעה של היצרן, בכתבה או בתווית של חנות מקוונת.</p>
<p><span class="chip chk">לבדוק</span> מרשימות של הורים. סביר, אבל עוד לא אימתנו מול מקור רשמי.</p>
</div>

<h2>חטיפים מלוחים</h2>
<div class="tbl"><table>
<thead><tr><th>מוצר</th><th>לשים לב</th><th>סטטוס</th></tr></thead>
<tbody>
<tr><td><b>במבה</b> (אסם)</td><td>הבמבה הקלאסית מסומנת "ללא גלוטן". לא במבה במילוי נוגט או שוקולד.</td><td><span class="chip ok">יש מקור</span></td></tr>
<tr><td><b>תפוצ'יפס</b></td><td>רוב הסדרה מסומנת. לא הסדרה האפויה.</td><td><span class="chip ok">יש מקור</span></td></tr>
<tr><td><b>דוריטוס</b></td><td>הרכיבים בטעם הרגיל: תירס, שמן ומלח. בטעמים אחרים בודקים את הסימון.</td><td><span class="chip chk">לבדוק</span></td></tr>
<tr><td><b>צ'יטוס</b></td><td>שטראוס הודיעה שתסמן את צ'יטוס כמתאים. בודקים כל טעם.</td><td><span class="chip ok">יש מקור</span></td></tr>
<tr><td><b>דובונים</b> (אסם)</td><td>לפי רשימות הורים, כל הסדרה.</td><td><span class="chip chk">לבדוק</span></td></tr>
<tr><td><b>אפרופו</b> (אסם)</td><td>רק הקלאסי. לא איטלקי ולא שוקולד.</td><td><span class="chip chk">לבדוק</span></td></tr>
<tr><td><b>פריכיות טעימות</b> (שטראוס Energy)</td><td>סדרת פריכיות אורז ותירס, מלוחות ומתוקות.</td><td><span class="chip ok">יש מקור</span></td></tr>
</tbody></table></div>

<h2>ממתקים ושוקולד</h2>
<div class="tbl"><table>
<thead><tr><th>מוצר</th><th>לשים לב</th><th>סטטוס</th></tr></thead>
<tbody>
<tr><td><b>שוקולד פרה חלב ומריר</b> (עלית)</td><td>מחפשים את סמל הפרח. לא כל טבלה בסדרה.</td><td><span class="chip ok">יש מקור</span></td></tr>
<tr><td><b>סוכריות גומי ומרשמלו</b></td><td>רק בחבילה סגורה ומסומנת. יש מותגים עם גלוטן, ורוב "שטיחי הגומי" מכילים גלוטן.</td><td><span class="chip chk">לבדוק</span></td></tr>
<tr><td><b>סוכריות על מקל, טופי, מנטוס</b></td><td>לפי רשימות הורים. בודקים כל אריזה.</td><td><span class="chip chk">לבדוק</span></td></tr>
<tr><td><b>מקופלת, פסק זמן, כיף כף</b></td><td><b>רק</b> במהדורה המיוחדת שמסומנת "ללא גלוטן". הגרסה הרגילה לא מתאימה.</td><td><span class="chip ok">יש מקור</span></td></tr>
</tbody></table></div>

<h2>קפוא ומרענן</h2>
<div class="tbl"><table>
<thead><tr><th>מוצר</th><th>לשים לב</th><th>סטטוס</th></tr></thead>
<tbody>
<tr><td><b>שלוקים וקרטיבי קרח</b></td><td>לפי רשימות הורים. קוראים את הסימון על כל אחד.</td><td><span class="chip chk">לבדוק</span></td></tr>
<tr><td><b>גלידות וארטיקים</b></td><td>רק עם סימון "ללא גלוטן". בלי עוגיות, וופל או גביע.</td><td><span class="chip chk">לבדוק</span></td></tr>
<tr><td><b>פירות וירקות</b></td><td>מתאימים תמיד. חותכים על צלחת נקייה, לא על קרש שנחתך עליו לחם.</td><td><span class="chip ok">בטוח</span></td></tr>
</tbody></table></div>

<h2>לא קונים, גם אם זה נראה תמים</h2>
<ul>
<li>ביסלי, בייגלה רגיל, קרקרים, וופלים, עוגיות וחטיפי דגנים</li>
<li>מוצרים שכתוב עליהם "עלול להכיל גלוטן" או "חשש לעקבות גלוטן"</li>
<li>ממתקים בתפזורת, ופיצוחים או פירות יבשים לא ארוזים</li>
<li>ממתקים מיובאים בלי סימון בעברית, למשל שקיות קטנות של משלוח מנות</li>
</ul>

<div class="callout"><p><b>לא בטוחים?</b> מצלמים את האריזה ושולחים להורים של הילד/ה. או סורקים את הברקוד באפליקציה "חופשי מגלוטן".</p></div>

<p class="asof">טיוטה. הרשימה נכונה ל-{UPDATED} ומתעדכנת מעת לעת. מצאתם מוצר שהשתנה? כתבו לנו: {mail()}</p>
<div class="sources"><b>מקורות</b><ul>
<li><a href="https://www.israelhayom.co.il/article/708783">ישראל היום – אסם תסמן את מוצרי הבמבה הקלאסיים "ללא גלוטן"</a></li>
<li><a href="https://www.foodis.co.il/%D7%91%D7%A9%D7%95%D7%A8%D7%94-%D7%9C%D7%99%D7%9C%D7%93%D7%99%D7%9D-%D7%A8%D7%92%D7%99%D7%A9%D7%99%D7%9D-%D7%90%D7%95-%D7%A0%D7%9E%D7%A0%D7%A2%D7%99%D7%9D-%D7%9E%D7%92%D7%9C%D7%95%D7%98/">פודיס – שטראוס פריטו ליי מרחיבה את החטיפים המלוחים ללא גלוטן (צ'יטוס, שוש, תפוצ'יפס)</a></li>
<li><a href="https://deli.yango.com/he-il/good/tapuchips-grill-flavored-crunchy-potato-chips-50-gram">Yango Deli – תווית תפוצ'יפס "ללא גלוטן"</a> · <a href="https://deli.yango.com/he-il/good/doritos-corn-snack-70-gram">רכיבי דוריטוס</a></li>
<li><a href="https://www.maariv.co.il/economy/consumerism/article-1342120">מעריב – סדרת החטיפים ללא גלוטן של שטראוס ועלית</a></li>
<li><a href="https://www.foodis.co.il/%D7%9E%D7%A2%D7%AA%D7%94-%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%94%D7%A9%D7%95%D7%A7%D7%95%D7%9C%D7%93-%D7%9E%D7%A8%D7%99%D7%A8-%D7%A9%D7%9C-%D7%A2%D7%9C%D7%99%D7%AA-%D7%9C%D7%9C%D7%90/">פודיס – שוקולד פרה מריר ללא גלוטן, סימון בפרח</a> · <a href="https://www.strauss-group.com/faq/which-products-are-suitable-for-people-who-are-sensitive-to-gluten">שטראוס – שוקולד פרה חלב</a></li>
<li><a href="https://www.bhol.co.il/news/1465662">בחדרי חרדים – מהדורה מיוחדת ללא גלוטן של פסק זמן, כיף כף ומקופלת</a></li>
<li>רשימת "דוגמאות לחטיפים וממתקים ללא גלוטן" (תמי וקנין) וסיכום של אמא לילדה עם צליאק – רשימות הורים</li>
</ul></div>
""")

# ---------------- SCHOOL ----------------
PAGES["school.html"] = ("גן ובית ספר", False, f"""
<h1>גן ובית ספר</h1>
<p class="lead">יש חוזר מנכ"ל של משרד החינוך שמחייב את המסגרת להתאים כל פעילות עם אוכל לילד/ה עם צליאק. התפקיד שלנו: להביא את החוזר, להסביר, ולהתכונן מראש.</p>

<h2>מה החוזר אומר, בקצרה</h2>
<ul>
<li>ילד/ה עם צליאק משתתף בכל פעילות, כשווה בין שווים.</li>
<li>בכל פעילות עם מזון או חומרים שמכילים גלוטן, המסגרת דואגת, יחד עם ההורים, לחלופה מתאימה. זה כולל יצירה, ואפייה לקראת חגים.</li>
<li>במסגרות עם הזנה, הילד מקבל מנה מותאמת, מגוונת וטעימה.</li>
<li>בטיולים ובמסעות, המסגרת נערכת מראש למנת מזון מתאימה.</li>
<li>מנהל המוסד אחראי להגביר את הידע והמודעות של הצוות.</li>
</ul>
<p>משרד החינוך פרסם ב-2026 גם חוברות "שמים לצליאק" לגנים, ליסודי ולעל-יסודי. כדאי להביא את החוברת המתאימה לפגישה.</p>

<h2>הפגישה הראשונה</h2>
<ol class="steps">
<li><b>עם מי:</b>המחנכת או הגננת, היועצת, והמנהלת. בצהרון: גם האחראית על האוכל.</li>
<li><b>מה מביאים:</b>את חוזר המנכ"ל, את חוברת "שמים לצליאק" המתאימה, ואת <a href="hosts.html">הדף לחוגגים</a> להורי הכיתה.</li>
<li><b>מה מבקשים:</b>הודעה מראש על כל פעילות עם אוכל, כדי שנספיק להתארגן.</li>
<li><b>הסבר לכיתה:</b>אפשר לבוא עם הילד ולהסביר לילדים, לפי הגיל. הם אלה שיעזרו לו ביומיום.</li>
</ol>

<h2>"על כל מקרה שלא יבוא"</h2>
<ul>
<li><b>קופסת חירום בכיתה:</b> חטיף מלוח, חטיף מתוק, סוכריה על מקל, טופי. אצל המורה, במקום שהילד מכיר.</li>
<li><b>מאפינס במקפיא של חדר המורים:</b> בקופסה עם שם וכיתה. מישהו הביא עוגה? חצי דקה במיקרו.</li>
<li><b>בקיץ:</b> כמה קרטיבים מתאימים במקפיא של המסגרת.</li>
</ul>

<h2>דברים שקל לשכוח</h2>
<ul>
<li><b>בצק משחק</b> רגיל מכיל גלוטן. מבקשים בצק ללא גלוטן.</li>
<li><b>משחקי קמח</b> (למצוא סוכריה בקמח) מזהמים את כל הסביבה.</li>
<li><b>איפור בפורים:</b> לא מורחים לילד שפתון.</li>
<li><b>חגים:</b> סופגניות, אוזני המן, משלוח מנות, מצות בסדר הכיתתי שבועיים לפני פסח. מבקשים לדעת מראש.</li>
<li><b>עוגה ביתית של הורה מהכיתה:</b> גם בכוונה טובה, מטבח רגיל עלול לזהם. עדיף מאפין מהבית שלנו.</li>
</ul>

<h2>טיולים</h2>
<ul>
<li><b>פיתה בטאבון:</b> מכינים בבית בצק ללא גלוטן, עוטפים בנייר כסף ושולחים, עם ממרח וזעתר מתאימים.</li>
<li><b>טיול שנתי עם לינה:</b> מתקשרים ישירות למקום ולאחראי על חדר האוכל, ומוודאים שהם מבינים מה זה "ללא גלוטן".</li>
<li><b>תמיד</b> שולחים אוכל גיבוי.</li>
</ul>
{sources("circ", "sim_gan", "sim_yes", "sim_al", "edu", "guide", "mom")}
""")

# ---------------- OUTSIDE ----------------
PAGES["outside.html"] = ("מחוץ לבית", False, f"""
<h1>מחוץ לבית</h1>
<p class="lead">הכלל הראשון: לא יוצאים מהבית בלי אוכל. גם בעיר גדולה, למצוא אוכל מתאים קשה יותר ממה שנדמה.</p>

<h2>הולכים לחברים</h2>
<ul>
<li><b>לא להתבייש להזכיר.</b> גם הורים שכבר יודעים יכולים לשכוח. הודעה קצרה לפני כל ביקור זה בסדר גמור.</li>
<li><b>שולחים להורים המארחים את <a href="playdate.html">הדף "מגיע אליכם לשחק"</a>.</b> שלושה כללים קצרים, בלי להלחיץ.</li>
<li><b>לחם בתיק:</b> בימים שתומר הולך לחברים, אני שמה לו בתיק סנדוויץ' ללא גלוטן, בלי מילוי. המארחים רק ממלאים, ואף אחד לא צריך לחפש לחם מתאים.</li>
<li><b>חטיף לחלוק:</b> אפשר לשלוח חטיף ללא גלוטן שכל הילדים יאכלו ממנו יחד.</li>
<li><b>מלמדים את הילד לשאול:</b> "יש על זה ללא גלוטן?", ולהגיד "לא תודה" כשלא בטוח.</li>
</ul>

<h2>אצל סבא וסבתא</h2>
<ul>
<li>מלמדים את העקרונות, ובהתחלה מתאמים מראש מה יוגש. בארוחות הראשונות מביאים יותר מהבית.</li>
<li>אצל סבא וסבתא שמארחים הרבה: סט תבלינים ללא גלוטן, מדף קטן עם מוצרי בסיס, קרש חיתוך ומסננת נפרדים.</li>
<li><b>טעויות נפוצות:</b> אבקת מרק עם גלוטן, רוטב סויה רגיל, חלה שמועברת מעל הצלחות ומפזרת פירורים.</li>
<li>מושיבים את הילד בצד השני של השולחן מהלחם, ומגישים לו ראשון.</li>
</ul>

<h2>מסעדות</h2>
<ul>
<li>בודקים בטלפון מראש. מסעדה עם תפריט מסומן ועובדים שמחליפים כפפות היא מסעדה שחוזרים אליה.</li>
<li><b>פסטה ללא גלוטן:</b> מוודאים שבושלה בסיר נקי ובמים נקיים.</li>
<li><b>צ'יפס:</b> שואלים אם מטוגן באותו שמן עם שניצל או טבעות בצל.</li>
<li><b>סושי ומוקפצים:</b> רוטב סויה רגיל מכיל גלוטן. מוודאים שהסויה מתאימה ושאין טמפורה.</li>
<li><b>פיצריות וגלידריות:</b> סיכון גבוה לזיהום. יש משפחות שמוותרות לגמרי, ויש שבוחרות מקומות מוכרים ובטוחים.</li>
<li>אם אין כלום בתפריט: אפשר לבקש בשר או דג על נייר אלומיניום, עם מלח ופלפל בלבד.</li>
</ul>

<h2>בדרכים</h2>
<ul>
<li><b>בתיק:</b> חטיפים, בייגלה ופריכיות ללא גלוטן (לא כל פריכיות האורז מתאימות), כריכים ופירות.</li>
<li><b>נתקעתם?</b> בכל סופר או חנות בתחנת דלק יש שימורי תירס, קוטג' ומעדנים מסומנים.</li>
<li><b>פופקורן בקולנוע:</b> לפעמים תערובת המלח מכילה גלוטן. עדיף חטיף סגור או פופקורן מתאים מהבית.</li>
<li><b>ארטיקים וגלידות:</b> קוראים את הסימון על כל אחד.</li>
</ul>
{sources("guide", "mom")}
""")

# ---------------- RIGHTS ----------------
PAGES["rights.html"] = ("זכויות", False, f"""
<h1>זכויות: מה מגיע ומה לא</h1>
<p class="lead">בכנות: אין קצבה או הטבה כספית ייעודית להורים לילדים עם צליאק. רוב ההטבות להורים תלויות בגמלת ילד נכה, וצליאק לבדה בדרך כלל לא מזכה בה. אלה הזכויות שכן קיימות.</p>

<h2>מה כן מגיע</h2>
<div class="tbl"><table>
<thead><tr><th>זכות</th><th>מה זה אומר</th></tr></thead>
<tbody>
<tr><td>התאמות במסגרות החינוך</td><td>חוזר מנכ"ל מחייב חלופה מתאימה בכל פעילות עם אוכל, כולל טיולים וחגים. מנות מזון לתלמידים עם צליאק צריכות להיות ארוזות בצבע שונה ומסומנות. ראו <a href="school.html">גן ובית ספר</a>.</td></tr>
<tr><td>תרופה חלופית</td><td>אם התרופה שבסל הבריאות לא מתאימה לחולה צליאק, יש זכות לקבל חלופה מתאימה.</td></tr>
<tr><td>תקרת תשלום לחולה כרוני</td><td>הורים לילדים עם מחלה כרונית לא משלמים על תרופות מהסל מעבר לתקרה מסוימת. רלוונטי בעיקר כשיש גם תרופות קבועות.</td></tr>
<tr><td>סימון מזון</td><td>מוצר שמכיל גלוטן חייב לציין ברשימת הרכיבים את מקור הגלוטן ואת המילים "מכיל גלוטן".</td></tr>
<tr><td>צבא</td><td>מתגייסים כרגיל, עם סעיף צליאק בפרופיל, ומקבלים דמי כלכלה לרכישת מזון. יש מגבלה על חלק מהיחידות המובחרות.</td></tr>
</tbody></table></div>

<h2 id="flour">הקמח המסובסד</h2>
<ul>
<li><b>לא צריך להגיש כלום.</b> משרד הבריאות מסבסד את הקמח כבר אצל היצרן, והוא נמכר בסופר במחיר נמוך לכל מי שקונה.</li>
<li>היום מסובסד קמח קונדיטור ללא גלוטן, שהוא עמילני ודל בסיבים.</li>
<li>ביולי 2026 פורסם שמשרד הבריאות יצא במכרז לקמח איכותי יותר, במחיר צפוי של כ-5 ש"ח לק"ג.</li>
<li>בכנסת עלה שרוב תקציב הסבסוד לא מנוצל, בין השאר כי קשה למצוא את המוצרים. לא מוצאים בסניף? מבקשים מהמנהל להזמין.</li>
</ul>

<h2>מתי כן לבדוק גמלת ילד נכה</h2>
<p>אם יש לילד גם מחלה נוספת, סיבוכים, או צורך בהשגחה מיוחדת. מגישים תביעה באזור האישי באתר ביטוח לאומי או במוקד ‎*3928. אם שני ילדים במשפחה זכאים, הגמלה לכל אחד מהם גדלה.</p>
<div class="callout"><p>לפני שמוותרים, כדאי לפנות לארגון זכויות הצליאק ולשאול על הטבות מקומיות או חדשות.</p></div>
{sources("kz", "kzparents", "kzclaim", "ynet", "bhol", "maariv", "circ")}
""")

# ---------------- RESOURCES ----------------
PAGES["resources.html"] = ("עמותות ומקורות", False, f"""
<h1>עמותות, קהילה ומקורות</h1>
<p class="lead">לא צריך לעבור את זה לבד. אלה הגופים והמקורות שעזרו לנו.</p>

<h2>ארגונים</h2>
<ul>
<li>{L["org"]}: מקדם זכויות במערכת החינוך ובצבא, ויש לו פרויקט ליווי למשפחות חדשות. טלפון (לפי האתר): ‎053-7541491, מייל: maavak.c@gmail.com.</li>
<li>{L["newpat"]}</li>
<li>הדיאטנית בקופת החולים שלכם.</li>
</ul>

<h2>קהילה</h2>
<ul>
<li>קבוצת הפייסבוק "צליאק – ללא גלוטן – הקבוצה הרשמית".</li>
<li>קבוצות אינסטגרם ווואטסאפ מקומיות: מספרות על בתי עסק מתאימים באזור.</li>
<li>האפליקציה "חופשי מגלוטן" לסריקת ברקודים.</li>
</ul>

<h2>מדריכים ומסמכים</h2>
<ul>
<li>{L["guide"]} (2017)</li>
<li>{L["circ"]}</li>
<li>{L["sim_gan"]} · {L["sim_yes"]} · {L["sim_al"]}</li>
<li>{L["edu"]}</li>
<li>{L["maccabi"]}</li>
<li>{L["diag"]}</li>
</ul>

<h2>זכויות וקמח מסובסד</h2>
<ul>
<li>{L["kz"]}</li>
<li>{L["kzparents"]}</li>
<li>{L["kzclaim"]}</li>
<li>{L["ynet"]}</li>
<li>{L["bhol"]}</li>
<li>{L["maariv"]}</li>
</ul>

<h2>מקורות אישיים</h2>
<ul>
<li>{L["mom"]}</li>
<li>הניסיון של המשפחה שלנו.</li>
</ul>
""")

# ---------------- ABOUT ----------------
PAGES["about.html"] = ("על האתר", False, f"""
<h1>על האתר</h1>

<h2 id="story">הסיפור שלי ולמה הקמתי את האתר</h2>
<p>שמי {AUTHOR}, ואני אמא לשני ילדים עם צליאק. קודם אובחן הבן שלי, תומר. אחרי האבחון שלו בדקנו את כל המשפחה, וגילינו צליאק גם אצל הבת, לירון.</p>
<p>ברגע האבחון החיים משתנים. פתאום צריך ללמוד מה מותר ומה אסור, לנקות את המטבח, לקרוא כל תווית, להסביר לגן ולבית הספר, ולהבין מה מגיע לנו. המידע קיים, אבל הוא מפוזר בין הרבה מקומות. הרגשתי שאין מקום אחד שעושה סדר.</p>
<p>תומר חזר פעם מיום הולדת עם כאבי בטן, למרות שהזמינו לו פיצה מיוחדת, רק כי על השולחן היה גם ביסלי. הבנתי שצריך להסביר להורים האחרים בצורה פשוטה וברורה, בלי להלחיץ.</p>
<p>הקמתי את האתר הזה למען הורים שרק קיבלו אבחנה ולא יודעים מאיפה להתחיל, ולמען הקניית מידע משמעותי שיגן על הילדים עם צליאק מחשיפה לגלוטן.</p>
<p>המטרה שלי היא שכל הורה לילד/ה עם צליאק שהולכים לחברים ישלח למארחים את <a href="playdate.html">דף ההסבר</a>, ושכל הורה לילד/ה עם צליאק שהולכים ליום הולדת ישלח מראש את <a href="hosts.html">דף ההסבר</a> למארגנים.</p>
<p>זה אתר פרטי שנכתב בהתנדבות. אין לי ממנו שום רווח: אין פרסומות, לא מבקשים תרומות, ואין קשר לאף גוף או עמותה. המידע נאסף ממקורות רשמיים, מאתרי הארגונים ומניסיון של הורים, וליד כל נושא יש קישור למקור.</p>
<p>מצאת טעות, או רוצה לשתף? אשמח לשמוע: {mail()}</p>
<p>{AUTHOR}</p>

<h2>מקורות המידע</h2>
<p>המידע באתר נבדק מול מקורות רשמיים ומול אתרי הארגונים, ונכון ל-{UPDATED}. בכל עמוד מופיעים המקורות שלו.</p>
<div class="tbl"><table>
<thead><tr><th>מקור</th><th>מה לקחנו ממנו</th></tr></thead>
<tbody>
<tr><td>{L["org"]}</td><td>המדריך להורים המתחילים, ליווי משפחות, חוזר המנכ"ל</td></tr>
<tr><td>משרד החינוך</td><td>חוזר המנכ"ל וחוברות "שמים לצליאק" לגנים ולבתי הספר</td></tr>
<tr><td><a href="https://www.kolzchut.org.il">כל זכות</a></td><td>זכויות חולי צליאק ומשפחות לילדים עם מחלה כרונית</td></tr>
<tr><td>קופות החולים</td><td>הנחיות תזונה למאובחנים חדשים</td></tr>
<tr><td>כתבות בתקשורת</td><td>סבסוד הקמח ללא גלוטן ודיוני הכנסת</td></tr>
<tr><td>הורים לילדים עם צליאק</td><td>טיפים מעשיים למטבח, לימי הולדת ולאכילה מחוץ לבית</td></tr>
</tbody></table></div>

<h2>פרטיות</h2>
<p>האתר לא מבקש הרשמה, שם, טלפון או כל פרט מזהה, ואין בו טפסים. אין באתר עוגיות, כלי מעקב או סטטיסטיקה. שירות האחסון רושם נתוני חיבור טכניים, כמו כתובת IP, לפי מדיניות הפרטיות שלו. <a href="privacy.html">למדיניות הפרטיות המלאה</a></p>

<h2>חשוב לדעת</h2>
<p>המידע באתר נאסף ממקורות רשמיים, מאתרי העמותות ומניסיון אישי, ונכון לתאריך העדכון. זכויות, מוצרים ורכיבים משתנים מעת לעת, ולכן יש לבדוק כל פרט מול התווית, הרופא או הגוף האחראי לפני שפועלים. המידע אינו ייעוץ רפואי, תזונתי או משפטי, ואינו מחליף פנייה לרופא, לדיאטנית או לגורם מוסמך. האתר אינו קשור לגופים ולעמותות המופיעים בו, ואינו אחראי לשירותים שהם נותנים. השימוש במידע הוא באחריות המשתמש/ת בלבד.</p>
<p>מצאת טעות? עמותה או ארגון שרוצים לעדכן פרטים? יש לך הצעה? נשמח שתכתבו: {mail()}</p>
""")

PAGES["terms.html"] = ("תנאי שימוש", False, f"""
<h1>תנאי שימוש באתר</h1>
<h2>1. כללי</h2>
<p>ברוכים הבאים לאתר {DOMAIN} (להלן: "<b>האתר</b>").</p>
<p>האתר הוא אתר מידע פרטי שנכתב ומופעל בהתנדבות על ידי {AUTHOR} (להלן: "<b>מפעילת האתר</b>", "<b>אנחנו</b>" או "<b>אנו</b>"). מטרתו לרכז מידע שעשוי לסייע להורים לילדים עם צליאק, ולהורים שמארחים ילדים עם צליאק.</p>
<p>תנאים אלה מסדירים את השימוש באתר. נוסף עליהם, מומלץ לעיין גם ב<a href="privacy.html">מדיניות הפרטיות</a> וב<a href="accessibility.html">הצהרת הנגישות</a>.</p>
<p>התנאים מנוסחים בלשון רבים ומיועדים לכלל המגדרים.</p>

<h2>2. מהות המידע באתר</h2>
<p>המידע באתר נועד לסייע בהתמצאות ראשונית והוא מובא למטרות מידע כללי בלבד. הוא אינו מהווה ייעוץ רפואי, תזונתי, משפטי או מקצועי אחר, ואינו תחליף לרופא, לדיאטנית או לייעוץ המותאם לנסיבות האישיות שלכם.</p>
<p>המידע באתר אינו מהווה התחייבות לזכאות לזכות, לתשלום או לשירות כלשהם, ואינו מחליף החלטה של הגוף המוסמך.</p>
<p>רכיבי מוצרים, סימון מזון, זכויות, נהלים ופרטי קשר עשויים להשתנות. דוגמאות למוצרים הן חלקיות בלבד, ויצרנים עשויים לשנות רכיבים ופסי ייצור ללא הודעה. המידע נכון למועד העדכון המצוין באתר. גם כאשר מידע נבדק לפני פרסומו, ייתכן שנפלה בו טעות או שהוא אינו מלא או מעודכן.</p>
<p><b>לפני שמגישים מזון לילד או ילדה עם צליאק, יש לבדוק את התווית על האריזה ולהתייעץ עם ההורים. בכל שאלה רפואית או תזונתית יש לפנות לרופא או לדיאטנית.</b></p>

<h2>3. קישורים לגופים ולאתרים חיצוניים</h2>
<p>האתר כולל קישורים למקורות חיצוניים, לרבות אתרי ממשלה, קופות חולים, עמותות וארגונים. הקישורים נועדו להקל על איתור מידע ושירותים, והכללתם אינה מהווה המלצה, אישור או התחייבות מטעמנו בנוגע לגוף המקושר או לשירותיו.</p>
<p>האתר אינו מייצג גוף ממשלתי, קופת חולים, עמותה או ארגון המופיעים בו, ואינו קשור אליהם, אלא אם צוין אחרת במפורש.</p>
<p>התוכן והשירותים באתרים חיצוניים אינם בשליטתנו, והם עשויים להשתנות ללא ידיעתנו.</p>

<h2>4. שימוש מותר באתר</h2>
<p>ניתן לעיין במידע באתר ולהשתמש בו לצרכים אישיים, וכן לשתף קישור לאתר ולדפים שבו, ובכלל זה לשלוח את הדפים לחוגגים ולמארחים להורים אחרים. אין להשתמש באתר באופן העלול לשבש את פעילותו, לפגוע באבטחתו או בזמינותו, או לנסות להשיג גישה בלתי מורשית למערכותיו. אין באמור כדי למנוע שימוש בטכנולוגיות מסייעות או שימוש אחר המותר לפי דין.</p>

<h2>5. זכויות בתוכן האתר</h2>
<p>התכנים שנוצרו עבור האתר, לרבות אופן הצגתם, ניסוחם ועיצובם, עשויים להיות מוגנים בזכויות קניין רוחני השייכות למפעילת האתר או לגורמים אחרים שהרשו את השימוש בהם.</p>
<p>האתר כולל גם הפניות למקורות חיצוניים ומידע שמקורו בגורמים אחרים, ובהם מדריכים של עמותות. הזכויות בתכנים אלה שייכות לבעליהן, ואנו מפנים אליהם ולא מעתיקים אותם.</p>
<p>אין להעתיק, להפיץ או לעשות שימוש מסחרי בתכנים המוגנים של האתר ללא אישור מראש ובכתב מבעל הזכויות הרלוונטי, למעט שימוש המותר לפי דין. אין באמור כדי להגביל שיתוף קישור לאתר.</p>

<h2>6. זמינות האתר ושינויים</h2>
<p>אנו רשאים לעדכן, לשנות, להוסיף או להסיר מידע באתר, וכן להפסיק את פעילות האתר, כולה או חלקה, מעת לעת.</p>
<p>נשתדל לאפשר גישה לאתר, אך ייתכנו תקלות, הפרעות או הפסקות בפעילותו. איננו מתחייבים שהאתר יהיה זמין בכל עת או שיפעל ללא תקלות.</p>

<h2>7. אחריות</h2>
<p>אנו משקיעים מאמץ סביר באיסוף המידע ובהצגתו, אך איננו מתחייבים שהוא מלא, מדויק, מעודכן או מתאים לנסיבותיו של כל משתמש.</p>
<p>ההחלטה אם וכיצד להסתמך על המידע באתר היא שלכם. עליכם לבדוק את המידע מול התווית, המקור הרשמי או הגורם המטפל, ולפנות לייעוץ מקצועי מתאים לפי הצורך.</p>
<p>יובהר, כי מפעילת האתר לא תישא באחריות לנזק או להפסד הנובעים מהסתמכות על המידע באתר, משימוש באתר או מתוכן ושירותים של גורמים חיצוניים.</p>

<h2>8. עדכון תנאי השימוש</h2>
<p>אנו רשאים לעדכן תנאים אלה מעת לעת. הנוסח המעודכן יפורסם באתר ויישא את תאריך העדכון. שינוי בתנאים אינו גורע מזכויות שהוקנו לפי דין לפני השינוי.</p>

<h2>9. דין חל</h2>
<p>על תנאי שימוש אלה ועל השימוש באתר יחולו דיני מדינת ישראל. סמכות השיפוט תהיה נתונה לבתי המשפט המוסמכים בישראל.</p>

<h2>10. יצירת קשר</h2>
<p>אם מצאתם טעות, מידע שאינו מעודכן או קישור שאינו פועל, או שאתם מייצגים ארגון המעוניין לעדכן פרטים, נשמח לקבל פנייה ונבחן אותה.</p>
<p>ניתן לפנות אלינו בדוא"ל: <b>{mail()}</b>.</p>
<p>תאריך עדכון אחרון: {UPDATED_MONTH}.</p>
""")

PAGES["privacy.html"] = ("מדיניות פרטיות", False, f"""
<h1>מדיניות פרטיות והגנת מידע</h1>
<h2>1. כללי</h2>
<p>אתר האינטרנט {DOMAIN} (להלן: "<b>האתר</b>") הוא אתר מידע פרטי, שנכתב ומופעל בהתנדבות על ידי {AUTHOR} (להלן: "<b>מפעילת האתר</b>", "<b>אנחנו</b>" או "<b>אנו</b>").</p>
<p>האתר נועד לרכז מידע שעשוי לסייע להורים לילדים עם צליאק, ולהורים שמארחים ילדים עם צליאק.</p>
<p>מדיניות זו מסבירה כיצד האתר פועל מבחינת פרטיות, איזה מידע עשוי להישמר אצל ספק האחסון או להימסר לנו בפנייה יזומה, כיצד הוא משמש ומהן זכויותיכם ביחס אליו.</p>

<h2>2. גלישה באתר</h2>
<p>הגלישה באתר אינה מחייבת הרשמה או פתיחת חשבון. האתר אינו כולל טפסים ואינו מבקש מכם להזין שם, מספר טלפון, כתובת דוא"ל, מידע רפואי או פרטים מזהים אחרים.</p>
<p>הבחירה אם לפנות אלינו בדוא"ל ואם למסור פרטים במסגרת הפנייה היא שלכם. ככלל, אינכם חייבים לפי חוק למסור לנו מידע אישי. עם זאת, ללא פרטי קשר או מידע הנחוץ להבנת הפנייה, ייתכן שלא נוכל להשיב לה.</p>

<h2>3. עוגיות, אחסון מקומי וכלי מעקב</h2>
<p>האתר אינו משתמש בעוגיות או באחסון מקומי בדפדפן, ואינו מפעיל כלי סטטיסטיקה, פרסום או מעקב.</p>
<p>השימוש באתר עדיין כרוך בתקשורת עם שירות האחסון ובאפשרות לעיבוד נתוני חיבור טכניים, כמפורט בסעיף הבא. היעדר עוגיות אינו משמעו בהכרח שלא מעובד מידע טכני כלשהו בעת הגלישה.</p>
<p>האתר טוען גופנים משירות Google Fonts. בעת טעינת הגופנים, הדפדפן שלכם פונה לשרתי Google, ו-Google עשויה לקבל נתוני חיבור טכניים כמו כתובת IP, בהתאם למדיניות הפרטיות שלה.</p>

<h2>4. אחסון האתר ונתוני חיבור טכניים</h2>
<p>האתר מתארח באמצעות שירות {HOST}.</p>
<p>בעת הגישה לאתר, הדפדפן שלכם פונה לשרתי שירות האחסון. במסגרת זו, ספק האחסון עשוי לקבל ולעבד נתוני חיבור טכניים, כגון כתובת IP ופרטים על הבקשה שנשלחה לשרת, בין היתר לצורך אספקת השירות, אבטחתו ומניעת שימוש לרעה.</p>
<p>נתונים אלה עשויים להיחשב למידע אישי, בהתאם לנסיבות. עיבודם נעשה בהתאם לתנאי השירות ולמדיניות הפרטיות של ספק האחסון. לפי תצורת האתר, למפעילת האתר אין גישה לרישומי החיבור של המבקרים.</p>

<h2>5. פנייה אלינו בדוא"ל</h2>
<p>ניתן לפנות אלינו בכתובת הדוא"ל {mail()} כדי להציע תיקון למידע באתר, לעדכן פרטים על גוף או שירות, להעלות שאלה או לפנות בנושא פרטיות או נגישות.</p>
<p>אם תבחרו לפנות אלינו, נקבל את כתובת הדוא"ל שממנה נשלחה הפנייה ואת המידע שתבחרו לכלול בה. נשתמש במידע זה לצורך קבלת הפנייה, בדיקתה, מתן מענה וטיפול בנושא שלשמו פניתם.</p>
<p>אין חובה לכלול בפנייה מידע אישי שאינו נחוץ לטיפול בה. בפרט, מומלץ להימנע משליחת מספרי זהות, מסמכים רפואיים, מידע רפואי על ילדים או פרטים אישיים רגישים אחרים, שלכם או של אחרים.</p>
<p>לא נפרסם באתר פנייה, סיפור אישי או פרטים שנמסרו לנו באופן המאפשר לזהות אתכם, ללא הסכמה מתאימה, ככל שנדרשת לפי דין.</p>

<h2>6. מסירת מידע לאחרים</h2>
<p>איננו מוכרים מידע אישי ואיננו מוסרים את תוכן הפניות לגופים המופיעים באתר לצורך פרסום או שיווק.</p>
<p>מידע עשוי להיות נגיש לגורמים המספקים שירותים הנחוצים להפעלת האתר ולטיפול בפניות, כגון ספק שירות הדוא"ל, בהתאם לאופן פעולתו ולתנאיו. כמו כן, מידע עשוי להימסר אם הדבר נדרש לפי דין או צו מחייב.</p>

<h2>7. שמירת מידע ואבטחתו</h2>
<p>פניות ותכתובות יישמרו למשך הזמן הנחוץ לטיפול בפנייה, ולתקופה נוספת ככל שהיא נדרשת לפי דין. תקופת השמירה הרגילה של פניות היא עד 24 חודשים. בתום התקופה נפעל למחיקת המידע שאינו נדרש עוד.</p>
<p>אנו נוקטים אמצעי הגנה סבירים על המידע שבשליטתנו. עם זאת, אין מערכת החסינה לחלוטין מפני תקלה, חדירה או גישה בלתי מורשית.</p>

<h2>8. מידע מחוץ לישראל</h2>
<p>ספק האחסון, Google Fonts וספק שירות הדוא"ל עשויים להפעיל תשתיות מחוץ לישראל. לכן, מידע טכני או מידע שתמסרו בפנייה עשויים להיות מעובדים גם מחוץ לישראל.</p>

<h2>9. קישורים לאתרים חיצוניים</h2>
<p>האתר כולל קישורים לאתרים חיצוניים. כאשר אתם עוברים לאתר חיצוני, הוא עשוי לאסוף ולעבד מידע בהתאם לתנאיו ולמדיניות הפרטיות שלו.</p>

<h2>10. זכויותיכם ביחס למידע</h2>
<p>בכפוף לדין, אתם רשאים לבקש לעיין במידע אישי על אודותיכם המוחזק אצלנו, ולבקש לתקן או למחוק אותו. בקשה למחיקת מידע שמסרתם בפנייה תיבחן בהתאם לדין בתוך 30 ימים.</p>
<p>למימוש זכויות ניתן לפנות אלינו בכתובת <b>{mail()}</b>. ככל שיידרש, נבקש פרטים סבירים לאימות זהותכם.</p>

<h2>11. שינויים במדיניות</h2>
<p>אנו עשויים לעדכן מדיניות זו מעת לעת. הנוסח המעודכן יפורסם באתר ויישא את תאריך העדכון.</p>

<h2>12. יצירת קשר</h2>
<p>לשאלות, לבקשות או לתלונות בנושא פרטיות והגנת מידע: {AUTHOR}, דוא"ל: <b>{mail()}</b></p>
<p>תאריך עדכון אחרון: {UPDATED_MONTH}</p>
""")

PAGES["accessibility.html"] = ("הצהרת נגישות", False, f"""
<h1>הצהרת נגישות</h1>
<p>אתר {DOMAIN} הוא אתר מידע פרטי, המופעל בהתנדבות על ידי {AUTHOR}.</p>
<p>חשוב לנו לאפשר לכל אדם להשתמש באתר ולקבל את המידע המוצג בו באופן שוויוני, מכבד ונגיש, לרבות אנשים עם מוגבלות. אנו פועלים לשיפור נגישות האתר ולהתאמתו לשימוש במכשירים ובאמצעי עזר שונים.</p>

<h2>1. התאמות הנגישות באתר</h2>
<p>האתר נבנה תוך התייחסות לתקן הישראלי 5568 ולהנחיות הנגישות לתוכן באינטרנט WCAG 2.1 ברמה AA. כל דפי האתר נבדקו באמצעות כלי בדיקת נגישות אוטומטי (axe), במצב בהיר ובמצב כהה.</p>
<p>בין התאמות הנגישות באתר:</p>
<ul>
<li><b>התאמה למכשירים שונים:</b> האתר מותאם לצפייה במחשב, בטאבלט ובטלפון נייד.</li>
<li><b>ניווט באמצעות מקלדת:</b> ניתן לנווט באתר באמצעות המקלדת. בעת המעבר בין רכיבים מופיע סימון חזותי של הרכיב שנבחר.</li>
<li><b>דילוג לתוכן המרכזי:</b> בתחילת כל דף קיים קישור המאפשר לדלג ישירות לתוכן המרכזי.</li>
<li><b>ניגודיות צבעים:</b> נעשה שימוש בניגודיות בין הטקסט לרקע כדי להקל על קריאת התוכן. האתר תומך גם במצב כהה של המכשיר.</li>
<li><b>הגדלת תצוגה:</b> ניתן להגדיל את הטקסט והתצוגה באמצעות הדפדפן.</li>
<li><b>תמיכה בקוראי מסך:</b> נעשה שימוש בכותרות מסודרות, בתוויות לתפריטים ולכפתורים, ובסימון שפה וכיוון כתיבה.</li>
<li><b>סימון שאינו נשען על צבע בלבד:</b> הסימונים "אפשר" ו"לא" מופיעים גם במילים, לא רק בצבע.</li>
<li><b>תוכן ללא מגבלת זמן:</b> השימוש באתר אינו מוגבל בזמן, ואין בו תוכן מהבהב או חלונות קופצים.</li>
</ul>

<h2>2. שימוש במקלדת והגדלת התצוגה</h2>
<p>ניתן לעבור בין הקישורים והכפתורים באתר באמצעות מקש <b>Tab</b>, ולחזור לרכיב הקודם באמצעות <b>Shift + Tab</b>. ניתן להפעיל רכיב שנבחר באמצעות מקש <b>Enter</b> או מקש הרווח, בהתאם לסוג הרכיב.</p>
<p>ניתן להגדיל או להקטין את התצוגה באמצעות הדפדפן. במחשב אפשר בדרך כלל להשתמש במקש <b>Ctrl</b> יחד עם <b>+</b> להגדלה או עם <b>-</b> להקטנה. במחשבי Mac משתמשים במקש <b>Command</b> במקום Ctrl.</p>

<h2>3. מגבלות וקישורים חיצוניים</h2>
<p>למרות המאמצים להנגיש את האתר, ייתכן שיתגלו בו רכיבים או תכנים שאינם נגישים באופן מלא. נשמח לקבל דיווח על קושי ולפעול לבדיקתו ולתיקונו.</p>
<p>האתר מפנה גם לאתרים חיצוניים ולקבצי PDF של גופים אחרים. הנגישות שלהם אינה בשליטתנו, וייתכן שחלקם אינם נגישים במלואם.</p>

<h2>4. פניות בנושא נגישות</h2>
<p>נתקלתם בקושי בגלישה, ברכיב שאינו נגיש או במידע שאינכם יכולים לקרוא או להפעיל? ניתן לפנות אלינו כדי לדווח על הבעיה או לבקש התאמת נגישות.</p>
<p><b>אשת קשר לפניות נגישות:</b> {AUTHOR} · <b>דוא"ל:</b> {mail()}</p>
<p>כדי שנוכל לבדוק את הפנייה, מומלץ לציין את הדף או הרכיב שבו נתקלתם בקושי, לתאר את הבעיה ולפרט באיזה דפדפן, מכשיר או טכנולוגיה מסייעת השתמשתם. אין צורך למסור מידע אישי או רפואי שאינו נחוץ לתיאור הקושי.</p>
<p>נבחן את הפנייה ונפעל לטפל בה בהקדם האפשרי, בהתאם לנסיבות ולהוראות הדין.</p>
<p><b>תאריך עדכון ההצהרה:</b> {UPDATED_MONTH}</p>
""")

import importlib.util as _ilu, os as _os
_spec = _ilu.spec_from_file_location("verified", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "verified.py"))
V = _ilu.module_from_spec(_spec); _spec.loader.exec_module(V)
PAGES["diagnosis.html"] = ("קיבלנו אבחנה", False, V.DIAGNOSIS)
PAGES["home.html"] = ("בבית", False, V.HOME)
PAGES["school.html"] = ("גן ובית ספר", False, V.SCHOOL)
PAGES["outside.html"] = ("מחוץ לבית", False, V.OUTSIDE)
PAGES["rights.html"] = ("זכויות", False, V.RIGHTS)
PAGES["birthdays.html"] = ("ימי הולדת", False, V.BIRTHDAYS)
PAGES["snacks.html"] = ("רשימת חטיפים ללא גלוטן", False, V.SNACKS.replace("{UPDATED}", UPDATED).replace("{MAIL}", mail()))

def demote(body, anchor):
    srcs = re.findall(r'<div class="sources">.*?</div>', body, flags=re.S)
    body = re.sub(r'<div class="sources">.*?</div>', '', body, flags=re.S)
    body = body.replace("<h2", "<h3").replace("</h2>", "</h3>")
    body = re.sub(r"<h1>(.*?)</h1>", rf'<h2 id="{anchor}">\1</h2>', body, count=1)
    return body, srcs

def combine(parts, h1, lead, toc):
    out, links = [], []
    for fname, anchor in parts:
        b, srcs = demote(PAGES[fname][2], anchor)
        out.append(b)
        for sblock in srcs:
            links += re.findall(r"<li>.*?</li>", sblock)
    seen, uniq = set(), []
    for l in links:
        if l not in seen: seen.add(l); uniq.append(l)
    tocs = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in toc)
    src = f'<div class="sources"><b>מקורות לעמוד הזה</b><ul>{"".join(uniq)}</ul></div>' if uniq else ""
    return f'<h1>{h1}</h1>\n<p class="lead">{lead}</p>\n<div class="toc"><b>בעמוד הזה</b><ol>{tocs}</ol></div>\n' + "\n".join(out) + src

manage = combine([("home.html", "home"), ("school.html", "school"), ("outside.html", "outside")],
    "איך מתנהלים", "בבית, בגן ובבית הספר, ומחוץ לבית. לימי הולדת יש <a href=\"birthdays.html\">עמוד משלהם</a>.",
    [("home", "בבית: המטבח, הקניות והתוויות"), ("school", "גן ובית ספר"), ("outside", "מחוץ לבית")])
rights = combine([("rights.html", "rights"), ("resources.html", "resources")],
    "זכויות ומקורות", "מה מגיע ומה לא, ואיפה מוצאים עזרה ומידע נוסף.",
    [("rights", "זכויות: מה מגיע ומה לא"), ("resources", "עמותות, קהילה ומקורות")])
for f in ("home.html", "school.html", "outside.html", "resources.html"):
    PAGES.pop(f)
PAGES["manage.html"] = ("איך מתנהלים", False, manage)
PAGES["rights.html"] = ("זכויות ומקורות", False, rights)

LINKS = {'href="home.html#': 'href="manage.html#', 'href="home.html"': 'href="manage.html#home"',
         'href="school.html"': 'href="manage.html#school"', 'href="outside.html"': 'href="manage.html#outside"',
         'href="resources.html"': 'href="rights.html#resources"', 'href="rights.html#flour"': 'href="rights.html#flour"'}
def fixlinks(h):
    for a, b in LINKS.items(): h = h.replace(a, b)
    return h

OUT.mkdir(parents=True, exist_ok=True)
if DOMAIN.startswith("http"):
    (OUT / "CNAME").write_text(re.sub(r"^https?://", "", DOMAIN).strip("/") + "\n", encoding="utf-8")
for fname, (title, wide, body) in PAGES.items():
    (OUT / fname).write_text(fixlinks(page(fname, title, body, wide)), encoding="utf-8")
print("built", len(PAGES), "pages")
