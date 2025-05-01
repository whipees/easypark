## EASYPARK

**Systém detekce a ověřování registračních značek vozidel pomocí kamery a Raspberry Pi**  

**Autor:** Sebastian Janíček  
**Studijní obor:** C  

---

## Anotace

Tato práce popisuje návrh, vývoj a testování systému pro detekci registrační značky (SPZ) vozidel pomocí kamery připojené k platformě Raspberry Pi 4. Po ověření platnosti SPZ se aktivuje externí LED dioda připojená přes Raspberry Pi Pico. Cílem projektu je vytvořit jednoduché, modulární a snadno opakovatelné řešení pro identifikaci a signalizaci platných SPZ.

---

## Úvod

V současné době roste poptávka po autonomních systémech pro monitorování dopravy a automatizovanou kontrolu přístupu na parkoviště či do uzavřených areálů. Tento projekt si klade za cíl vytvořit cenově dostupné a přehledné řešení založené na otevřeném hardwaru a softwaru.

Systém využívá Raspberry Pi 4 pro zpracování obrazu a detekci SPZ pomocí knihovny OpenCV a OCR (Optical Character Recognition). V případě úspěšného rozpoznání a ověření platnosti SPZ dojde k odeslání signálu přes sériovou linku na Raspberry Pi Pico, která následně rozsvítí připojenou LED diodu.

Práce je rozdělena do několika hlavních částí:

1. Konkurenceschopnost a ekonomické zhodnocení  
2. Popis architektury a technologií  
3. Vývoj a dokumentace kódu  
4. Testování  
5. Nasazení  
6. Závěrečné zhodnocení  

---

## Ekonomická rozvaha

### Analýza konkurence

- Komerční řešení pro automatickou detekci SPZ často stojí desítky tisíc korun a vyžadují licencované softwarové moduly.  
- Otevřená řešení existují, ale většinou nejsou plně integrovaná nebo vyžadují složitou konfiguraci.  

### Výhody našeho projektu

- Nízká cena (do 6 000 Kč za hardware)  
- Jednoduchá instalace  
- Využití otevřeného softwaru (OpenCV, Tesseract) bez licenčních poplatků  

### Způsob propagace

- GitHub repozitář s dokumentací a ukázkovými daty  
- Prezentace na školních konferencích a workshopech  
- Příspěvek do odborných časopisů o automatizaci  

### Návratnost investic

- Hardware lze využít pro více aplikací (vstupní systémy, parkoviště, statické kamery)  
- Škálovatelnost: nasazení více jednotek přinese úspory z rozsahu  

---

## Vývoj

### Použité technologie

- **Raspberry Pi 4:** zpracování obrazu, hlavní řídicí jednotka  
- **Raspberry Pi Pico:** signalizace LED diody  
- **Python 3:** hlavní jazyk  
- **OpenCV:** detekce oblastí SPZ  
- **Tesseract OCR:** převod obrazu na text  
- **pyserial:** komunikace mezi Pi 4 a Pico  

### Architektura a členění kódu

- **Main_pi.py:** inicializace kamery, smyčka čtení snímků, detekce SPZ  
- **Main.py (v raspi pico):** obsluha signálu a aktivace LED diody  

### Průběh vývoje

1. Inicializace prostředí a testovací skripty  
2. Implementace detekce SPZ v OpenCV  
3. Integrace Tesseract OCR s předzpracováním obrazu  
4. Nastavení sériové komunikace a vývoj kódu pro Pico  
5. Debugging a optimalizace výkonu  

---

## Testování

### Testovací scénáře

1. **Detekce čitelné SPZ za denního světla**  
   - Očekávaný výsledek: úspěšné rozpoznání  
2. **Detekce SPZ za slabého osvětlení**  
   - Očekávaný výsledek: částečně čitelný text, nižší přesnost  
3. **Falešné SPZ (neexistující formát)**  
   - Očekávaný výsledek: validace zamítne  
4. **Špinavá SPZ**  
   - Očekávaný výsledek: rozpoznání s nižší spolehlivostí  
5. **Spuštění nasazení**  
   - Očekávaný výsledek: systém spuštěn jako služba, po bootu OS se automaticky spustí skript  

### Výsledky testů

- Scénář 1: 98 % úspěšnost  
- Scénář 2: 65 % úspěšnost  
- Scénář 3: 100 % (správné zamítnutí)  
- Scénář 4: 60 % (doporučeno lepší kameru)  
- Scénář 5: bez chybových hlášení, LED se aktivuje  

---

## Nasazení a spuštění

1. Nainstalujte OS Raspberry Pi OS na SD kartu  
2. Připojte kameru a Pico přes USB  
3. Nainstalujte Python 3, OpenCV, pytesseract, pyserial  
4. Upravte konfiguraci v `config.json` (cesta k Tesseractu, sériový port)  
5. Přidejte `main.py` do autostartu (systemd nebo cron)  
6. Restartujte zařízení  

**Požadavky:**  
- Kamera kompatibilní s Raspberry Pi  
- Tesseract nainstalovaný v systému  
- Raspberry Pi Pico s nahraným firmwarem  

---

## Licence

Projekt je licencován pod licencí MIT. Viz soubor `LICENSE`.  

---

## Odkaz na GIT

[https://github.com/whipees/easypark](https://github.com/whipees/easypark)  

---

## Závěr

V práci byl úspěšně implementován modulární systém pro detekci a signalizaci platných SPZ. Projekt prokázal vysokou spolehlivost za ideálních podmínek a ukázal oblasti pro další vylepšení, zejména v oblasti osvětlení a rychlosti detekce. Díky otevřenému přístupu je systém snadno rozšiřitelný a adaptovatelný pro různé scénáře.  
