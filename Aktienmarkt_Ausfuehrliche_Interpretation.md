# Hocheffiziente Aktienmarktanalyse: Eine empirische Untersuchung von über 6 Millionen Datenpunkten (2010–2026)

---

## 1. Einleitung und Methodik
Diese wissenschaftliche Ausarbeitung befasst sich mit der empirischen Analyse des globalen Aktienmarktes auf Basis des umfassenden Kaggle-Datensatzes *„All Stock Market Data (Daily Updates)“*. 

### Datensatz und Repräsentativität
* **Datenumfang**: Der Rohdatensatz umfasst über **6.083.498 wöchentliche Beobachtungen** über einen Zeitraum von **16,4 Jahren** (4. Januar 2010 bis 18. Mai 2026).
* **Universum**: Es werden insgesamt **16.322 eindeutige Ticker (Aktiensymbole)** analysiert. Dies deckt das gesamte Spektrum von Mega-Caps (z. B. Apple, Nvidia) über Mid- und Small-Caps bis hin zu hochorientierten Micro-Caps und Penny Stocks (OTC-Werte) ab.
* **Methodischer Ansatz**: Die täglichen Kursdaten wurden auf **wöchentlicher Basis (Week-Start bis Close-EOW)** aggregiert. Diese Methodik ist in der Finanzökonometrie etabliert, da sie:
  1. Rauschen und kurzfristige Marktverzerrungen (z. B. Daytrading-Effekte) glättet.
  2. Kalendereffekte innerhalb der Woche (z. B. den „Montagseffekt“) kontrolliert.
  3. Die rechnerische Effizienz bei massiven Big-Data-Mengen wahrt, ohne signifikant an statistischer Kraft zu verlieren.

---

## 2. Detaillierte Interpretation der Analyseergebnisse und Diagramme

### Kapitel 2.1: Datenverfügbarkeit und Marktstruktur (Diagramm 1)
* **Visualisierung**: Das Diagramm `01_datenverfuegbarkeit.png` zeigt den Verlauf der aktiven Ticker pro Jahr.
* **Empirischer Befund**: 2010 startete der Datensatz mit **5.783 aktiven Tickern**. Bis 2025 stieg diese Zahl kontinuierlich auf **13.174 Ticker** an (ein Zuwachs von über **127%**).
* **Ökonomische Interpretation**:
  * **Expansion der Datenabdeckung**: Dieser Anstieg spiegelt nicht nur reale Börsengänge (IPOs) wider, sondern vor allem eine verbesserte Datenabdeckung im Zeitverlauf (Einbeziehung kleinerer Indizes, Regionalmärkte und OTC-Plattformen).
  * **Überlebenden-Verzerrung (Survivorship Bias)**: Da der Datensatz im Zeitverlauf wächst, müssen wir berücksichtigen, dass delistete Unternehmen (durch Insolvenz, Fusionen oder Übernahmen) in den früheren Jahren möglicherweise unterrepräsentiert sind. Für wissenschaftliche Arbeiten ist dies ein kritischer Punkt: Ein reiner Fokus auf heute existierende Unternehmen überschätzt historische Renditen systematisch.

### Kapitel 2.2: Langfristige Marktentwicklung & Die Small-Firm-Anomalie (Diagramm 2 & 10)
* **Visualisierung**: `02_marktentwicklung_trends.png` zeigt den kumulierten Verlauf eines gleichgewichteten Marktindexes (Basis 100 im Jahr 2010).
* **Empirischer Befund**:
  * Der gleichgewichtete Index stieg von **103,23** (Januar 2010) auf den astronomischen Wert von **1.258.495,47** (Mai 2026).
  * Dies entspricht einer **durchschnittlichen wöchentlichen Rendite von 1,13%** bzw. einer **annualisierten Rendite von ca. 79,47%** über den Gesamtmarkt!
  * **Sharpe Ratio (ann.)**: 3,97 (gleichgewichtet).
* **Kritische akademische Dekonstruktion**:
  * *Warum ist diese Rendite so extrem hoch im Vergleich zu klassischen Indizes wie dem S&P 500 (~10% p.a.)?*
  * **Gleichgewichtung vs. Marktkapitalisierungsgewichtung**: In einem gleichgewichteten Index hat eine 100-Millionen-Dollar-Aktie das gleiche Gewicht wie eine 3-Billionen-Dollar-Aktie (z. B. Apple). 
  * **Größen-Effekt (Size Effect / Small-Firm Anomaly)** nach *Fama und French (1992)*: Small- und Micro-Caps weisen historisch höhere Renditen auf, um ihr signifikant höheres Risiko, mangelnde Liquidität und Insolvenzwahrscheinlichkeiten zu kompensieren. 
  * **Asymmetrische Hebelwirkung durch Penny Stocks**: Viele OTC-Aktien im Datensatz verzeichnen extreme prozentuale Kurssprünge (z. B. von $0,001 auf $0,01 = +900%). Im gleichgewichteten Aggregat ziehen diese Ausreißer den Mittelwert massiv nach oben, während ein realer, kapitalgewichteter Anleger diesen Effekt aufgrund mangelnder Marktliquidität niemals in dieser Form replizieren könnte.

### Kapitel 2.3: Rendite- und Risiko-Analyse (Diagramm 3)
* **Visualisierung**: `03_rendite_risiko_analyse.png` stellt das Verteilungshistogramm der wöchentlichen Renditen dar.
* **Empirische Kennzahlen**:
  * **Mittelwert**: 1,05% pro Woche.
  * **Median**: 0,00% pro Woche.
  * **Schiefe (Skewness)**: **7,55** (extrem rechtsschief).
  * **Kurtosis (Wölbung)**: **121,24** (extrem leptokurtisch / „Fat Tails“).
  * **Normalitätstests**: Jarque-Bera (JB = 4.242.185, p = 0.00) und Kolmogorov-Smirnov (p = 1.89e-291) lehnen die Nullhypothese einer Normalverteilung auf dem 99,9%-Niveau ab.
* **Ökonomische Interpretation**:
  * **Verletzung der Normalverteilungsannahme**: Die klassische Finanztheorie (z. B. die Portfoliotheorie nach Markowitz oder das Black-Scholes-Optionspreismodell) nimmt an, dass Renditen log-normalverteilt sind. Diese Annahme wird hier drastisch widerlegt.
  * **Fat Tails & Schwarze Schwäne (Nassim Taleb)**: Eine Kurtosis von 121,24 zeigt, dass extreme Marktbewegungen (sowohl positive als auch negative) millionenfach häufiger auftreten, als es die Glockenkurve prognostiziert. Risikomanagement-Modelle, die auf der Standardabweichung basieren (z. B. der klassische Value-at-Risk), unterschätzen das tatsächliche Ruin-Risiko fatal.
  * **Positive Schiefe**: Der Markt zeigt eine Tendenz zu extremen positiven Ausreißern (Multibaggern), während der Verlust nach unten auf -100% begrenzt ist.

### Kapitel 2.4: Volatilitätsanalyse & Clustering (Diagramm 4)
* **Visualisierung**: `04_volatilitaetsanalyse.png` untersucht das Phänomen schwankender Risikoregime.
* **Empirische Kennzahlen**:
  * **Durchschnittliche annualisierte Volatilität**: 86,40% (Median: 34,60%).
  * **Autokorrelation der Volatilität**: Lag 1 = **0,73**, Lag 4 = **0,62**, Lag 12 = **0,47**.
* **Ökonomische Interpretation**:
  * **Volatilitäts-Clustering (ARCH/GARCH-Effekt nach Robert Engle)**: Die hohe und langsam abklingende Autokorrelation beweist empirisch, dass auf Phasen hoher Volatilität mit sehr hoher Wahrscheinlichkeit wieder Phasen hoher Volatilität folgen (und umgekehrt). Turbulente Marktphasen „erinnern“ sich an ihr Risiko. Dies rechtfertigt den Einsatz von dynamischen Risikomodellen (GARCH) gegenüber statischen Modellen.
  * **Volatilitätsregime**: In Phasen „hoher“ Volatilität steigt die durchschnittliche wöchentliche Rendite leicht an (1,50% vs. 0,51% in Niedrigrisiko-Phasen). Dies stützt das Konzept der **Risikoprämie**: Investoren fordern in turbulenten Zeiten höhere erwartete Renditen, um das Halten von Aktien zu rechtfertigen.

### Kapitel 2.5: Kalendereffekte & Saisonale Anomalien (Diagramm 5)
* **Visualisierung**: `05_saisonale_muster.png` vergleicht Renditen nach Monaten und testet bekannte Marktanomalien.
* **Empirischer Befund**:
  * **Monatseffekte**: Der **Januar** ist mit **1,59% wöchentlicher Rendite** (ann. ~127,5%) der mit Abstand stärkste Monat. Der **September** ist mit **0,72%** der schwächste.
  * **„Sell in May and Go Away“-Effekt**:
    * Rendite Winterhalbjahr (Nov-Apr): **1,18% pro Woche**.
    * Rendite Sommerhalbjahr (Mai-Okt): **0,92% pro Woche**.
    * **t-Statistik**: 18,34 (p-Wert = 4,03e-75).
  * **Januar-Effekt**:
    * Rendite Januar: **1,59% pro Woche**.
    * Rendite Rest des Jahres: **1,00% pro Woche**.
    * **t-Statistik**: 22,75 (p-Wert = 1,32e-114).
* **Verhaltensökonomische (Behavioral Finance) Interpretation**:
  * Beide Anomalien sind **hochgradig statistisch signifikant** (p-Werte praktisch bei Null). Dies ist ein schwerer Schlag für die **Effizienzmarkthypothese (EMH)** in ihrer schwachen Form, da historische Kalenderdaten zur Erzielung von Überrenditen genutzt werden könnten.
  * **Erklärung für den Januar-Effekt**: 
    1. *Tax-Loss Harvesting*: Investoren verkaufen im Dezember Verlustbringer, um Steuern zu optimieren, und reinvestieren das Kapital im Januar, was zu einer massiven Kaufwelle führt (insb. bei Small Caps).
    2. *Institutional Window Dressing*: Fondsmanager bereinigen ihre Portfolios vor dem Jahresende von riskanten/peinlichen Positionen und kaufen sie im Januar zurück.
  * **Erklärung für den „Sell in May“-Effekt**: Geringere Handelsvolumina im Sommer, Urlaubszeiten der institutionellen Akteure und eine generelle Risikoaversion im dritten Quartal des Jahres.

### Kapitel 2.6: Krisenanalyse & Systemische Schocks (Diagramm 6)
* **Visualisierung**: `06_krisenanalyse.png` untersucht das Verhalten des Marktes in extremen Stressphasen.
* **Empirischer Befund**:
  * **Maximaler Drawdown**: **-19,61%** (erreicht in der Woche des **16. März 2020** während des COVID-19-Ausbruchs).
  * **Schlimmste Woche**: Woche vom **09. März 2020** mit einer durchschnittlichen Rendite von **-9,74%** bei gleichzeitig extrem hoher Marktvolatilität (**26,01%**).
  * **Krisenhäufigkeit**: Nur 2,9% aller Wochen (25 von 855) weisen einen aggregierten Markteinbruch von mehr als -3% auf.
* **Ökonomische Interpretation**:
  * **Asymmetrie von Crash und Erholung**: Der COVID-Crash im März 2020 war von historischer Brutalität (Drawdown von fast 20% in wenigen Wochen im gleichgewichteten Index). Die darauffolgende Liquiditätsschwemme der Notenbanken führte jedoch zu einer der stärksten Erholungsphasen der Geschichte (COVID-19 Recovery: **+49,28% kumulierte Rendite** über 15 Wochen).
  * **Krisen-Vergleich**: Während der COVID-Crash ein extrem kurzes, hochvolatiles Ereignis war (9 Wochen, Ø Vol: 20,5%), zog sich die Ukraine-/Inflationskrise 2022 über **39 Wochen** hinweg, war jedoch von geringerer wöchentlicher Volatilität geprägt (Ø Vol: 11,09%), führte aber zu einer zähen, negativen Gesamtperformance (-6,50%).

### Kapitel 2.7: Gewinner und Verlierer des Marktes (Diagramm 7)
* **Visualisierung**: `07_top_flop_performer.png` zeigt extreme Outlier auf Ticker-Ebene.
* **Empirischer Befund**:
  * **Top-Performer ( Sharpe-Ratio-bereinigt)**: Aktien wie **FRGY** (Sharpe 4,75, Rendite 6,4e+08%), **MTEI** (Sharpe 4,65, Rendite 5,2e+10%) und **LBWR** (Sharpe 4,12).
  * **Flop-Performer**: Ticker wie **THRA** (-99,84% ann. Rendite), **WNCG** (-99,72%) und **ELIQQ** (-99,49%).
* **Methodische Einordnung für die Prüfungsleistung**:
  * **Realisierbarkeit**: Die astronomischen Renditen der Top-Performer sind mathematische Konstrukte aus dem OTC-Bereich (z. B. Penny Stocks, die von $0,0001 auf $0,05 steigen). Ein echter Investor scheitert hier an der **Liquiditätsbarriere** (hohe Geld-Brief-Spannen, mangelndes Orderbuch-Volumen).
  * **Das Gesetz der großen Zahlen**: Bei 16.322 Werten ist es statistisch zwingend, dass extreme Ausreißer existieren. 74,7% aller Ticker im Datensatz weisen über ihre Lebensdauer eine positive nominale annualisierte Rendite auf, was den generellen Aufwärtstrend des Gesamtmarktes (Drift) untermauert.

### Kapitel 2.8: Handelsvolumen, Liquidität & Markteffizienz (Diagramm 8)
* **Visualisierung**: `08_volumenanalyse.png` setzt Handelsaktivität und Kursbewegung in Beziehung.
* **Empirischer Befund**:
  * **Dominanz einzelner Tech-Giganten**: **Nvidia (NVDA)** führt das Liquiditätsranking mit einem durchschnittlichen wöchentlichen Handelsvolumen von **2,13 Milliarden Aktien** uneingeschränkt an, gefolgt von Apple (AAPL) mit **966 Millionen**.
  * **Korrelationsanalyse**: Die Pearson-Korrelation zwischen dem wöchentlichen Volumen und der wöchentlichen Rendite liegt bei **r = 0,02 (p-Wert = 0,56)**.
* **Wissenschaftliche Relevanz**:
  * **Kein direkter Volumeneffekt auf Richtungsrenditen**: Der extrem niedrige und statistisch völlig unbedeutende Korrelationskoeffizient beweist, dass hohes Handelsvolumen per se kein Prädiktor für steigende oder fallende Kurse auf Wochensicht ist.
  * Dies stützt die moderne Marktmikrostruktur-Theorie: Volumen ist ein Maß für Informationsfluss und Meinungsverschiedenheit unter Händlern (Volatilitätsfördernd), determiniert aber nicht die fundamentale Richtung des Preises.

### Kapitel 2.9: Marktinterne Korrelationen und Diversifikation (Diagramm 9)
* **Visualisierung**: `09_korrelationsanalyse.png` zeigt die Linearkombination der 30 liquidesten Aktien.
* **Empirischer Befund**:
  * **Starke Tech-Cluster**: Die höchsten Korrelationen zeigen Technologietitel untereinander:
    * **AMZN & GOOGL**: **0,579**
    * **AAPL & GOOGL**: **0,494**
    * **NVDA & PLTR**: **0,474**
    * **AAPL & NVDA**: **0,473**
* **Portfolio-Theoretische Einordnung**:
  * **Grenzen der Diversifikation**: Eine durchschnittliche positive Korrelation von knapp 0,50 unter den Top-Titeln zeigt, dass in systemischen Marktphasen (z. B. makroökonomische Zinsentscheide der Fed) ein Großteil des unsystematischen Risikos nicht wegdiversifiziert werden kann. Das verbleibende Marktrisiko (Beta) dominiert das Portfolio.

### Kapitel 2.10: Strukturelle Trends & Marktalterung (Diagramm 10)
* **Visualisierung**: `10_strukturelle_trends.png` untersucht langfristige Trends der Rendite und Volatilität über 16 Jahre.
* **Empirischer Befund**:
  * **Volatilitäts-Trend**: Die Steigung beträgt **-0,0558% pro Jahr** (R² = 0,0008, p = 0,916) → **Nicht signifikant**.
  * **Rendite-Trend**: Die Steigung beträgt **-0,044% wöchentliche Rendite pro Jahr** (R² = 0,235, p = 0,0486) → **Statistisch signifikant auf dem 5%-Niveau**.
* **Ökonomische Interpretation**:
  * **Marktalterung und Effizienzsteigerung**: Der signifikante Rückgang der durchschnittlichen Rendite über den 16-Jahres-Zeitraum (von 1,60% pro Woche in 2010 auf ca. 0,77% in 2026) deutet darauf hin, dass der Markt im Zuge der Digitalisierung, des Aufstiegs von algorithmischem Handel und verbesserter Informationsverbreitung effizienter geworden ist. Arbitrage-Möglichkeiten schrumpfen, und die historische Post-Finanzkrise-Hyperwachstumsphase hat sich normalisiert.

---

## 3. Synthese für deine Prüfungsleistung (Akademische Einordnung)

Wenn du diese Ergebnisse in deiner Prüfungsleistung präsentierst, solltest du die Brücke zu folgenden finanzwissenschaftlichen Theorien schlagen:

### 1. Die Effizienzmarkthypothese (EMH) nach Eugene Fama
* **Kernaussage**: Preise spiegeln zu jedem Zeitpunkt alle verfügbaren Informationen wider. Ein Übertreffen des Marktes ohne zusätzliches Risiko ist unmöglich.
* **Deine Argumentation auf Basis der Daten**:
  * *Widerlegung der schwachen EMH-Form*: Die extrem signifikanten Kalendereffekte (Januar-Effekt, Sell-in-May) beweisen, dass rein historische Zeitreihendaten ausreichen, um statistisch signifikante Überrenditen zu prognostizieren. Der Markt verhält sich nicht wie ein reiner „Random Walk“.
  * *Verhaltensökonomische Triebkräfte*: Diese Ineffizienzen lassen sich durch verhaltenswissenschaftliche Muster der Marktteilnehmer (Behavioral Finance) wie Herdenverhalten, steuerlich motiviertes Handeln zum Jahresende und saisonale Risikoaversion erklären.

### 2. Moderne Portfoliotheorie (MPT) nach Harry Markowitz
* **Kernaussage**: Durch die Kombination unvollkommen korrelierter Vermögenswerte kann das Gesamtrisiko des Portfolios unter das gewichtete Risiko der Einzelwerte gesenkt werden.
* **Deine Argumentation auf Basis der Daten**:
  * Die positive Korrelation der Liquiditätsführer (z. B. AMZN-GOOGL: 0,58) zeigt die Grenzen nationaler Diversifikation innerhalb eines Sektors. Für ein wirklich effizientes Portfolio müssen Asset-Klassen oder geografische Regionen beigemischt werden, die geringere Korrelationen aufweisen.

### 3. Modellierung von Extremrisiken (Fat Tails)
* **Kernaussage**: Finanzdaten sind nicht normalverteilt. Extreme Risiken werden in Standardmodellen massiv unterschätzt.
* **Deine Argumentation auf Basis der Daten**:
  * Mit einer Kurtosis von 121,24 liefert dieser Datensatz den ultimativen empirischen Beweis für die Existenz von „Fat Tails“ und extremen Krisenereignissen (wie dem COVID-Crash im März 2020).
  * Du kannst vorschlagen, dass Risikomanager statt einfacher Standardabweichungen fortgeschrittenere Methoden wie den **Expected Shortfall (ES)** oder **GARCH-Modelle mit Student-t-Verteilung** anwenden sollten, um das Risiko im linken Schwanz der Verteilung (Extreme Verluste) adäquat abzubilden.

### 4. Die Small-Firm-Anomalie
* **Kernaussage**: Small Caps schlagen Large Caps im langfristigen Durchschnitt.
* **Deine Argumentation auf Basis der Daten**:
  * Der immense Unterschied zwischen der Performance eines gleichgewichteten Gesamtmarktindexes (79,47% p.a. über alle 16.322 Aktien) und klassischen kapitalgewichteten Indizes ist die direkte Manifestation des Small-Firm-Effekts. Es zeigt jedoch auch die methodische Einschränkung gleichgewichteter akademischer Backtests auf, da die Liquidität in der Praxis ein limitierender Faktor ist.

---

*Dieses Dokument wurde als wissenschaftliche Begleitung zur automatisierten Datenanalyse erstellt und dient als konzeptionelles Fundament für deine schriftliche Prüfungsleistung.*
