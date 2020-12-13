from xlrd import open_workbook
import xlsxwriter

ADVANCED_GIVAT_RAM_NEW_DEPARTMENT = 111  # a number to put givat ram's masters under, should be different
# then all other departments numbers

# all degrees by order
Degrees = [None, 'בוגר', 'תעודה', 'השלמה למוסמך', 'מוסמך', 'ד"ר לפילוסופיה', 'ד"ר לרפואה',
           'ד"ר לרפואת שיניים', 'מכינה', 'לא לתואר', 'ד"ר לוטרינריה', 'ד"ר רוקחות קלינית', 'השלמה למחקר']
degs_not_advanced = [1, 2, 9]  # not advanced degrees (by index)

# all faculties by order
Faculties = [None, 'רוח', 'טבע', 'משפטים', 'רפואה', 'רפואת שיניים', 'מנהל עסקים', 'חברה', 'חקלאות', 'עו"ס',
             None, 'מדעי המוח', 'הנדסה ומדעי המחשב', 'רוקחות', 'ריפוי בעיסוק', 'סיעוד', 'מכינה',
             'תלמידי חו"ל', 'מדעי הרפואה']

# all departments by index and name
Departments = {860: 'מכינה מסלול מדעי הטבע והחיים מוגבר',
               820: 'מכינה מסלול מדעי הטבע והחיים',
               830: 'מכינה מסלול מדעים מדוייקים והנדסה',
               835: 'קדם מכינה לעתידים',
               840: 'מכינה מסלול מדעי הרוח והחברה מוגבר',
               855: 'קדם מכינה חסרי בגרות',
               870: 'מכינה מסלול מדעי הרוח והחברה',
               900: 'לימודי עברית - חיצוניים',
               926: 'מכינה - טבע',
               105: 'היסטוריה של עם ישראל ויהדות זמננו',
               151: 'היסטוריה כללית',
               127: 'חבצלות',
               142: 'הסטוריה פילוסופיה וסוציולוגיה של המדעים',
               122: 'איסלאם מזרח תיכון',
               123: 'שפה וספרות ערבית',
               225: 'תכנית רב תחומית',
               102: 'תלמוד והלכה',
               113: 'מחשבת ישראל',
               101: 'מקרא',
               115: 'יהדות  ',
               117: 'פולקלור יהודי והשוואתי',
               202: 'תוכנית רביבים',
               150: ' ארכיאולוגיה והמזרח הקרוב הקדום',
               108: 'ספרות עברית',
               109: 'לשון עברית',
               112: 'יידיש',
               180: 'ספרות כללית והשוואתית (180)',
               181: 'בלשנות',
               176: 'אנגלית',
               157: 'שפה וספרות גרמנית',
               197: 'תולדות האומנות',
               198: 'תאטרון',
               199: 'מוסיקולוגיה',
               140: 'פילוסופיה',
               141: 'מדע הדתות',
               222: 'ב.א כללי',
               255: 'תכנית "אמירים" למצטיינים',
               143: 'מדעי הקוגניציה',
               144: 'תכנית אישית בלימודים קוגנטיביים',
               155: 'אמל"ט',
               156: 'לימודים סלאביים',
               160: 'תרבויות מרכז אירופה ומזרחה',
               172: 'לימודים קלאסיים',
               179: 'לימודים רומאניים ולטינו אמריקניים',
               124: 'לימודי מזרח אסיה',
               200: 'חינוך',
               207: 'תכנית מעל"ה',
               249: 'תכנית אישית במגמת הוראה',
               230: 'לימודים משולבים במדעי החינוך',
               231: 'חינוך- מחשבת החינוך',
               237: 'המגמה למנהל, מדיניות ומנהיגות בחינוך',
               238: 'המגמה לחינוך יהודי',
               239: 'חינוך- פסיכולוגיה חינוכית וקלינית של הילד',
               240: 'חינוך – ייעוץ חינוכי',
               241: 'חינוך- חינוך מיוחד',
               242: 'חינוך- למידה והוראה',
               243: 'לקויות למידה',
               246: 'ייעוץ חינוכי לגיל הרך',
               298: 'תכנית אישית למוסמך',
               299: 'תכנית מיוחדת במדעי הרוח',
               201: 'לימודי הוראה תעודת הוראה',
               431: 'עו"ס',
               432: 'עבודה סוציאלית-השלמה למוסמך לבוגרי תחומים אחרים',
               433: 'נהול מלכ"רים וארגונים קהלתיים',
               434: 'לימודי מוסמך בגיל הרך',
               430: 'עבודה סוציאלית - תוכנית משותפת',
               300: 'פסיכולוגיה ',
               301: 'סוציולוגיה ואנתרופולוגיה',
               802: 'גאוגרפיה',
               369: 'לימודי תרבות-תכנית אישית',
               810: 'גיאוגרפיה ותכנון עירוני',
               821: 'גיאוגרפיה סביבה  וגאואינפורמטיקה',
               809: 'בי"ס האוניברסיטאי ללימודי הסביבה',
               815: 'ניהול ומדיניות משאבי טבע וסביבה',
               365: 'מגדר',
               323: 'תקשורת ועיתונאות',
               525: 'אינטרנט וחברה',
               816: 'מוסמך במגדר ומגוון',
               311: 'מדעי המדינה',
               312: 'יחסים בין לאומיים',
               364: 'לימודים גרמניים',
               363: 'תוכנית בלימודי אירופה',
               358: 'לימודי פיתוח קהילות',
               350: 'חקר-סכסוכים,ניהולם ויישובם',
               326: 'תכנית משולבת: פילוסופיה,כלכלה,מדע המדינה',
               335: 'מדיניות ציבורית',
               330: 'צוערים לשירות המדינה',
               321: 'כלכלה ',
               343: 'כלכלה ומינהל עסקים',
               399: 'תוכנית מיוחדת - קורסים כלכליים',
               337: 'כלכלה: תכנית משותפת עם אונ. ת"א',
               320: 'סטטיסטיקה',
               824: 'מדע הנתונים',
               366: 'תכנית משולבת בכלכלה ובמדיניות ציבורית',
               322: 'מנהל עסקים',
               379: 'תכנית מיוחדת במינהל עסקים',
               325: 'חשבונאות',
               370: 'השתלמות לבוגרי חשבונאות',
               347: 'מנהל עסקים ומוסיקולוגיה',
               331: 'מנהל עסקים ותולדות האומנות',
               352: 'מנהל עסקים ולימודי התאטרון',
               380: 'התמחות בחקר ביצועים',
               386: 'מנהל עסקים ולימודי אסיה',
               819: 'מנהל עסקים בהתמחות מורחבת בניהול, חדשנות ויזמות רפואית',
               401: 'משפטים',
               402: 'משפטים – תכנית משותפת',
               404: 'משפטים - תכנית מיוחדת',
               414: 'מכפיל במשפטים',
               409: 'קרימינולוגיה - התמחות במדע פורנזי (משפטים)',
               417: 'תכנית מנהלים למוסמך במשפטים',
               411: 'קרימינולוגיה',
               415: 'קרימינולוגיה לכוחות הביטחון',
               410: 'קרימינולוגיה בהתמחות באכיפת החוק',
               880: '',
               511: 'תארים מתקדמים - ',
               899: 'מדעי המחשב תוכנית מיוחדת',
               521: 'מדעי המחשב',
               523: 'אמירים - מחשבים',
               586: 'הנדסת תוכנה',
               587: 'הנדסת מחשבים - התמחות בפיסיקה',
               890: 'ביוטכנולוגיה',
               583: 'הנדסת חשמל ומחשבים',
               581: 'הנדסת חשמל ופיזיקה יישומית',
               530: 'מתמטיקה',
               541: 'פיזיקה',
               555: '"אמירים"',
               560: 'כימיה',
               545: 'מדעי האטמוספירה',
               591: 'תוכנית לימודי הסביבה',
               595: 'מדעי כדור הארץ',
               599: 'תוכנית מיוחדת במדעי הטבע',
               589: 'הידרולוגיה ומשאבי מים',
               590: 'גיאולוגיה',
               592: 'אוקיינוגרפיה',
               596: 'ניהול טכנולוגיה',
               318: 'צירוף פסיכולוגיה וביולוגיה',
               588: 'התמחות בגנומיקה וביואינפורמטיקה',
               580: 'מדעי החיים בדגש בביו פיסיקה',
               532: 'מדעי המחשב וביולוגיה חישובית',
               570: 'ביולוגיה',
               569: 'תוכנית משולבת מדעים מדוייקים',
               566: 'מדעי הכימיה והבילוגיה',
               579: 'אבולוציה ואקולוגיה ',
               575: 'גנטיקה',
               577: 'ביוכימיה מבנית ומולקולארית',
               573: 'ביולוגיה תאית והתפתחותית',
               576: 'מדעי המוח וההתנהגות',
               582: 'ביו-הנדסה- מסלול ישיר לדוקטורט',
               681: 'רפואה - המסלול הצבאי - צמרת',
               601: 'רפואה',
               699: 'רפואה - לימודים כלליים',
               611: 'רפואת שיניים',
               617: 'מדעים ביו-רפואיים ברפו"ש',
               602: 'מדעי הרפואה הבסיסיים',
               603: 'תלמידי בריאות הציבור',
               616: 'בריאות הציבור ורפואה קהילתית בינ"ל',
               630: 'מדעי הרפואה - סיעוד קליני',
               698: 'אפידמיולוגיה',
               606: 'סיעוד- "הדסה"',
               608: 'סיעוד- "אסף הרופא"',
               610: 'סיעוד שלוחת "קפלן"',
               618: 'ניהול מערכות בריאות',
               619: 'סיעוד לחובשים קפלן',
               607: 'ריפוי בעיסוק',
               627: 'ריפוי בעיסוק- לימודים מתקדמים',
               621: 'רוקחות',
               624: 'מדעי התרופה - תכנית מצוינות',
               626: 'מסלול מצויינות לתואר דוקטור ברוקחות קלינית',
               625: 'רוקחות קלינית',
               628: 'רפואה ומחקר ביו-רפואי',
               640: 'תוכנית הסבה לרוקחות',
               710: 'מדעי הצומח בחקלאות',
               713: 'גידולי שדה וירקות',
               714: 'מטעים וצמחי נוי',
               715: 'הגנת הצומח',
               716: 'מדעי הקרקע והמים',
               721: 'גנטיקה והשבחה',
               724: 'מדעי הצמח בחקלאות- מוסמך',
               728: 'איכות הסביבה ומשאבי טבע בחקלאות',
               755: 'אמירים- תכנית מצטיינים בחקלאות',
               791: 'התמחות בביוטכנולוגיה, מדעי הצמח, הגנת הצומח, ביוכימיה בעלי חיים',
               792: 'הגנת הצומח וביוטכנולוגיה בחקלאות',
               731: 'גידולי שדה וירקות - תכנית בינלאומית',
               717: 'כלכלה חקלאית',
               729: 'ניהול משאבי אנוש מגמת מלונאות',
               795: 'כלכלה, מינהל ביוטכנולוגיה בחקלאות',
               712: 'מדעי התזונה',
               722: 'מדעי המזון והתזונה',
               723: 'ביוכימיה מדעי המזון והתזונה',
               718: 'מדעי בעלי חיים',
               730: 'רפואה וטרינרית',
               734: 'מדעי בעלי חיים- תכנית בינלאומית',
               735: 'וטרינריה',
               736: 'בריאות ציבור וטרינרית',
               794: 'בעלי חיים וביוטכנולוגיה בחקלאות',
               793: 'ביוכימיה ומדעי המזון וביוטכנולוגיה בחקלאות',
               991: 'האקדמיה למוזיקה',
               992: 'האקדמיה למוזיקה (מוסמך)',
               0: 'Unknown',
               ADVANCED_GIVAT_RAM_NEW_DEPARTMENT: 'תארים מתקדמים גבעת רם כללי'
               }
# departments in givat ram
givat_ram_deps = [899, 521, 523, 586, 587, 890, 583, 581, 530, 541, 569, 555, 560, 545, 591, 595,
                  599, 589, 590, 592, 596, 318, 588, 580, 532, 570, 566, 579, 575, 577, 573, 576,
                  582, 572, 597, 511, 880]
givat_ram_advanced = [511, 880, 582]  # advanced degrees departments in givat ram

departments_with_studs = dict()


def add_stud_dept(deg, dept, num):
    """
    Adds a student to the department.
     Checks if the student is in advanced degrees in givat ram or not (if s/he is, adds to advanced degrees
     as should be in givat ram).
    Adds the number specified in num.
    """
    if dept in givat_ram_deps and deg not in degs_not_advanced:
        if dept not in givat_ram_advanced:  # this is already advanced and need not be moved to the new dept
            dept = ADVANCED_GIVAT_RAM_NEW_DEPARTMENT
    try:
        departments_with_studs[dept] += num
    except KeyError:  # should not happen as it is zeroed at first, but remained for future changes
        departments_with_studs[dept] = num


def deal_with_row(fac, deg, dept1, dept2, dept3):
    """
    If the students has two departments, it will count as half to each one of them. If it has only one,
    it will count as full one to it.
    Unused parameters are for if they will be wanted in the future.
    """
    if dept2 == 0:
        add_stud_dept(deg, dept1, 1)
    else:
        add_stud_dept(deg, dept1, 0.5)
        add_stud_dept(deg, dept2, 0.5)


def read_xls_file():
    wb = open_workbook('aguda2021.xls')  # file should be in same directory and have this exact name
    # columns should be in this order, with header column: faculty, degree, department, department
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

        for row in range(1, number_of_rows):
            values = []
            for col in range(number_of_columns):
                value = sheet.cell(row, col).value
                try:
                    value = int(value)
                except ValueError:
                    value = 0
                finally:
                    values.append(value)
            deal_with_row(values[0], values[1], values[2], values[3], values[4])


def write_results():
    workbook = xlsxwriter.Workbook('Elections.xlsx')
    worksheet = workbook.add_worksheet("Results")

    worksheet.write(0, 0, 'חוג')
    worksheet.write(0, 1, 'סמל חוג')
    worksheet.write(0, 2, 'מספר סטודנטים')

    row = 1
    col = 0

    for elem in departments_with_studs:
        worksheet.write(row, col, Departments[elem])  # department
        worksheet.write(row, col + 1, elem)  # department num
        worksheet.write(row, col + 2, departments_with_studs[elem])  # num of studs
        row += 1
    workbook.close()


if __name__ == '__main__':
    for i in Departments:
        departments_with_studs[i] = 0
    read_xls_file()
    write_results()
