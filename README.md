# Hackdata2017_Backend

This repo contains the code for the backend of an Android application, **Contexa**: Our working prototype put together during *HackData 2017.* Contains code for the flask server talking to the android app and the external APIs we used. 

A combination of the following APIs has been used to facilitate text extraction and classification from images:

- [Microsoft's LUIS platform](https://www.luis.ai/): For classifying the extracted text based on the needs of the user (dates, contacts, etc.)
- [Google Cloud Vision API](https://cloud.google.com/vision/): For actually extracting the text from the image.
 
### Refer to https://github.com/starship9/Hackdata2017 for the details of the entire project, as well as the Android frontend. 
