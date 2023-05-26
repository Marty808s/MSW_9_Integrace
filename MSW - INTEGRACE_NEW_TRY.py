import numpy as np
import sympy as sp
import datetime
import matplotlib.pyplot as plt


#OUTPUT
lichobeznik_output = []
obdelnik_output = []
numpy_trapz_output = []
analytic_output = []


#OUTPUT cas
lichobeznik_cas = []
obdelnik_cas = []
numpy_trapz_cas = []
analytic_cas = []

#DEFINICE FUNKCE:

# Definice funkce polynomicka(x)

#DULEZITA POZNAMKA! POUZITI NUMPY NA SIN A LOG ZNAMENA PROBLEM,
# NUMPY KNIHOVNA NEUMOZNUJE NASLEDNY POCET PO VYVOLANI FUNKCE INSERTOVAT DO X JAKO DO PROMENNE
#PROTO JSEM POUZIL KNIHOVNU SYMPY

x = sp.symbols('x')

def polynomicka(x):
    return x**2

def harmonicka(x):
    return 2*sp.sin(x**2)

def logaritmicka(x):
    return sp.log(x**4)
#--------------------------------------------------------------------------------------------------------
#LICHOBEZNIKOVA METODA

def lichobeznik_method(funkce, a, b, n):
    start_time = datetime.datetime.now()
    integral = 0  # hodnota integrálu
    krok = (b - a) / n #definice velikosti kroku
    x_i = a #přetypování začátku

    for _ in range(n): #cyklus v počtu iteraci
        aktualni_pozice = x_i + krok  # aktualizace pozice pro každý interval

        iterace = (funkce.subs(x, x_i) + funkce.subs(x, aktualni_pozice)) * krok / 2  # výpočet plochy lichoběžníku
        #  pro nahrazení symbolu x za konkrétní hodnoty
        # 1. proměnná = znak, který nahradím hodnotou druhé proměnné : (značka,hodnota)

        integral += iterace
        x_i = aktualni_pozice  # posun na další interval

    timer_licho = (datetime.datetime.now() - start_time)
    timer_licho_ms = timer_licho.total_seconds() * 1000
    print(f"hodnota lichobeznik: {integral} čas: {timer_licho_ms} ms")

    lichobeznik_output.append((integral, timer_licho_ms))
    return integral, timer_licho_ms

#--------------------------------------------------------------------------------------------------------
#OBDELNIKOVA METODA

def obdelnikova_method(funkce, a, b, n):
    start_time = datetime.datetime.now()
    integral = 0  # hodnota integrálu
    krok = (b - a) / n #definice velikosti kroku
    x_i = a #přetypování začátku

    for _ in range(n):
        posun = x_i + krok
        iterace = funkce.subs(x,posun) * (posun-x_i)
        integral += iterace
        x_i = posun

    timer_obdelnik = (datetime.datetime.now() - start_time)
    timer_obdelnik_ms = timer_obdelnik.total_seconds() * 1000
    print(f"hodnota lichobeznik: {integral} čas: {timer_obdelnik_ms} ms")

    obdelnik_output.append((integral, timer_obdelnik_ms))
    return integral, timer_obdelnik_ms

#--------------------------------------------------------------------------------------------------------
#NUMPY TRAPZ METODA  BUILT-IN

def numpy_trapz(funkce,a,b,n):
    start_time = datetime.datetime.now()
    dx = (b - a) / n #výpočet kroku
    x_vec = np.arange(a, b + dx, dx)


    f_func = sp.lambdify(x, funkce)
    #převádí symbolickou funkci na ekvivalentní funkci, která je vyhodnocovatelná pomocí NumPy

    trapz_method = np.trapz(f_func(x_vec), x_vec)

    timer_numpy_trapz = (datetime.datetime.now() - start_time)
    timer_numpy_trapz_ms = timer_numpy_trapz.total_seconds() * 1000

    #timer_numpy_trapz_ms = round(timer_numpy_trapz_ms,3)

    print(f"hodnota numpy_trapz: {trapz_method} čas: {timer_numpy_trapz_ms} ms")

    numpy_trapz_output.append((trapz_method, timer_numpy_trapz_ms))
    return trapz_method, timer_numpy_trapz_ms

"""
Při opakovaném volání metody v rámci stejného běhu programu se tyto inicializace a předzpracování již neprovádějí, 
protože 
potřebné struktury jsou již v paměti. To může vést ke zdánlivě rychlejšímu běhu metody.

Při použití modulu timeit pro měření času je tato "efekt načítání" redukována, protože timeit spouští kód opakovaně 
a zjišťuje průměrný čas běhu. To zahrnuje i první inicializační čas a poskytuje tak přesnější měření časové náročnosti 
metody.

"""

#--------------------------------------------------------------------------------------------------------
#ANALYTIC SOLUTION - PRO MNE

def analytic_solution(funkce,vec):
    start_time = datetime.datetime.now()
    analytic_sol = sp.integrate(funkce, vec)
    timer_analytic_sol = (datetime.datetime.now() - start_time)
    timer_analytic_sol_ms = timer_analytic_sol.total_seconds() * 1000

    #timer_analytic_sol_ms = round(timer_analytic_sol_ms,5)

    print(f"ANALYTIC: {float(analytic_sol)} čas: {timer_analytic_sol_ms} ms")

    analytic_output.append((float(analytic_sol), timer_analytic_sol_ms))
    return analytic_sol, timer_analytic_sol_ms
#--------------------------------------------------------------------------------------------------------
#TĚLO PROGRAMU

#nazvy: polynomicka,harmonicka,logaritmicka
#metody: lichobeznik, obdelnik, numpy_trapz, analytic solution


#POLYNOMICKA
analytic_solution(polynomicka(x),(x,0,10))
lichobeznik_method(polynomicka(x), 0, 10, 1000)
obdelnikova_method(polynomicka(x), 0, 10, 1000)
numpy_trapz(polynomicka(x),0,10,1000)


#HARMONICKA
analytic_solution(harmonicka(x),(x,0,10))
lichobeznik_method(harmonicka(x), 0, 10, 1000)
obdelnikova_method(harmonicka(x), 0, 10, 1000)
numpy_trapz(harmonicka(x), 0, 10, 1000)

#LOGARITMICKA
analytic_solution(logaritmicka(x),(x,1,10))
lichobeznik_method(logaritmicka(x), 1, 10, 1000)
obdelnikova_method(logaritmicka(x), 1, 10, 1000)
numpy_trapz(logaritmicka(x), 1, 10, 1000)

print("\n")

print("-------------------------------------FINAL OUTPUT-------------------------------------")
#---------------------------------------------------------------------
print("ANALYTICKE SOLUTION:", analytic_output)
print("LICHOBEZNIKOVA SOLUTION:", lichobeznik_output)
print("OBDELNIKOVA SOLUTION:", obdelnik_output)
print("NUMPY TRAPZ METODA:", numpy_trapz_output)


# VÝPOČET ODCHYLEK
odchylky_licho = []
odchylky_obdelnik = []
odchylky_numpy = []

print("\n")

"""
Ve smyčce for jsou proměnné analytic a lichobeznik při každé iteraci přiřazeny korespondujícím 
prvkům z analytic_output 
lichobeznik_output. Například při první iteraci budou obsahovat první prvky obou seznamů.
"""

for analytic, lichobeznik in zip(analytic_output, lichobeznik_output):
    # funkce zip, slouzi k prochazeni ve for cyklu ve
    # vice seznamech naraz

    odchylka_licho = abs(analytic[0] - lichobeznik[0]) #abs pro nezapornou odchylku (jde nam o rozmer)
    odchylky_licho.append(float(odchylka_licho))

for analytic, obdelnik in zip(analytic_output, obdelnik_output):
    odchylka_obdelnik = abs(analytic[0] - obdelnik[0])
    odchylky_obdelnik.append(float(odchylka_obdelnik))

for analytic, numpy in zip(analytic_output, numpy_trapz_output):
    odchylka_numpy = abs(analytic[0] - numpy[0])
    odchylky_numpy.append(float(odchylka_numpy))

print("ODCHYLKY LICHOBĚŽNÍKOVÁ METODA:", odchylky_licho)
print("ODCHYLKY OBDELNÍKOVÁ METODA:", odchylky_obdelnik)
print("ODCHYLKY NUMPY TRAPZ METODA:", odchylky_numpy)

#VŽDY SE JEDNÁ O ODCHYLKU DANÉ METODY OD ANALYTICKÉ METODY
#----------------------------------------------------------------------

#PŘEVOD ČASŮ DANÝCH METOD
for analytic, lichobeznik, obdelnik, numpy_meth \
        in zip(analytic_output, lichobeznik_output, obdelnik_output, numpy_trapz_output):

    analytic_cas.append(analytic[1])
    lichobeznik_cas.append(lichobeznik[1])
    obdelnik_cas.append(obdelnik[1])
    numpy_trapz_cas.append(numpy_meth[1])

print(numpy_trapz_cas)
print(obdelnik_cas)
print(lichobeznik_cas)
print(analytic_cas)

#----------------------------------------------------------------------
#GRAF ČASY


x = np.arange(len(analytic_cas))

width = 0.2  # Šířka sloupce

plt.bar(x - width, lichobeznik_cas, width=width, label="Lichobeznikova metoda")
plt.bar(x, obdelnik_cas, width=width, label="Obdelnikova metoda", align='center')
plt.bar(x + width, analytic_cas, width=width, label="Analytic method")
plt.bar(x + 1.5 * width, numpy_trapz_cas, width=width, label= "Numpy Trapz method", align='edge')

# Nastavení popisků os a titulku
plt.xlabel("Funkce")
plt.ylabel("Čas (ms)")
plt.title("Časová náročnost metod")

# Nastavení značek na ose x
plt.xticks(x, x + 1)
plt.xticks(x, ['Polynomicka', 'Harmonicka', 'Logaritmicka'])

# Zobrazení legendy
plt.legend()

# Zobrazení mřížky
plt.grid()


# Zobrazení grafu
plt.show()

#-----------------------------------------------------------------------------------------------
#GRAF - ODCHYLKY

#každou zvlášť, nulová čára (sloupcově)

# X-ová osa (pořadí výpočtu)
x_axis = range(1, len(odchylky_licho) + 1)

plt.ylim(0, max(max(odchylky_licho), max(odchylky_obdelnik), max(odchylky_numpy)) * 0.1)
# Nastavte vhodný násobek maxima


width = 0.2  # Šířka sloupce

plt.bar(x - width, odchylky_licho, width=width, label="Lichobeznikova metoda")
plt.bar(x, odchylky_obdelnik, width=width, label="Obdelnikova metoda", align='center')
plt.bar(x + width, odchylky_numpy, width=width, label="Numpy Trapz method")

plt.xticks(x, ['Polynomicka', 'Harmonicka', 'Logaritmicka'])

# Nastavení popisků os a titulku
plt.xlabel("Funkce")
plt.ylabel("Odchylka od analytického řešení")
plt.title("Odchylky metod od analytického řešení")

plt.grid()

# Legenda
plt.legend()

# Zobrazení grafu
plt.show()
#----------------------------------------------------------
