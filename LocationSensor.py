

class LocationSample:
    def __init__(self, lat_degrees: float, lon_degrees: float, alt_meters: float, time_utc_seconds: float):
        """A container representing a reading from a LocationSensor.
        Encodes position and time.

        :param lat_degrees: Latitude of the reading in degrees. Positive is East
        :param lon_degrees: Longitude of the reading in degrees. Positive is North
        :param alt_meters: Altitude of the reading in meters.
        :param time_utc_seconds: Time of the reading in seconds since the linux epoch.
        """
        self.lat_degrees = lat_degrees
        self.lon_degrees = lon_degrees
        self.alt_meters = alt_meters
        self.time_utc_seconds = time_utc_seconds


class LocationSensor:
    def __init__(self, sensor_read_path='Data/sensorinput.csv'):
        """This class simulates a sensor that reads location per time.
        Note: Do not modify the contents of this class.
        """
        self.__file = open(sensor_read_path, newline='')
    
    def __del__(self):
        self.__file.close()

    def read_location(self) -> LocationSample | None:
        """This method "reads" from the location sensor. On each invocation,
        this method will return the next reading from the sensor, with a new timestamp.
        If no valid reading is availble, this will return None.
        
        Note that while this method returns timestamps, they are not correlated with 
        the real times that the method is called, rather they are predetermined samples
        that are read in order (don't worry about actual timing of calling this function, just 
        invoke it to get multiple samples).
        """

        try: 
            row = self.__file.readline()
            row_list = row.split(',')
            lat_deg = float(row_list[0])
            lon_deg = float(row_list[1])
            alt_meters = float(row_list[2])
            time_utc_seconds = float(row_list[3])

            reading = LocationSample(lat_deg, lon_deg, alt_meters, time_utc_seconds)

            return reading

        except:
            return None
