from django.core.management.base import BaseCommand
from app.models import Car, Listing, Image
import requests
from bs4 import BeautifulSoup
import csv
import re
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


class Command(BaseCommand):
    help = 'Scrape car data and insert into database'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('url', type=str, help='URL of make page')
        parser.add_argument('make', type=str, help='Make of the car')


    def handle(self, *args, **options):
        
        #url = "https://www.ss.com/lv/transport/cars/audi/"
        self.url = options['url']
        self.make = options['make']
        all_car_data = self.run_scraper(self.url)  # Make sure run_scraper returns a list of car data
        
        for car_data in all_car_data:
            self.insert_into_database(car_data)
            
        print("Done!")


    def insert_into_database(self, car_data):
        # Create a new Car object
        car = Car(
            Make=self.make,
            Model=car_data['model'] if car_data['model'] is not None else "None",  # Default value of "None" if model is None
            Year=car_data['year'] if car_data['year'] is not None else 0,  # Default value of 0 if year is None
            Fuel=car_data['fuel'] if car_data['fuel'] is not None else "None",  # Default value of "None" if fuel is None
            Engine_cc=car_data['displacement'] if car_data['displacement'] is not None else 0,  # Default value of 0 if displacement is None
            Gearbox=car_data['gearbox'] if car_data['gearbox'] is not None else "None",  # Default value of "None" if gearbox is None
            Color=car_data['color'] if car_data['color'] is not None else "None"  # Default value of "None" if color is None
        )
        car.save()  # Insert the car into the database

        # Create a new Listing object
        listing = Listing(
            Car=car,
            Price=car_data['price'] if car_data['price'] is not None else 0,  # Default value of 0 if price is None
            Mileage=car_data['mileage'] if car_data['mileage'] is not None else 0,  # Default value of 0 if mileage is None
            Location="None",  # Replace this with actual location data
            Description="None",  # Replace this with actual description
            Phone="None",  # Replace this with actual phone
            Email="None",  # Replace this with actual email
            Name="None",  # Replace this with actual name
            Link=car_data['link'] if car_data['link'] is not None else "http://ss.com/"  # Default value of "None" if link is None
        )
        listing.save()  # Insert the listing into the database
        
        if car_data['image_src']:  # Check if 'image_src' is not None
            response = requests.get(car_data['image_src'], stream=True)
            if response.status_code == 200:
                image_name = car_data['image_src'].split('/')[-1]
                image_path = default_storage.save('listing_images/' + image_name, ContentFile(response.content))

                # Create a new Image object
                image = Image(
                    listing=listing,
                    image=image_path  # ImageField takes the path of the image relative to the media folder
                )
                image.save()  # Insert the image into the database

    def get_car_data(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        car_data = {}

        car_data["link"] = url
        model = soup.find("td", {"id": "tdo_31"})
        car_data["model"] = model.text.replace(self.make, "") if model else None
        
        year = soup.find("td", {"id": "tdo_18"})
        car_data["year"] = year.text[:4] if year else None

        engine = soup.find("td", {"id": "tdo_15"})
        if engine:
            car_data["displacement"] = int(float(engine.text.split()[0])*1000)
            car_data["fuel"] = engine.text.split()[1]
        else:
            car_data["displacement"] = None
            car_data["fuel"] = None

        mileage = soup.find("td", {"id": "tdo_16"})
        car_data["mileage"] = int(mileage.text.replace(" ", "")) if mileage else None

        color = soup.find("td", {"id": "tdo_17"})
        car_data["color"] = color.text.split()[0] if color else None

        gearbox = soup.find("td", {"id": "tdo_35"})
        car_data["gearbox"] = gearbox.text.split()[0] if gearbox else None

        price = soup.find("span", {"id": "tdo_8"})
        car_data["price"] = int(price.text.replace(" ", "").replace("€", "")) if price else None

        image = soup.find("img", {"class": "pic_thumbnail isfoto"})
        if image and image.parent.name == 'a':
            car_data["image_src"] = image.parent.get('href')
        else:
            car_data["image_src"] = None

        return car_data

    def run_scraper(self, url):
        make_site = requests.get(url)
        soup_make = BeautifulSoup(make_site.text, 'html.parser')
        pattern = re.compile(r'^tr_\d+$')
        tr_elements = soup_make.find_all('tr', id=pattern)
        
        car_data_list = []
        for tr in tr_elements:
            a_element = tr.find('a')
            if a_element:
                href = a_element['href']
                full_link = f"http://www.ss.lv{href}"
                car_data = self.get_car_data(full_link)
                car_data_list.append(car_data)
            else:
                print("No <a> element found within the <tr> element")
        return car_data_list
