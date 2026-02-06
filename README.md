
### Temat
Projekt dotyczy stworzenia systemu wspomagania decyzji dla graczy League of Legends w oparciu o sztuczną inteligencję. Głównym problemem jest optymalizacja wyboru bohatera (faza Draftu).

### Cel
Celem jest aplikacja w języku Python, która w czasie rzeczywistym analizuje skład sojuszników i przeciwników, a następnie rekomenduje bohatera maksymalizującego prawdopodobieństwo wygranej. System zwraca listę sugestii wraz z przewidywanym procentowym wskaźnikiem sukcesu, uwzględniając podział na role.

### Motywacja
Stworzyłęm ten projekt, ponieważ mam bardzo dużo godzin w grze oraz niedawno mój znajmoy napisał program do pobierania wyników meczów z bazy danych Riotu. Projekt ten może przydać się do zwiększenie szansy na wygraną w przyszłych meczach. 

### Dane wejściowe i metodologia
Projekt korzysta z relacyjnej bazy danych SQL zawierającej historię ok. 35 500 meczów.
* W programie mierzone są korelacja między zestawem 10 bohaterów a binarnym wynikiem meczu (Wygrana/Przegrana).
* Dane są filtrowane (odrzucam gry <16 min na podstawie statystyk złota) i transformowane techniką One-Hot Encoding z uwzględnieniem ról.

### Powiązanie z AI
Projekt realizuje zagadnienia z zakresu uczenia maszynowego:
* Typ problemu: Uczenie nadzorowane - Klasyfikacja binarna.
* Algorytm: XGBoost 
* Optymalizacja: Zastosowano bibliotekę Optuna do automatycznego strojenia parametrów modelu.

### Inne znane koncepcje rozwiązania problemu

* **[DraftGap](https://draftgap.com)** – Podobne podejście do problemu. Serwis wykorzystuje niemal identyczną metodologię. Zamiast prostych statystyk, używa modelu uczenia maszynowego analizującego pełne składy 5vs5, wyliczając procentową zmianę szansy na zwycięstwo.

* **Profesjonalne drużyny e-sportowe (np. G2, T1)** – Wykorzystują zbliżone narzędzia analityczne. Działy Data Science topowych organizacji tworzą prywatne modele oparte na algorytmach typu Gradient Boosting (XGBoost/LightGBM) lub sieciach neuronowych, trenowane na danych ze scrimów, aby symulować drafty.

* **[Mobalytics](https://mobalytics.gg)** – Stosuje częściowo podobną logikę. Ich moduł analizy przedmeczowej ocenia kompozycję (siła teamfightu, skalowanie, typ obrażeń) i szuka synergii, co jest zbliżone do celu klasyfikatora w tym projekcie.

* **[Blitz.gg](https://blitz.gg) / [Porofessor](https://porofessor.gg)** – Prezentują klasyczne podejście. Bazują na agregacji prostych statystyk historycznych (np. winrate pary na linii), nie dokonując predykcji wyniku dla całego zespołu przy użyciu AI, co wyróżnia mój projekt na tle typowych nakładek.


