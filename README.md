        http://chriswhong.com/open-data/foil_nyc_taxi/
        http://www.andresmh.com/nyctaxitrips/
        https://pypi.python.org/pypi/geopy
        Mapping: Basemap, http://matplotlib.org/basemap

        Overarching To do:

        1. Sift through data using python. Each cell should be a item in a list. 
        2. Find a way to bin each record of taxi rides to a specific place in NYC
        	Bin types:	uptown/midtown/downtown
        			neighborhoods
	        		upper east/upper west/lower west/lower east/etc...
		        	longitudinal/latitudinal bins (just based on long/lat)
        3. Generate a table based on this information, i.e.     
        	Start location/end location - bins
        	Price - price
        	etc...
        4. Build a graph based on the table
        	Graph type: correlations, something else, something else...

	Alternatives:
	A) Examine tip data to find highest and lowest tipped areas of manhattan/NY
	
	
-------------------------
main.py
-------------------------
usage:
		python main.py -f <farefile.csv> -t <tripfile.csv> [--firstpass] [--secondpass] [--finalpass]
		* please use either firstpass, secondpass, or finalpass
		* the farefile and tripfiles are required (although it isn't enforced. I should change that)
	
--firstpass:
	What should happen is this:
		1. open both farefile and tripfile
		2. read both files at the same time (line by line)
		3. parse the line as an array (split(','))
		4. take the lat/long (in that order) from the TRIPFILE and use geopy to geolocate address
			4.i. this is in a TRY because there is a good chance geopy will timeout (15 second timeout)
			4.ii. IN WHICH CASE: the EXCEPT clause will put this this line number into a separate file called 'excludedlines.txt'
		5. concat tripfile and farefile line then append the geolocation address (pickup & dropoff respectively)
		6. It will loop over the whole file, writing into 'excludedlines.txt' and 'rawoutput.csv'.
	



