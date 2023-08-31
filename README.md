# CanvasCourseScaffolder
This is a Python script which can be run to scaffold a Canvas course. Instructions on how to use can be found below.

:warning: *This script might delete existing content in your course. Please make sure you are aware of this before running the script.*

## Vereisten
- Enige kennis van Python
- Enige kennis van HTML en CSS
- Een Canvas API token (zie verder)

### Een Canvas API token aanmaken
1. Ga naar Canvas en log in
2. Klik op Account > Instellingen
3. Scroll naar beneden tot je bij **Goedgekeurde integraties** komt
4. Klik op **Nieuw toegangstoken**
5. Geef het token een naam (doel) en klik op **Toegangstoken genereren**
6. Kopieer het token en bewaar het op een veilige plaats

Een voorbeeld van een token ziet er als volgt uit: `13183~cnTzlTlJlQfd3CQOYkfKPKu933hu2p9LQmFqKjdbYTvOEaiY9Rt6WjyQMEOS0gTG`.

### Excel bestand en mappenstructuur
Het script verwacht een Excel bestand met de naam `config.xlsx` in een map naar keuze. De mappenstructuur ziet er daarna als volgt uit:

```
data
├── config.xlsx
├── afbeeldingen
│   ├── image1.png
│   ├── ...
├── bestanden
│   ├── voorbeeld.txt
│   ├── ...
├── opdrachten
│   ├── opdrachtbeschrijving.html
│   ├── ...
├── paginas
│   ├── leerdoelen.html
│   ├── ...
```

## Gebruik
1. Download de repository
2. Voorzie de mappenstructuur van de nodige bestanden
3. Open een terminal in de map van de repository
4. Voer het volgende commando uit: `python index.py`
5. Volg de instructies in de terminal