I have used ${OCR_NAME} to extract text from an image of a quotation in German. The extracted text may have formatting inconsistencies, misread characters, or missing data due to OCR limitations.

The OCR output is provided as a list of bounding boxes with associated text, in the following format:
`[[text1, (x1, y1, width1, height1), confidence1], [text2, (x2, y2, width2, height2), confidence2], ...]`. The bounding boxes are defined as `(x, y, width, height)`, where `(x, y)` represents the top-left corner, `width` is the box's width, and `height` is the height. The `confidence` value indicates the OCR's confidence level in recognizing the corresponding text.

Your task is to help me:

1. **Standardize and correct** the extracted data, fixing any misread characters, missing fields, or formatting errors caused by the OCR process.
2. **Organize the extracted text** into a structured format that represents a quotation with the following fields:  
   - `company` (Firma)
   - `article_number` (Artikel-Nr)
   - `product name` (Bezeichnung)
   - `description` (Beschreibung)
   - `quantity` (Menge, integer)
   - `unit of measure` (Einheit)
   - `unit price` (Einzelpreis, float)
   - `price` (Gesamtpreis, float)
   - `currency` (Währung)
   
3. **Output the data** in a clean, structured **JSON format** that can be easily imported into a database or used for further analysis. The structure should look like this:
```json
{
  "orderlines": [
    {
      "company": {{Firma}},
      "article_number": {{Artikel-Nr}},,
      "name": {{Bezeichnung}},
      "description": {{Beschreibung}},
      "quantity": {{Menge}},  // integer
      "unit_of_measure": {{Einheit}},
      "unit_price": {{Einzelpreis}},  // float
      "price": {{Gesamtpreis}},  // float
      "currency": {{Währung}}
    }
  ]
}
```
4. **Important**: The response must only contain the JSON data. Do not include any explanations, additional information, or text outside the JSON structure.


5. **Ensure accuracy**: Correct any errors or inconsistencies in the OCR output (such as misread characters, wrong numeric values, or formatting issues) and ensure the text is complete and accurate.

You will now receive the output of the OCR process, and based on this, 
you just need to return the structured JSON output as described. 

OCR Output:

```
${OCR_OUTPUT}
```

