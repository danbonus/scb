# nomn = именительный (кто, что?)
# gent = родительный (нет кого, чего?)
# datv = дательный (дать кому, чему?)
# accs = винительный (вижу кого, что?)
# ablt = творительный (доволен кем, чем?)
# loct = предложный (думаю о чём, ком?)


class Subject:
    label: str

    nomn: str
    gent: str
    datv: str
    accs: str
    ablt: str
    loct: str

    shorts: str

    emoji: str

    lang_group: int = 0
    exam_group: int = 0

'''
class GroupSubject(Subject):
    teacher_name: str
    group: int'''

''' 
class ElectiveSubject(Subject):
    elective: bool'''

# математические:
#   матеша, алгебра,
#   геометрия, инфа


class Math(Subject):
    label = "math"

    nomn = "Математика"
    gent = "математики"
    datv = "математике"
    accs = "математику"
    ablt = "математикой"
    loct = "математике"

    shorts = [
        "математика", "мат", "матеша",
        "матан", "math", "mat"
    ]
    emoji = "📝"


class Algebra(Subject):
    label = "algebra"

    nomn = "Алгебра"
    gent = "алгебры"
    datv = "алгебре"
    accs = "алгебру"
    ablt = "алгеброй"
    loct = "алгебре"

    shorts = [
        "алгебра", "алг", "алгеб",
        "algebra", "alg", "algeb"
    ]
    emoji = "📝"


class Geometry(Subject):
    label = "geometry"

    nomn = "Геометрия"
    gent = "геометрии"
    datv = "геометрии"
    accs = "геометрию"
    ablt = "геометрией"
    loct = "геометрии"

    shorts = [
        "геометрия", "геом", "геометр",
        "geometry", "geom", "geometr"
    ]
    emoji = "📐"


class GeometryEl(Geometry, Subject):
    label = "geometry-el"

    nomn = "Планиметрия (эл.)"
    gent = "геометрии (эл.)"
    datv = "геометрии (эл.)"
    accs = "геометрию (эл.)"
    ablt = "геометрией (эл.)"
    loct = "геометрии (эл.)"

    shorts = [
        "геометрия эл", "геом эл", "геометр эл",
        "geometry el", "geom el", "geometr el"
    ]


class IT(Subject):
    label = "compsci"

    nomn = "Информатика"
    gent = "информатики"
    datv = "информатике"
    accs = "информатику"
    ablt = "информатикой"
    loct = "информатике"

    shorts = [
        "Информатика", "инф", "инфа",
        "инфо", "info", "infa", "it"
    ]
    emoji = "🖥"


class IT_PD(IT, Subject):
    label = "compsci1"

    name = " П. Д"

    shorts = [
        "Информатика 1", "инф 1", "инфа 1",
        "инфо 1", "info 1", "infa 1", "it 1"
    ]

    lang_group = 1


class IT_ON(IT, Subject):
    label = "compsci2"

    name = " О. Н"

    shorts = [
        "Информатика 2", "инф 2", "инфа 2",
        "инфо 2", "info 2", "infa 2", "it 2"
    ]
    lang_group = 2

####################


# общественно-научные:
#   история, экономика
class History(Subject):
    label = "history"

    nomn = "История"
    gent = "истории"
    datv = "истории"
    accs = "историю"
    ablt = "историей"
    loct = "истории"

    shorts = [
        "история", "ист", "истор",
        "history", "hist", "histor",
        "istoria", "ist", "istor"
    ]
    emoji = "🏛"


class Economy(Subject):
    label = "economy"

    nomn = "Экономика"
    gent = "экономики"
    datv = "экономике"
    accs = "экономику"
    ablt = "экономикой"
    loct = "экономике"

    shorts = [
        "экономика", "экон", "эконом",
        "economy", "econ", "econom"
        # почему нет эко? эко ассоциируется с экологией потому что
    ]
    emoji = "💰"


####################


# eстественно-научные:
#   окружающий мир, география,
#   биология, физика, химия,
#   ОБЖ, астрономия
class SurroundingWorld(Subject):
    label = "surrworld"

    nomn = "Окружающий мир"
    gent = "окружающего мира"
    datv = "окружающему миру"
    accs = "окружающий мир"
    ablt = "окружающим миром"
    loct = "окружающем мире"

    shorts = [
        "окружающий мир", "окр мир", "окр",
        "мир", "okrmir", "okr", "mir",
        "surrworld", "surr", "world"
    ]

    emoji = "🌱"


class Geography(Subject):
    label = "geography"

    nomn = "География"
    gent = "географии"
    datv = "географии"
    accs = "географию"
    ablt = "географией"
    loct = "географии"

    shorts = [
        "география", "гео", "геог",
        "географ", "geography", "geo",
        "geog", "geograf", "geograph", "геогр"
        # и не пизди, что гео может быть не только географией, но и геометрией
        # гео с греческого означает земля, а не геометрия бляха :|
    ]
    emoji = "🌍"


class Biology(Subject):
    label = "biology"

    nomn = "Биология"
    gent = "биологии"
    datv = "биологии"
    accs = "биологию"
    ablt = "биологией"
    loct = "биологии"

    shorts = [
        "биология", "био", "биолог",
        "беу", "беулогия", "biology",
        "bio", "beu", "beulogia",
        "biologia", "biolog"
    ]
    emoji = "🧬"


class BiologyEl(Biology, Subject):
    label = "biology-el"

    nomn = "Биология (эл.)"
    gent = "биологии (эл.)"
    datv = "биологии (эл.)"
    accs = "биологию (эл.)"
    ablt = "биологией (эл.)"
    loct = "биологии (эл.)"

    shorts = [
        "биология", "био", "биолог",
        "беу", "беулогия", "biology",
        "bio", "beu", "beulogia",
        "biologia", "biolog"
    ]


class BiologyEGE(BiologyEl, Subject):
    label = "biology-el1"
    name = " ЕГЭ"
    # nomn = Biology.nomn + teacher_name
    exam_group = 1


class BiologyNonEGE(BiologyEl, Subject):
    label = "biology-el2"
    name = " неЕГЭ"
    # nomn = Biology.nomn + teacher_name
    exam_group = 2


class Physics(Subject):
    label = "physics"

    nomn = "Физика"
    gent = "физики"
    datv = "фиизке"
    accs = "физику"
    ablt = "физикой"
    loct = "физике"

    shorts = [
        "физика", "физик", "physics",
        "physic", "phys"
        # "физ" конфликтует с физрой, поэтому не юзаем ни там, ни здесь 🤪
    ]
    emoji = "⚛️"


class Chemistry(Subject):
    label = "chemistry"

    nomn = "Химия"
    gent = "химии"
    datv = "химии"
    accs = "химию"
    ablt = "химией"
    loct = "химии"

    shorts = [
        "химия", "хим",
        "chemistry", "chem"
    ]
    emoji = "🧪"


class ChemistryEl(Chemistry, Subject):
    label = "chemistry-el"

    nomn = "Химия (эл.)"
    gent = "химии (эл.)"
    datv = "химии (эл.)"
    accs = "химию (эл.)"
    ablt = "химией (эл.)"
    loct = "химии (эл.)"


class ChemistryEGE(ChemistryEl, Subject):
    label = "chemistry-el1"
    name = " (ЕГЭ)"
    exam_group = 1


class ChemistryNonEGE(ChemistryEl, Subject):
    label = "chemistry-el2"
    name = " (неЕГЭ)"
    exam_group = 2


class LifeSafetyFundamentals(Subject):
    label = "lifesafetyfundamentals"

    nomn = "ОБЖ"
    gent = "ОБЖ"
    datv = "ОБЖ"
    accs = "ОБЖ"
    ablt = "ОБЖ"
    loct = "ОБЖ"

    shorts = [
        "обж", "безопасность",
        "жизнь", "жизнедеятельность",
        "safe", "safety", "life", "lsf",
        "obzh"
    ]
    emoji = "🧯"


class Astronomy(Subject):
    label = "astronomy"

    nomn = "Астрономия"
    gent = "астрономии"
    datv = "астрономии"
    accs = "астрономию"
    ablt = "астрономией"
    loct = "астрономии"

    shorts = [
        "астрономия", "астро",
        "астроном", "astronomy",
        "astro", "astronom"
    ]
    emoji = "🌠"


####################


# гуманитарные:
#   обществознание, право,
#   этика
class SocialStudies(Subject):
    label = "socialstudies"

    nomn = "Обществознание"
    gent = "обществознания"
    datv = "обществознанию"
    accs = "обществознание"
    ablt = "обществознанием"
    loct = "обществознании"

    shorts = [
        "обществознание", "общество",
        "общага", "общ", "social studies",
        "social", "soc"
    ]
    emoji = "⚖"


class Law(Subject):
    label = "law"

    nomn = "Право"
    gent = "права"
    datv = "праву"
    accs = "право"
    ablt = "правом"
    loct = "праве"

    shorts = [
        "право", "прав", "права",
        "law", "laws", "right",
        "rights"
    ]
    emoji = "⚖"


'''class Ethics(Subject):
    label = "ethics"

    nomn = "Этика"
    gent = "этики"
    datv = "этике"
    accs = "этику"
    ablt = "этикой"
    loct = "этике"

    shorts = [
        "этика", "этик", "ethics",
        "eth", "ethic"
    ]
    emoji = "👋"'''


####################


# трудовое обучение:
#   труд, технология,
#   черчение
'''class Work(Subject):
    label = "work"

    nomn = "Труд"
    gent = "труда"
    datv = "труду"
    accs = "труд"
    ablt = "трудом"
    loct = "труде"

    shorts = [
        "труд", "work"
    ]
    emoji = "✂"
'''
'''
class Technology(Subject):
    label = "technology"

    nomn = "Технология"
    gent = "технологии"
    datv = "технологии"
    accs = "технологию"
    ablt = "технологией"
    loct = "технологии"

    shorts = [
        "технология", "техно", "технолог",
        "technology", "techo", "technolog"
    ]
    emoji = "🛠"'''


'''class MechanicalDrawing(Subject):
    label = "mechanicaldrawing"

    nomn = "Черчение"
    gent = "черчения"
    datv = "черчению"
    accs = "черчение"
    ablt = "черчением"
    loct = "черчении"

    shorts = [
        "черчение", "чер", "черч",
        "mechanical draw", "mech draw"
    ]
    emoji = "✏"'''


####################


# физра
class PE(Subject):
    label = "pe"

    nomn = "Физкультура"
    gent = "физкультуры"
    datv = "физкультуре"
    accs = "физкультуру"
    ablt = "физкультурой"
    loct = "физкультуре"

    shorts = [
        "физкультура", "физра", "physical edu",
        "physical education", "pe", "физ-ра"
    ]
    emoji = "⚽"


####################


# искусство:
#   ИЗО, музыка, МХК
class Music(Subject):
    label = "music"

    nomn = "Музыка"
    gent = "музыки"
    datv = "музыке"
    accs = "музыку"
    ablt = "музыкой"
    loct = "музыке"

    shorts = [
        "музыка", "муз", "музон",
        "music", "mus"
    ]
    emoji = "🎻"


class Art(Subject):
    label = "art"

    nomn = "ИЗО"
    gent = "ИЗО"
    datv = "ИЗО"
    accs = "ИЗО"
    ablt = "ИЗО"
    loct = "ИЗО"

    shorts = [
        "изо", "art"
    ]
    emoji = "🎨"


class WorldArt(Subject):
    label = "worldart"

    nomn = "МХК"
    gent = "МХК"
    datv = "МХК"
    accs = "МХК"
    ablt = "МХК"
    loct = "МХК"

    shorts = [
        "мхк", "худ культура", "мир культура",
        "худ культ", "мир культ", "world art",
        "w art", "mhk"
    ]
    emoji = "🖼"


####################


# иностранные языки:
#   английский, французский,
#   немецкий, испанский
class English(Subject):
    label = "english"

    nomn = "Английский"
    gent = "английского"
    datv = "английскому"
    accs = "английский"
    ablt = "английским"
    loct = "английском"

    shorts = [
        "английский", "англ", "анг",
        "ен", "енг", "англия"
                     "english", "eng", "en",
        "angl", "ang", "gb"
    ]
    emoji = "🇬🇧"


class EnglishPD(English, Subject):
    label = "english1"
    name = " П. Д"
    lang_group = 1


class EnglishON(English, Subject):
    label = "english2"
    name = " О. Н"
    lang_group = 2


'''class French(Subject):
    label = "french"

    nomn = "Французский"
    gent = "французского"
    datv = "французскому"
    accs = "французский"
    ablt = "французским"
    loct = "французском"

    shorts = [
        "французский", "фран",
        "франц", "француз", "фр",
        "френч", "франция", "франс",
        "french", "fr", "france",
        "fran"
    ]
    emoji = "🇫🇷"'''


'''class Deutsch(Subject):
    label = "deutsch"

    nomn = "Немецкий"
    gent = "немецкого"
    datv = "немецкому"
    accs = "немецкий"
    ablt = "немецким"
    loct = "немецком"

    shorts = [
        "немецкий", "немец", "нем",
        "деу", "deutsch", "deu",
        "german", "germany",
        "ger", "nem", "de"
    ]
    emoji = "🇩🇪"'''


'''class Spanish(Subject):
    label = "spanish"

    nomn = "Испанский"
    gent = "испанского"
    datv = "испанскому"
    accs = "испанский"
    ablt = "испанским"
    loct = "испанском"

    shorts = [
        "испанский", "исп", "испан",
        "есп", "спан", "spanish",
        "esp", "es" "espanol", "espan",
        "span"
    ]
    emoji = "🇪🇸"'''


####################


# филологические:
#   русский, украинский,
#   белорусский, казахский,
#   литература
class Russian(Subject):
    label = "russian"

    nomn = "Русский"
    gent = "русского"
    datv = "русскому"
    accs = "русский"
    ablt = "русским"
    loct = "русском"

    shorts = [
        "русский", "рус", "руск",
        "русск", "russian", "rus",
        "ru"
    ]
    emoji = "🇷🇺"


'''class Ukrainian(Subject):
    label = "ukrainian"

    nomn = "Украинский"
    gent = "украинского"
    datv = "украинскому"
    accs = "украинский"
    ablt = "украинским"
    loct = "украинском"

    shorts = [
        "украинский", "укр", "украин",
        "ukrainian", "ukr", "ua"
    ]
    emoji = "🇺🇦"'''


'''class Belarusian(Subject):
    label = "belarusian"

    nomn = "Белорусский"
    gent = "белорусского"
    datv = "белорусскому"
    accs = "белорусский"
    ablt = "белорусским"
    loct = "белорусском"

    shorts = [
        "белорусский", "бел", "белор",
        "belarusian", "bel", "belar"
                             "belarus", "by"
    ]
    emoji = "🇧🇾"'''


'''class Kazakh(Subject):
    label = "kazakh"

    nomn = "Казахский"
    gent = "казахского"
    datv = "казахскому"
    accs = "казахский"
    ablt = "казахским"
    loct = "казахском"

    shorts = [
        "казахский", "каз", "казах",
        "kazakh", "kazah", "qazaq",
        "kaz", "kazah", "kz"
    ]
    emoji = "🇰🇿"'''


class Literature(Subject):
    label = "literature"

    nomn = "Литература"
    gent = "литературы"
    datv = "литературе"
    accs = "литературу"
    ablt = "литературой"
    loct = "литературе"

    shorts = [
        "литература", "лит", "литра",
        "literature", "lit", "litra",
        "liter"
    ]
    emoji = "📖"


####################


# говно какое то
class IndividualProject(Subject):
    label = "individualproject"

    nomn = "Индивидуальный проект"
    gent = "индивидуального проекта"
    datv = "индивидуальному проекту"
    accs = "индивидуальный проект"
    ablt = "индивидуальным проектом"
    loct = "индивидуальном проекте"

    shorts = [
        "индивидуальный проект", "инд", "индивид",
        "проект", "individual project", "ind",
        "individ", "proj", "project", "ип"
    ]
    emoji = "👨‍🏫"



class Talks(Subject):
    label = "talks"

    nomn = "Классный час"
    gent = "классного часа"
    datv = "классному часу"
    accs = "классный час"
    ablt = "классным часом"
    loct = "о классном часе"

    shorts = ["клч", "классный час"]

    emoji = "[?]"


####################


class DefaultSubjects:
    default = [i for i in Subject.__subclasses__()]
    #print(default)