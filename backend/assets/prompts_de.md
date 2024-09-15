Ich habe ${OCR_NAME} verwendet, um Text aus einem Bild eines Angebots auf Deutsch zu extrahieren. Der extrahierte Text kann aufgrund von OCR-Beschränkungen Formatierungsinkonsistenzen, falsch erkannte Zeichen oder fehlende Daten enthalten.

Das OCR-Ergebnis wird als Textdatei bereitgestellt.

Deine Aufgabe ist es:

1. **Standardisiere und korrigiere** die extrahierten Daten, behebe falsch erkannte Zeichen, fehlende Felder oder durch den OCR-Prozess verursachte Formatierungsfehler.
2. **Organisiere den extrahierten Text** in ein strukturiertes Format, das ein Angebot mit den folgenden Feldern darstellt:  
   - `company` (Firma)
   - `article_number` (Artikel-Nr)
   - `product name` (Bezeichnung)
   - `description` (Beschreibung)
   - `quantity` (Menge, Ganzzahl, standardmäßig 1)
   - `unit of measure` (Einheit)
   - `unit price` (Einzelpreis, Kommazahl)
   - `discount` (Rabatt %, Kommazahl, standardmäßig 0)
   - `price` (Gesamtpreis, Kommazahl)
   - `currency` (Währung)
   
   Es ist wichtig, die Formel zu beachten, um den Preis zu berechnen: `price = unit_price * quantity * (1 - discount / 100)`.

3. **Gib die Daten** in einem sauberen, strukturierten **JSON-Format** aus, das leicht in eine Datenbank importiert oder zur weiteren Analyse verwendet werden kann. Die Struktur sollte folgendermaßen aussehen:
```json
{
  "orderlines": [
    {
      "company": {{Firma}},
      "article_number": {{Artikel-Nr}},
      "name": {{Bezeichnung}},
      "description": {{Beschreibung}},
      "quantity": {{Menge}},  // Ganzzahl, standardmäßig 1
      "unit_of_measure": {{Einheit}},
      "unit_price": {{Einzelpreis}},  // Kommazahl
      "discount": {{Rabatt_in_Prozent}},  // Kommazahl, standardmäßig 0
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

```text
${OCR_OUTPUT}
```