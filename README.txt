celiackids.co.il – מדריך להורים לילדים עם צליאק
================================================
אתר סטטי: HTML ו-CSS בלבד. אין שרת, אין טופס, אין מסד נתונים.
כל הפרטים כבר מולאו: שם, מייל, דומיין (celiackids.co.il). הקובץ CNAME כבר בתיקייה.

שלב 1 – קונים את הדומיין
  celiackids.co.il אצל רשם דומיינים ישראלי. מומלץ להפעיל חידוש אוטומטי.

שלב 2 – מעלים ל-GitHub
  1. יוצרים מאגר חדש (למשל celiackids) ומעלים אליו את כל הקבצים שבתיקייה, כולל CNAME.
  2. Settings ← Pages ← Source: Deploy from a branch ← main ← / (root) ← Save.
  3. Custom domain: אמור להופיע celiackids.co.il (מהקובץ CNAME). אם לא, כותבים ושומרים.

שלב 3 – מחברים את הדומיין (אצל הרשם, בהגדרות DNS)
  * ארבע רשומות A לשורש הדומיין (celiackids.co.il) שמצביעות לכתובות של GitHub Pages.
  * רשומת CNAME ל-www שמצביעה ל: <שם המשתמש שלך ב-GitHub>.github.io
  את הכתובות המדויקות לוקחים מהמדריך הרשמי של GitHub:
  docs.github.com ← Pages ← Configuring a custom domain for your GitHub Pages site
  (בדיוק כמו שהוגדר ל-almanim.co.il – אפשר להעתיק משם את אותן רשומות.)

שלב 4 – אחרי שהדומיין עובד (יכול לקחת עד יום)
  ב-Settings ← Pages מסמנים Enforce HTTPS.
  בודקים: שולחים לעצמך בוואטסאפ את celiackids.co.il/hosts.html ורואים את התצוגה המקדימה.

עדכונים בעתיד
  עורכים את build.py ומריצים:  python3 build.py .
  ואז מעלים את הקבצים שהשתנו ל-GitHub.
