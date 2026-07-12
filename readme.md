# Problem biznesowy: Opóźnienia w księgowaniu faktur zakupowych

### Odtworzenie istniejącego procesu AS IS
Projekt rozpocząłem od odtworzenia procesu AS IS przebiegu faktury - poniżej proces w notacji **BPMN 2.0**
![Diagram Procesu AS IS](images/diagram_as_is.jpg)

### Stworzenie datasetu do analizy istniejącego procesu AS IS
Na potrzeby projektu stworzyłem skrypt w pythonie [generate_dataset.py](scripts/generate_dataset.py) generujący dane do poniższego datasetu, aby odwzorować opóźnienia i błędy w obecnym procesie.
![Dataset](images/dataset.jpg)

### Stworzenie bazy danych na podstawie datasetu
Na podstawie wygenerowanych danych stworzyłem bazę danych w **MS SQL** i za pomocą bulk insertu zaimportowałem do niego dane
![Database](images/database.png)

### Analiza w Power BI 
Łącząc się z bazą w Power BI stworzyłem interaktywny dashboard pozwalający na dalsze monitorowanie przebiegu fakturowania i znalezienie głównych problemów.
![Dashobard_1](images/dashboard_1.png)
![Dashobard_2](images/dashboard_2.png)
![Dashobard_3](images/dashboard_3.png)

### Analiza procesu i próba znalezienia kluczowych bottleneck'ów
Po analizie dashboardów największym wąskim gardłem okazał się być dział akceptacji, brak dokumentów PZ i rozbieżności cenowe na zamówieniach i fakturach. Poniżej mapa z analizą przyczyn:
![Mapa analizy przyczyn opóźnień w procesie fakturowania](images/invoice_analysis_mindmap.jpg)

**Rozwiązanie braku dokumentów PZ** - wyposażenie magazynierów w skanery - po sczytaniu dokumentu WZ, system automatycznie generuje dokument PZ w bazie.  

**Rozwiązanie rozbieżności cenowych** - konieczność ponownego sprawdzenia szablonów do zamówień w systemie ERP, istnieje możliwość, że dostawcy gdzie najczęściej pojawiają się rozbieżności naliczają rabat powyżej konkretnej ilości zamówionych sztuk danego produktu.

### Modelowanie procesu TO BE wraz z uwzględnieniem usprawnień 
Jako rozwiązanie powyższych problemów przygotowałem zoptymalizowany proces. Poniżej model TO BE wraz z uwzględnieniem usprawnień (m.in. automatyczna akceptacja niskich kwot i przekierowania podczas urlopów).
![Diagram Procesu TO BE](images/diagram_to_be.jpg)
