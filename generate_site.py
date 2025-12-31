import os
import shutil
import sys

# Data Definitions

# 1. Services (Electrical and Low-current systems)
services = [
    "Монтаж электропроводки",
    "Установка розеток и выключателей",
    "Сборка электрощитов",
    "Монтаж освещения",
    "Монтаж слаботочных систем",
    "Установка видеонаблюдения",
    "Монтаж пожарной сигнализации",
    "Установка домофонов",
    "Монтаж СКУД (Системы контроля доступа)",
    "Прокладка интернет-кабеля (ЛВС)",
    "Монтаж системы 'Умный дом'",
    "Заземление и молниезащита",
    "Электромонтаж под ключ",
    "Ремонт электрики",
    "Подключение бытовой техники",
    "Монтаж теплых полов",
    "Установка стабилизаторов напряжения",
    "Монтаж охранной сигнализации",
    "Телефония и АТС",
    "Спутниковое и эфирное телевидение"
]

# 2. Geography: Regions and Cities
# Mapping Region -> List of Cities
geography = {
    "Московская область": ["Москва", "Балашиха", "Подольск", "Химки", "Мытищи"],
    "Ленинградская область": ["Санкт-Петербург", "Гатчина", "Выборг", "Всеволожск", "Мурино"],
    "Свердловская область": ["Екатеринбург", "Нижний Тагил", "Каменск-Уральский", "Первоуральск"],
    "Новосибирская область": ["Новосибирск", "Бердск", "Искитим"],
    "Краснодарский край": ["Краснодар", "Сочи", "Новороссийск", "Армавир"],
    "Республика Татарстан": ["Казань", "Набережные Челны", "Нижнекамск", "Альметьевск"],
    "Нижегородская область": ["Нижний Новгород", "Дзержинск", "Арзамас"],
    "Самарская область": ["Самара", "Тольятти", "Сызрань"],
    "Ростовская область": ["Ростов-на-Дону", "Таганрог", "Шахты"],
    "Челябинская область": ["Челябинск", "Магнитогорск", "Златоуст"]
}

# 3. Industries
industries = [
    "Офисы и Бизнес-центры",
    "Торговые центры и Магазины",
    "Складские комплексы",
    "Промышленные предприятия",
    "Рестораны и Кафе",
    "Гостиницы и Отели",
    "Медицинские учреждения",
    "Образовательные учреждения",
    "Частные дома и Коттеджи",
    "Квартиры и Новостройки"
]

# Output directory
OUTPUT_DIR = "site"

# Flag to limit generation for environment safety
# Default is False (generate full site ~1200 pages)
# Can be overridden by env var DEMO_LIMIT=1
DEMO_LIMIT = os.environ.get("DEMO_LIMIT", "0") == "1"

# Slugify helper (very basic)
def slugify(text):
    translit = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        ' ': '-', '.': '', ',': ''
    }
    result = []
    for char in text.lower():
        if char in translit:
            result.append(translit[char])
        elif char.isalnum() or char == '-':
            result.append(char)
        else:
            continue
    return "".join(result)

# HTML Templates

def get_header(title, depth=0):
    path_prefix = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - ЭлектроМонтажПро</title>
    <link rel="stylesheet" href="{path_prefix}style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="{path_prefix}index.html">ЭлектроМонтажПро</a></h1>
            <nav>
                <ul>
                    <li><a href="{path_prefix}geo/index.html">По городам</a></li>
                    <li><a href="{path_prefix}industry/index.html">По отраслям</a></li>
                </ul>
            </nav>
        </div>
    </header>
    <main class="container">
"""

def get_footer():
    return """
    </main>
    <footer>
        <div class="container">
            <p>&copy; 2023 ЭлектроМонтажПро. Все права защищены.</p>
        </div>
    </footer>
</body>
</html>
"""

def generate_index():
    content = get_header("Главная")
    content += """
        <div class="hero">
            <h2>Профессиональный монтаж электрических и слаботочных систем</h2>
            <p>Мы работаем по всей России и во всех отраслях.</p>
        </div>
        <div class="grid-2">
            <div class="card">
                <h3>Услуги в вашем городе</h3>
                <p>Найдите мастера в своем регионе.</p>
                <a href="geo/index.html" class="btn">Выбрать город</a>
            </div>
            <div class="card">
                <h3>Решения для бизнеса</h3>
                <p>Специализированные услуги для вашей отрасли.</p>
                <a href="industry/index.html" class="btn">Выбрать отрасль</a>
            </div>
        </div>
    """
    content += get_footer()
    with open(f"{OUTPUT_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write(content)

def generate_geo_pages():
    geo_dir = f"{OUTPUT_DIR}/geo"
    os.makedirs(geo_dir, exist_ok=True)

    # Geo Index (List of Regions)
    content = get_header("Регионы обслуживания", depth=1)
    content += "<h2>Выберите регион</h2><ul class='list-group'>"
    for region in geography:
        region_slug = slugify(region)
        content += f"<li><a href='{region_slug}/index.html'>{region}</a></li>"
    content += "</ul>"
    content += get_footer()
    with open(f"{geo_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(content)

    # Region Pages
    for i, (region, cities) in enumerate(geography.items()):
        if DEMO_LIMIT and i > 2: break # Limit regions

        region_slug = slugify(region)
        region_dir = f"{geo_dir}/{region_slug}"
        os.makedirs(region_dir, exist_ok=True)

        content = get_header(f"Монтаж в {region}", depth=2)
        content += f"<h2>Города в регионе {region}</h2><ul class='list-group'>"
        for city in cities:
            city_slug = slugify(city)
            content += f"<li><a href='{city_slug}/index.html'>{city}</a></li>"
        content += "</ul>"
        content += get_footer()
        with open(f"{region_dir}/index.html", "w", encoding="utf-8") as f:
            f.write(content)

        # City Pages
        for j, city in enumerate(cities):
            if DEMO_LIMIT and j > 2: break # Limit cities

            city_slug = slugify(city)
            city_dir = f"{region_dir}/{city_slug}"
            os.makedirs(city_dir, exist_ok=True)

            content = get_header(f"Электрика в г. {city}", depth=3)
            content += f"<h2>Услуги в городе {city}</h2><p>Мы предоставляем полный спектр услуг по монтажу электрики и слаботочных систем в г. {city}.</p><ul class='list-group'>"
            for service in services:
                service_slug = slugify(service)
                content += f"<li><a href='{service_slug}.html'>{service}</a></li>"
            content += "</ul>"
            content += get_footer()
            with open(f"{city_dir}/index.html", "w", encoding="utf-8") as f:
                f.write(content)

            # Service Pages (City context)
            for k, service in enumerate(services):
                if DEMO_LIMIT and k > 5: break # Limit services

                service_slug = slugify(service)
                content = get_header(f"{service} в г. {city}", depth=3)
                content += f"""
                    <h2>{service} в городе {city}</h2>
                    <p>Профессиональный {service.lower()} в г. {city} по доступным ценам. Наши специалисты имеют большой опыт работы и готовы выполнить заказ любой сложности.</p>
                    <h3>Почему выбирают нас:</h3>
                    <ul>
                        <li>Гарантия качества</li>
                        <li>Соблюдение сроков</li>
                        <li>Лицензированные специалисты</li>
                    </ul>
                    <p><a href="index.html" class="btn">Вернуться к списку услуг в г. {city}</a></p>
                """
                content += get_footer()
                with open(f"{city_dir}/{service_slug}.html", "w", encoding="utf-8") as f:
                    f.write(content)

def generate_industry_pages():
    ind_dir = f"{OUTPUT_DIR}/industry"
    os.makedirs(ind_dir, exist_ok=True)

    # Industry Index
    content = get_header("Отраслевые решения", depth=1)
    content += "<h2>Выберите вашу отрасль</h2><ul class='list-group'>"
    for industry in industries:
        ind_slug = slugify(industry)
        content += f"<li><a href='{ind_slug}/index.html'>{industry}</a></li>"
    content += "</ul>"
    content += get_footer()
    with open(f"{ind_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(content)

    # Specific Industry Pages
    for i, industry in enumerate(industries):
        if DEMO_LIMIT and i > 2: break # Limit industries

        ind_slug = slugify(industry)
        industry_dir = f"{ind_dir}/{ind_slug}"
        os.makedirs(industry_dir, exist_ok=True)

        content = get_header(f"Услуги для: {industry}", depth=2)
        content += f"<h2>Электрика и слаботочные системы для: {industry}</h2><p>Специализированные решения.</p><ul class='list-group'>"
        for service in services:
            service_slug = slugify(service)
            content += f"<li><a href='{service_slug}.html'>{service}</a></li>"
        content += "</ul>"
        content += get_footer()
        with open(f"{industry_dir}/index.html", "w", encoding="utf-8") as f:
            f.write(content)

        # Service Pages (Industry context)
        for j, service in enumerate(services):
            if DEMO_LIMIT and j > 5: break # Limit services

            service_slug = slugify(service)
            content = get_header(f"{service} - {industry}", depth=2)
            content += f"""
                <h2>{service} для категории "{industry}"</h2>
                <p>Мы предлагаем профессиональный {service.lower()}, специально адаптированный под требования категории "{industry}".</p>
                <h3>Особенности работы:</h3>
                <p>Мы учитываем специфику вашего бизнеса и предлагаем оптимальные технические решения.</p>
                <p><a href="index.html" class="btn">Вернуться к услугам для "{industry}"</a></p>
            """
            content += get_footer()
            with open(f"{industry_dir}/{service_slug}.html", "w", encoding="utf-8") as f:
                f.write(content)

def main():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    print("Generating pages...")
    if DEMO_LIMIT:
        print("DEMO_LIMIT is enabled. Generating a subset of pages.")

    generate_index()
    generate_geo_pages()
    generate_industry_pages()

    # Copy CSS
    if os.path.exists("style.css"):
        shutil.copy("style.css", f"{OUTPUT_DIR}/style.css")
        print("Copied style.css to site/")
    else:
        print("WARNING: style.css not found in current directory!")

    print("Site generation complete.")

if __name__ == "__main__":
    main()
