Ich habe ${OCR_NAME} verwendet, um Text aus einem Bild eines Angebots auf Deutsch zu extrahieren. Der extrahierte Text kann aufgrund von OCR-Beschränkungen Formatierungsinkonsistenzen, falsch erkannte Zeichen oder fehlende Daten enthalten.

Das OCR-Ergebnis wird als eine Liste von Begrenzungsrahmen mit zugehörigem Text im folgenden Format bereitgestellt:
`[[text1, (x1, y1, width1, height1), confidence1], [text2, (x2, y2, width2, height2), confidence2], ...]`. Die Begrenzungsrahmen sind definiert als `(x, y, width, height)`, wobei `(x, y)` die Koordinaten der oberen linken Ecke darstellen, `width` die Breite und `height` die Höhe des Rahmens ist. Der `confidence`-Wert gibt das Vertrauen der OCR-Erkennung in den erkannten Text an.

Deine Aufgabe ist es:

1. **Standardisiere und korrigiere** die extrahierten Daten, behebe falsch erkannte Zeichen, fehlende Felder oder durch den OCR-Prozess verursachte Formatierungsfehler.
2. **Organisiere den extrahierten Text** in ein strukturiertes Format, das ein Angebot mit den folgenden Feldern darstellt:  
   - `company` (Firma)
   - `article_number` (Artikel-Nr)
   - `product name` (Bezeichnung)
   - `description` (Beschreibung)
   - `quantity` (Menge, Ganzzahl)
   - `unit of measure` (Einheit)
   - `unit price` (Einzelpreis, Kommazahl)
   - `price` (Gesamtpreis, Kommazahl)
   - `currency` (Währung)
   
3. **Gib die Daten** in einem sauberen, strukturierten **JSON-Format** aus, das leicht in eine Datenbank importiert oder zur weiteren Analyse verwendet werden kann. Die Struktur sollte folgendermaßen aussehen:
```json
{
  "orderlines": [
    {
      "company": {{Firma}},
      "article_number": {{Artikel-Nr}},
      "name": {{Bezeichnung}},
      "description": {{Beschreibung}},
      "quantity": {{Menge}},  // Ganzzahl
      "unit_of_measure": {{Einheit}},
      "unit_price": {{Einzelpreis}},  // Kommazahl
      "price": {{Gesamtpreis}},  // Kommazahl
      "currency": {{Währung}}
    }
  ]
}
```
4. **Wichtig**: Die Antwort darf nur die JSON-Daten enthalten. Füge keine Erklärungen, zusätzlichen Informationen oder Text außerhalb der JSON-Struktur hinzu.

5. **Stelle die Genauigkeit sicher**: Korrigiere alle Fehler oder Ungenauigkeiten im OCR-Ergebnis (z. B. falsch erkannte Zeichen, falsche Zahlenwerte oder Formatierungsfehler) und stelle sicher, dass der Text vollständig und korrekt ist.

Du erhältst jetzt das OCR-Ergebnis, und basierend darauf musst du das beschriebene, strukturierte JSON-Ergebnis liefern.

OCR-Ergebnis:

```
${OCR_OUTPUT}
```
