# ==========================================================
#   STUDENT GRADE MANAGER - EXTREME EDITION v2.0
#   Lënda: Hyrje në Programim - Klasa X
#   Lloji: Console Application në Python
#   Veçoritë: 12 opsione, ngjyra, statistika, ruajtje skedari
# ==========================================================

import os
from datetime import datetime

# Aktivizo ngjyrat ANSI në Windows
if os.name == "nt":
    os.system("")


# ---------- KLASA E NGJYRAVE ----------
class C:
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    DIM      = "\033[2m"
    RED      = "\033[91m"
    GREEN    = "\033[92m"
    YELLOW   = "\033[93m"
    BLUE     = "\033[94m"
    MAGENTA  = "\033[95m"
    CYAN     = "\033[96m"
    WHITE    = "\033[97m"
    BG_RED   = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_BLUE  = "\033[44m"


# ---------- VARIABLA GLOBALE ----------
student_names  = []                       # listë me emra (str)
student_grades = []                       # listë me nota (float)
school_name    = "Shkolla e Mesme"        # str
max_grade      = 5                        # int
passing_grade  = 2.0                      # float
DATA_FILE      = "students_data.txt"
is_running     = True                     # bool


# ==========================================================
# FUNKSIONE NDIHMËSE
# ==========================================================
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_line(char="=", length=62, color=None):
    if color is None:
        color = C.CYAN
    print(f"{color}{char * length}{C.RESET}")


def print_header(title):
    clear_screen()
    print()
    print_line("=", 62, C.MAGENTA)
    print(f"{C.BOLD}{C.YELLOW}{title.center(62)}{C.RESET}")
    print_line("=", 62, C.MAGENTA)
    print()


def print_success(msg):
    print(f"{C.GREEN}✓ {msg}{C.RESET}")


def print_error(msg):
    print(f"{C.RED}✗ {msg}{C.RESET}")


def print_warning(msg):
    print(f"{C.YELLOW}⚠ {msg}{C.RESET}")


def print_info(msg):
    print(f"{C.CYAN}ℹ {msg}{C.RESET}")


def pause():
    input(f"\n{C.DIM}Shtyp ENTER për të vazhduar...{C.RESET}")


# ==========================================================
# STATUSI I NOTËS  (if / elif / else)
# ==========================================================
def grade_status(grade):
    if grade >= 4.5:
        return "Shkëlqyeshëm", C.GREEN
    elif grade >= 3.5:
        return "Shumë mirë", C.CYAN
    elif grade >= 2.5:
        return "Mirë", C.BLUE
    elif grade >= 2.0:
        return "Kaluar", C.YELLOW
    else:
        return "Dobët", C.RED


def fmt_grade(grade, width=10):
    _, color = grade_status(grade)
    return f"{color}{str(grade):<{width}}{C.RESET}"


def fmt_status(grade, width=18):
    status, color = grade_status(grade)
    return f"{color}{status:<{width}}{C.RESET}"


def colored_grade(grade):
    _, color = grade_status(grade)
    return f"{color}{C.BOLD}{grade}{C.RESET}"


def colored_status(grade):
    status, color = grade_status(grade)
    return f"{color}{status}{C.RESET}"


# ==========================================================
# VALIDIMI I EMRIT
# ==========================================================
def get_valid_name(prompt="Shkruaj emrin e nxënësit: "):
    while True:
        name = input(f"{C.CYAN}{prompt}{C.RESET}").strip()
        if name == "":
            print_error("Emri nuk mund të jetë bosh!")
        elif len(name) < 2:
            print_error("Emri duhet të ketë të paktën 2 shkronja!")
        elif any(ch.isdigit() for ch in name):
            print_error("Emri nuk mund të përmbajë numra!")
        else:
            return name


# ==========================================================
# VALIDIMI I NOTËS
# ==========================================================
def get_valid_grade(prompt="Shkruaj notën (1 - 5): "):
    while True:
        raw = input(f"{C.CYAN}{prompt}{C.RESET}").strip().replace(",", ".")
        if raw == "":
            print_error("Nota nuk mund të jetë bosh!")
            continue
        try:
            grade = float(raw)
        except ValueError:
            print_error("Gabim: Shkruaj një numër të vlefshëm!")
            continue

        if grade < 1 or grade > max_grade:
            print_error(f"Nota duhet të jetë ndërmjet 1 dhe {max_grade}!")
        else:
            return round(grade, 2)


# ==========================================================
# MENU
# ==========================================================
def show_menu():
    print_header("STUDENT GRADE MANAGER v2.0")
    print(f"{C.BOLD}{C.CYAN}  ZGJIDH NJË OPSION:{C.RESET}\n")
    print(f"  {C.GREEN}[1]{C.RESET}   ➕  Shto nxënës të re")
    print(f"  {C.GREEN}[2]{C.RESET}   📋  Paraqit të gjithë nxënësit")
    print(f"  {C.GREEN}[3]{C.RESET}   🔍  Kërko nxënës")
    print(f"  {C.GREEN}[4]{C.RESET}   📊  Statistika të plota")
    print(f"  {C.GREEN}[5]{C.RESET}   ✏️   Edito notën e nxënësit")
    print(f"  {C.GREEN}[6]{C.RESET}   🗑️   Fshi nxënës")
    print(f"  {C.GREEN}[7]{C.RESET}   🔀  Rendit nxënësit")
    print(f"  {C.GREEN}[8]{C.RESET}   🏆  Top 3 nxënësit më të mirë")
    print(f"  {C.GREEN}[9]{C.RESET}   🎯  Filtro sipas statusit")
    print(f"  {C.GREEN}[10]{C.RESET}  💾  Ruaj të dhënat në skedar")
    print(f"  {C.GREEN}[11]{C.RESET}  📂  Ngarko të dhëna nga skedari")
    print(f"  {C.RED}[12]{C.RESET}  🚪  Dil")
    print()
    print_line("-", 62, C.DIM)


# ==========================================================
# 1) SHTO NXËNËS
# ==========================================================
def add_student():
    print_header("SHTIMI I NXËNËSVE TË RE")
    name = get_valid_name()
    grade = get_valid_grade()

    student_names.append(name)
    student_grades.append(grade)

    print()
    print_success(f"Nxënësi '{C.BOLD}{name}{C.RESET}{C.GREEN}' u shtua me sukses!")
    print_info(f"Nota: {colored_grade(grade)}  |  Statusi: {colored_status(grade)}")
    print_info(f"Totali i nxënësve tani: {C.BOLD}{len(student_names)}{C.RESET}")
    pause()


# ==========================================================
# 2) PARAQIT TË GJITHË NXËNËSIT (cikli for)
# ==========================================================
def show_students():
    print_header("LISTA E NXËNËSVE")

    if len(student_names) == 0:
        print_warning("Nuk ka nxënës të regjistruar!")
        pause()
        return

    print(f"{C.BOLD}{C.MAGENTA}{'Nr.':<6}{'Emri':<26}{'Nota':<10}{'Statusi':<18}{C.RESET}")
    print_line("-", 62, C.DIM)

    total = 0.0
    for i in range(len(student_names)):
        grade = student_grades[i]
        total += grade
        print(f"{C.YELLOW}{str(i + 1) + '.':<6}{C.RESET}"
              f"{C.WHITE}{student_names[i]:<26}{C.RESET}"
              f"{fmt_grade(grade, 10)}"
              f"{fmt_status(grade, 18)}")

    print_line("-", 62, C.DIM)
    avg = total / len(student_grades)
    print(f"{C.BOLD}Totali: {len(student_names)} nxënës  |  "
          f"Mesatarja: {avg:.2f}  |  Shuma: {total:.2f}{C.RESET}")
    pause()


# ==========================================================
# 3) KËRKO NXËNËS
# ==========================================================
def search_student():
    print_header("KËRKIMI I NXËNËSVE")

    if len(student_names) == 0:
        print_warning("Nuk ka nxënës për të kërkuar!")
        pause()
        return

    query = input(f"{C.CYAN}Kërko nxënësin (emër ose pjesë e emrit): {C.RESET}").strip().lower()

    if query == "":
        print_error("Kërkimi nuk mund të jetë bosh!")
        pause()
        return

    results = []
    for i in range(len(student_names)):
        if query in student_names[i].lower():
            results.append(i)

    print()
    if len(results) == 0:
        print_error(f"Nuk u gjet asnjë nxënës që përmban '{query}'.")
    else:
        print_success(f"U gjetën {len(results)} rezultat(e):\n")
        print(f"{C.BOLD}{C.MAGENTA}{'Nr.':<6}{'Emri':<26}{'Nota':<10}{'Statusi':<18}{C.RESET}")
        print_line("-", 62, C.DIM)
        for i in results:
            grade = student_grades[i]
            print(f"{C.YELLOW}{str(i + 1) + '.':<6}{C.RESET}"
                  f"{C.WHITE}{student_names[i]:<26}{C.RESET}"
                  f"{fmt_grade(grade, 10)}"
                  f"{fmt_status(grade, 18)}")
    pause()


# ==========================================================
# 4) STATISTIKA TË PLOTA
# ==========================================================
def show_statistics():
    print_header("STATISTIKA TË PLOTA")

    if len(student_grades) == 0:
        print_warning("Nuk ka të dhëna për statistika!")
        pause()
        return

    total = sum(student_grades)
    count = len(student_grades)
    average = total / count
    highest = max(student_grades)
    lowest = min(student_grades)

    best_idx = student_grades.index(highest)
    worst_idx = student_grades.index(lowest)

    passed = 0
    for g in student_grades:
        if g >= passing_grade:
            passed += 1
    failed = count - passed
    pass_rate = passed / count * 100

    dist = {
        "Shkëlqyeshëm": 0,
        "Shumë mirë": 0,
        "Mirë": 0,
        "Kaluar": 0,
        "Dobët": 0,
    }
    for g in student_grades:
        s, _ = grade_status(g)
        dist[s] += 1

    print(f"{C.BOLD}{C.YELLOW}📈 PËRMBLEDHJE:{C.RESET}")
    print(f"  Numri i nxënësve : {C.BOLD}{count}{C.RESET}")
    print(f"  Shuma e notave   : {C.BOLD}{total:.2f}{C.RESET}")
    print(f"  Mesatarja        : {C.BOLD}{C.CYAN}{average:.2f}{C.RESET}")
    print(f"  Nota më e lartë  : {colored_grade(highest)}  ({C.GREEN}{student_names[best_idx]}{C.RESET})")
    print(f"  Nota më e ulët   : {colored_grade(lowest)}  ({C.RED}{student_names[worst_idx]}{C.RESET})")
    print()

    print(f"{C.BOLD}{C.YELLOW}🎯 KALIMI:{C.RESET}")
    print(f"  Kaluar    : {C.GREEN}{passed}{C.RESET} / {count}  ({pass_rate:.1f}%)")
    print(f"  Ngelur    : {C.RED}{failed}{C.RESET} / {count}  ({100 - pass_rate:.1f}%)")
    print()

    print(f"{C.BOLD}{C.YELLOW}📊 SHPËRNDARJA SIPAS STATUSIT:{C.RESET}")
    status_map = {
        "Shkëlqyeshëm": 5.0,
        "Shumë mirë": 4.0,
        "Mirë": 3.0,
        "Kaluar": 2.5,
        "Dobët": 1.0,
    }
    for status, n in dist.items():
        if n == 0:
            continue
        _, color = grade_status(status_map[status])
        bar = "█" * n
        print(f"  {color}{status:<15}{C.RESET} {color}{bar}{C.RESET} {n}")
    pause()


# ==========================================================
# 5) EDITO NOTËN
# ==========================================================
def edit_student():
    print_header("EDITIMI I NOTËS")

    if len(student_names) == 0:
        print_warning("Nuk ka nxënës për të edituar!")
        pause()
        return

    name = input(f"{C.CYAN}Shkruaj emrin e nxënësit: {C.RESET}").strip().lower()

    found = False
    for i in range(len(student_names)):
        if student_names[i].lower() == name:
            found = True
            print_info(f"Nxënësi: {C.BOLD}{student_names[i]}{C.RESET}")
            print_info(f"Nota aktuale: {colored_grade(student_grades[i])}")
            new_grade = get_valid_grade("Shkruaj notën e re (1 - 5): ")
            student_grades[i] = new_grade
            print_success(f"Nota u përditësua në {colored_grade(new_grade)}!")
            break

    if not found:
        print_error(f"Nxënësi '{name}' nuk u gjet!")
    pause()


# ==========================================================
# 6) FSHI NXËNËS
# ==========================================================
def delete_student():
    print_header("FSHIRJA E NXËNËSIT")

    if len(student_names) == 0:
        print_warning("Nuk ka nxënës për të fshirë!")
        pause()
        return

    name = input(f"{C.CYAN}Shkruaj emrin e nxënësit për t'u fshirë: {C.RESET}").strip().lower()

    found = False
    for i in range(len(student_names)):
        if student_names[i].lower() == name:
            found = True
            confirm = input(f"{C.YELLOW}Jeni i sigurt? (p/j): {C.RESET}").strip().lower()
            if confirm == "p":
                removed_name = student_names.pop(i)
                removed_grade = student_grades.pop(i)
                print_success(f"Nxënësi '{removed_name}' (nota {removed_grade}) u fshi!")
            else:
                print_info("Fshirja u anulua.")
            break

    if not found:
        print_error(f"Nxënësi '{name}' nuk u gjet!")
    pause()


# ==========================================================
# 7) RENDIT NXËNËSIT
# ==========================================================
def sort_students():
    print_header("RENDITJA E NXËNËSVE")

    if len(student_names) == 0:
        print_warning("Nuk ka nxënës për të renditur!")
        pause()
        return

    print(f"{C.BOLD}Zgjidh kriterin:{C.RESET}")
    print(f"  {C.GREEN}[1]{C.RESET} Sipas emrit (A → Z)")
    print(f"  {C.GREEN}[2]{C.RESET} Sipas emrit (Z → A)")
    print(f"  {C.GREEN}[3]{C.RESET} Sipas notës (lart → poshtë)")
    print(f"  {C.GREEN}[4]{C.RESET} Sipas notës (poshtë → lart)")
    choice = input(f"{C.CYAN}Zgjidh: {C.RESET}").strip()

    combined = list(zip(student_names, student_grades))

    if choice == "1":
        combined.sort(key=lambda x: x[0].lower())
    elif choice == "2":
        combined.sort(key=lambda x: x[0].lower(), reverse=True)
    elif choice == "3":
        combined.sort(key=lambda x: x[1], reverse=True)
    elif choice == "4":
        combined.sort(key=lambda x: x[1])
    else:
        print_error("Opsion i pavlefshëm!")
        pause()
        return

    student_names.clear()
    student_grades.clear()
    for n, g in combined:
        student_names.append(n)
        student_grades.append(g)

    print_success("Renditja u krye me sukses!")
    pause()


# ==========================================================
# 8) TOP 3 NXËNËSIT
# ==========================================================
def show_top_students():
    print_header("TOP 3 NXËNËSIT MË TË MIRË")

    if len(student_names) == 0:
        print_warning("Nuk ka nxënës!")
        pause()
        return

    combined = list(zip(student_names, student_grades))
    combined.sort(key=lambda x: x[1], reverse=True)

    medals = ["🥇", "🥈", "🥉"]
    top_n = min(3, len(combined))

    print()
    for i in range(top_n):
        name, grade = combined[i]
        status, color = grade_status(grade)
        print(f"  {medals[i]}  {C.BOLD}{color}{name}{C.RESET}  "
              f"- Nota: {colored_grade(grade)}  [{color}{status}{C.RESET}]")
    pause()


# ==========================================================
# 9) FILTRO SIPAS STATUSIT
# ==========================================================
def filter_by_status():
    print_header("FILTRIMI SIPAS STATUSIT")

    if len(student_names) == 0:
        print_warning("Nuk ka nxënës!")
        pause()
        return

    print(f"{C.BOLD}Zgjidh statusin:{C.RESET}")
    print(f"  {C.GREEN}[1]{C.RESET} Shkëlqyeshëm")
    print(f"  {C.GREEN}[2]{C.RESET} Shumë mirë")
    print(f"  {C.GREEN}[3]{C.RESET} Mirë")
    print(f"  {C.GREEN}[4]{C.RESET} Kaluar")
    print(f"  {C.GREEN}[5]{C.RESET} Dobët")
    choice = input(f"{C.CYAN}Zgjidh: {C.RESET}").strip()

    statuses = {
        "1": "Shkëlqyeshëm",
        "2": "Shumë mirë",
        "3": "Mirë",
        "4": "Kaluar",
        "5": "Dobët",
    }

    if choice not in statuses:
        print_error("Opsion i pavlefshëm!")
        pause()
        return

    target = statuses[choice]
    print()
    count = 0
    for i in range(len(student_names)):
        s, color = grade_status(student_grades[i])
        if s == target:
            count += 1
            print(f"  {C.YELLOW}{count}.{C.RESET} {C.WHITE}{student_names[i]}{C.RESET} "
                  f"- Nota: {colored_grade(student_grades[i])}")

    if count == 0:
        print_warning(f"Asnjë nxënës nuk ka statusin '{target}'.")
    else:
        print()
        print_info(f"Totali: {count} nxënës me statusin '{target}'.")
    pause()


# ==========================================================
# 10) RUAJ TË DHËNAT
# ==========================================================
def save_to_file():
    print_header("RUAJTJA E TË DHËNAVE")

    if len(student_names) == 0:
        print_warning("Nuk ka të dhëna për të ruajtur!")
        pause()
        return

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write(f"# Ruajtur më: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            for i in range(len(student_names)):
                f.write(f"{student_names[i]}|{student_grades[i]}\n")
        print_success(f"Të dhënat u ruajtën në '{DATA_FILE}'!")
        print_info(f"Totali: {len(student_names)} nxënës.")
    except OSError as e:
        print_error(f"Gabim gjatë ruajtjes: {e}")
    pause()


# ==========================================================
# 11) NGARKO TË DHËNAT
# ==========================================================
def load_from_file():
    print_header("NGARKIMI I TË DHËNAVE")

    if not os.path.exists(DATA_FILE):
        print_warning(f"Skedari '{DATA_FILE}' nuk ekziston!")
        pause()
        return

    loaded = 0
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "" or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) != 2:
                    continue
                name, grade_text = parts
                try:
                    grade = float(grade_text)
                except ValueError:
                    continue
                if name not in student_names:
                    student_names.append(name)
                    student_grades.append(grade)
                    loaded += 1
        print_success(f"U ngarkuan {loaded} nxënës nga '{DATA_FILE}'!")
        print_info(f"Totali tani: {len(student_names)} nxënës.")
    except OSError as e:
        print_error(f"Gabim gjatë ngarkimit: {e}")
    pause()


# ==========================================================
# 12) MAIN - menuja kryesore (while)
# ==========================================================
def main():
    clear_screen()
    print()
    print(f"{C.BOLD}{C.MAGENTA}╔{'═' * 60}╗{C.RESET}")
    print(f"{C.BOLD}{C.MAGENTA}║{C.RESET}{C.YELLOW}{'★  MIRË SE VINI NË STUDENT GRADE MANAGER  ★':^60}{C.RESET}{C.BOLD}{C.MAGENTA}║{C.RESET}")
    print(f"{C.BOLD}{C.MAGENTA}║{C.RESET}{C.CYAN}{'Hyrje në Programim - Klasa X':^60}{C.RESET}{C.BOLD}{C.MAGENTA}║{C.RESET}")
    print(f"{C.BOLD}{C.MAGENTA}╚{'═' * 60}╝{C.RESET}")
    input(f"\n{C.DIM}Shtyp ENTER për të filluar...{C.RESET}")

    running = True
    while running:
        show_menu()
        choice = input(f"{C.BOLD}{C.CYAN}Zgjidh një opsion (1-12): {C.RESET}").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            show_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            show_statistics()
        elif choice == "5":
            edit_student()
        elif choice == "6":
            delete_student()
        elif choice == "7":
            sort_students()
        elif choice == "8":
            show_top_students()
        elif choice == "9":
            filter_by_status()
        elif choice == "10":
            save_to_file()
        elif choice == "11":
            load_from_file()
        elif choice == "12":
            print_header("LARGIMI")
            print(f"{C.YELLOW}Faleminderit që përdorët Student Grade Manager!{C.RESET}")
            print(f"{C.CYAN}Mirupafshim! 👋{C.RESET}\n")
            running = False
        else:
            print_error("Opsion i pavlefshëm! Provoni përsëri (1-12).")
            pause()


# ==========================================================
# PIKA E NISJES
# ==========================================================
if __name__ == "__main__":
    main()