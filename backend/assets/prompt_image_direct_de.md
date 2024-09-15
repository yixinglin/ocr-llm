I have a set of images that contain German quotations captured via mobile phone. 
Your task is to extract key information from these images and convert it into 
a structured JSON format. The information on the images is written in German, 
and it includes the following fields:

1. **company** (Firma)
2. **article_number** (Artikel-Nr)
3. **product name** (Bezeichnung)
4. **description** (Beschreibung)
5. **quantity** (Menge, integer, default to 1 if not provided)
6. **unit of measure** (Einheit)
7. **unit price** (Einzelpreis, float)
8. **discount** (Rabatt %, float, default to 0 if not provided)
9. **price** (Gesamtpreis, float)
10. **currency** (Währung)

For each quotation in the image, I need you to extract this data and 
convert it into JSON format. The JSON structure should look like this:

```json
{
    "orderlines": [
        {
        "company": "Company name",
        "article_number": "123456",
        "product_name": "Product name",
        "description": "Description of the product",
        "quantity": 10,
        "unit_of_measure": "Unit type (e.g., kg, ml, etc.)",
        "unit_price": 12.50,
        "discount": 5.0,
        "price": 118.75,
        "currency": "EUR"
        }
    ]
}
```

If any information is missing, you should leave that field blank, except for the **discount** field, which defaults to 0. Additionally, ensure that all numbers are extracted as numerical data types (integers for quantities and floats for prices).

Please process the image accordingly and return the extracted data in the structured format as described.
