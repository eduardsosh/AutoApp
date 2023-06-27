# Installing and running

### Prerequisites

-Latest python <br>
-Git <br>


### Running

-Clone repo <br>
-Create a venv in `\AutoApp` using `python -m venv .`<br>
-Run venv using `\Scripts\activate.bat` <br>
-Run `pip install -r requirments.txt` <br>

###### We now have all the files 
In `AutoApp\autosite\` run `python manage.py --migrate`

###### Now run server
In `\AutoApp\autosite` run `python manage.py --runserver`
<br>
<br>
### Populating the database
Running `python manage.py your_command` will populate the database <br>
with the first page of vehicles and their thumbnail images in the set make of the vehicle.
