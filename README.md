# CanvasCourseScaffolder
This is a Python script which can be run to scaffold a Canvas course. Instructions on how to use can be found below.

:warning: *This script might delete existing content in your course. Please make sure you are aware of this before running the script.*

:information_source: *For more information, contact me at [joren.synaeve@thomasmore.be](mailto:joren.synaeve@thomasmore.be).*

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

#### Bestanden die nodig zijn en als template gebruikt worden
- `afbeeldingen/banner_TM.png` is de banner die onderaan de cursuspagina komt te staan.
- `paginas/leerdoelen.html` is de pagina met de leerdoelen. Deze wordt toegevoegd aan de studiewijzer.
- `paginas/planning.html` is de pagina met de planning. Deze wordt toegevoegd aan de studiewijzer.
- `paginas/feedback_en_begeleiding.html` is de pagina met de feedback en begeleiding. Deze wordt toegevoegd aan de studiewijzer.
- `paginas/toetsing.html` is de pagina met de toetsing. Deze wordt toegevoegd aan de studiewijzer.
- `paginas/studiemateriaal.html` is de pagina met het studiemateriaal. Deze wordt toegevoegd aan de studiewijzer.
- `paginas/startpagina.html` is de startpagina van de cursus. Deze pagina is de homepage van de cursus.


## Gebruik
1. Download de repository
2. Voorzie de mappenstructuur van de nodige bestanden
3. Open een terminal in de map van de repository
4. Voer het volgende commando uit: `python index.py`
5. Volg de instructies in de terminal
