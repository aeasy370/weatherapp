# weatherapp
GUI weatherapp using PyQt5 and several various web APIs to display information to the user

We are Running python version 3.9.7. 
We are Running Pip version pip 21.2.4. 
Need to pip intall (requests) (geocoder) (geopy) and (pyspellchecker) 

You are able to run the app of two ways. 
- 1st is to use this command "python .\main.py"
- 2nd is to hit the run button on vscode when in the mainfile

ALL that needs to be done to run it to hit the Run without debugging button. 
Once the Window pops up asking or the location, Type the city name without the state. If you want to type the state name you have to spell it fully out. (Knoxville) or (Knoxville, Tennessee). A zip code with the country initals will also work. (37914, US). Then you can hit the submit button or press enter on the keyboard. Mkae sure the city is spelled correctly because at the moment it does not reask because of a widget issue. The refresh button will re run the api call and update to the most current data.

To change the Temperature from F to C, hit the button on the top left named acoordingly.

To change back and forth from Darkmode, hit the button on the top Right named acoordingly.
