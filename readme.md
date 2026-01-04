# 🚀 Windows Installer saatavilla!

> [!NOTE]
> Ohjelmasta on julkaistu ensimmäinen Windows-asennuspaketti helpottamaan käyttöönottoa.

Voit ladata valmiin asennustiedoston suoraan tästä:
**[📥 SIEM PRO BETA v1.0.0-beta](https://github.com/kvScepter/Poor-mans-SIEM-for-WIN11/releases/tag/v1.0.0-beta)**

---


# 🛡️ SIEM Ultimate Dashboard v4.5

**SIEM Ultimate Dashboard** on kevyt ja moderni tietoturvan hallintatyökalu (Security Information and Event Management), joka on suunniteltu Windows-ympäristön reaaliaikaiseen valvontaan. Sovellus yhdistää lokien seurannan ja verkkoanalyysin yksinkertaiseen käyttöliittymään. 
---

## 🚀 Ominaisuudet

- **📊 Reaaliaikainen Event Log**: Seuraa prosessien käynnistyksiä (Event ID 4688) ja kirjautumisyrityksiä.[2]
- **📡 Network Monitor**: Tunnistaa ulospäin suuntautuvan liikenteen kohteet ja tarkistaa IP-osoitteiden maineen.[3]
- **🔍 Win+R Forensics**: Lukee Windowsin Run-ikkunan komentohistorian suoraan rekisteristä.[4]
- **👤 Käyttäjätunnistus**: Erottelee automaattisesti käyttäjän manuaaliset toiminnot (`[KÄYTTÄJÄ]`) järjestelmäprosesseista.[2]
- **⚙️ Dynaaminen Whitelist**: Hallitse ohitettavia ohjelmia suoraan GUI:sta ilman koodin muokkausta.
- **🌙 Moderni Dark Mode**: Rakennettu CustomTkinterillä Windows 11 -tyyliin.[1]

---

## 🛠️ Asennus

### 1. Esivaatimukset
- **Python 3.10+**
- **Administrator-oikeudet** (pakollinen lokien lukemiseen).[5]

### 2. Kirjastojen asennus
Aja seuraava komento virtuaaliympäristössäsi:

```bash
pip install customtkinter psutil requests pywin32
```

### 3. Windows-auditointiasetukset
Jotta sovellus näkee ohjelmien komentorivitiedot, toimi näin:

1. Paina **Win + R**, kirjoita `gpedit.msc` ja paina Enter.
2. Navigoi: **Tietokoneasetukset > Hallintamallit > Järjestelmä > Audit Process Creation**.
3. Aseta **Include command line in process creation events** tilaan **Enabled**.

> **Vaihtoehtoisesti (Windows Home):** Aja rekisterikomento järjestelmänvalvojana:
> ```powershell
> reg add "hklm\software\microsoft\windows\currentversion\policies\system\audit" /v ProcessCreationIncludeCmdLine_Enabled /t REG_DWORD /d 1 /f
> ```

## 🖥️ Käyttöohje

Käynnistä sovellus ajamalla päävalikko:

```bash
python gui_main.py
```
---

### Välilehtien toiminta:

* **📊 Event Log**: Näyttää live-virran järjestelmän tapahtumista. Sisältää tarkat aikaleimat, ohjelman kuvaukset ja komentorivit.
* **📡 Network Traffic**: Listaa verkkoyhteydet. Hälyttää punaisella, jos liikenne suuntautuu `config.json`-tiedostossa blokattuihin maihin.
* **🔍 Forensics**: "Scan Run History" -painike hakee viimeisimmät Win+R ikkunaan kirjoitetut komennot.
* **⚙️ Settings**: Lisää tästä uusia ohjelmia (esim. `spotify.exe`) Whitelist-listalle, jolloin niistä ei tule turhia ilmoituksia.

### 📂 Projektin rakenne


* **`gui_main.py`**: Sovelluksen moderni käyttöliittymä ja päälogiikka.
* **`log_monitor.py`**: Windows-tapahtumalokien reaaliaikainen seuraaja.
* **`network_monitor.py`**: Verkkoyhteyksien ja IP-maineen valvonta.
* **`metadata_helper.py`**: Hakee ohjelmien valmistajatiedot ja kuvaukset EXE-tiedostoista.
* **`config.json`**: Hallitsee asetuksia, kuten blokatut maat ja whitelistit.


## ⚠️ Vastuuvapauslauseke

Tämä työkalu on kehitetty harrastus- ja oppimiskäyttöön. Käyttäjä on yksin vastuussa ohjelmiston käytöstä ja sen vaikutuksista tietokoneen tietoturvaan ja suorituskykyyn.

---
**SIEM Ultimate - Projekti Tammikuu 2026**
