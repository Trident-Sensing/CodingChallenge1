# Author: Colin Pollard
# Date Created: 4/29/2023
# Copyright: Trident Sensing LLC. (colin.pollard@tridentsensing.com)

from LocationSensor import LocationSensor, LocationSample
import numpy as np
import math

''' 
Welcome to the first attempt at a technical interview question for prospective TS engineers!

- This interview asks you to implement the class below. You do not need to, and shouldn't modify any files other than this one.
- There are unit tests which will evaluate your implementation. Try not to look at the unit test files unless you need a hint.
  Please do use the names of the unit tests to intuit what about your implementation might be incorrect.
- Feel free to use any tools you normally would while coding. Google is great.
- Using libraries is encouraged. We utilized numpy extensively in our implementation.

Leaderboard:
Colin Pollard: 16:57, 12:19, ~13:01, ~5:02
'''

class ModeledLocationSensor:
    def __init__(self, max_samples: int=15, sensor_read_path='Data/sensorinput.csv'):
        """
        Motivation: 
        Let's say that you have a sensor that reads position per time. Because you are
        reading from a real-world data source, you do not have precise timing control over
        data acquisition, and must correct this prior to providing data to the rest of the 
        project. To accomplish this task, you have been asked to create a layer that handles
        the messy timing of the sensor, and provides a nicer interface to your coworkers
        who inevitably will think that this was all functionality built into the sensor,
        and then complain that you haven't done any actual work.

        Requirements and Hints:
        - For this implementation, you will want to create an instance of the LocationSensor class,
        already imported above. Be sure to read the read_location method's documentation.
        - Each of the methods of this class will be called multiple times, do not recreate the
        LocationSensor instance to handle this.
        - Assume that the sensor goes offline after max_samples invocations. 

        :param max_samples: _description_
        :type max_samples: _type_
        """
        self.__max_samples = max_samples
        self.__ls = LocationSensor(sensor_read_path=sensor_read_path)
        self.__sample_buffer: list(LocationSample | None) = []
        self.__timestamp_buffer: list(float) = []

        for i in range(max_samples):
            sample = self.__ls.read_location()
            self.__sample_buffer.append(sample)

            if sample is None:
                self.__timestamp_buffer.append(np.inf)
            else:
                self.__timestamp_buffer.append(sample.time_utc_seconds)
        
        self.__timestamp_buffer = np.array(self.__timestamp_buffer)

    def get_nearest_sample(self, timestamp: float) -> LocationSample | None:
        """
        Motivation: 
        The team has decided to implement a new feature on the frontend that shows
        the location history of the sensor, based on a user-input slider that selects a timestamp to view.
        They consult you about their new feature and ask for a method that "gives them the location."
        You tell them that the sensor does not output a value for every possible time, and suggest that 
        they could display to the user the available sensor readings and allow the user to select one
        of those times to display. They promptly ignore the suggestion, citing the woes of angularjs. 
        As you start to suggest a way of outputting smooth values, your coworkers think that all of that
        fancy math would take too long to implement, and they just need something that will work for now.
        
        This method gets the closest valid sample to the requested timestamp and returns it.
        If there is no valid sample to retrieve, this method returns None.

        :param timestamp: Requested timestamp of the sample.
        :return: A LocationSample at the closest sensor reading to the requested timestamp.
        """
        time_distances = np.subtract(self.__timestamp_buffer, timestamp)
        index = np.argmin(np.abs(time_distances))
        return self.__sample_buffer[index]

    def get_estimated_sample(self, timestamp: float) -> LocationSample | None:
        """
        Motivation:
        With the new nearest sample method implemented, the frontend team has a functional new widget.
        As they begin to slide the time selector around, the position of the sensor jumps from point to point,
        occasionally waiting at one spot for a long pause, and then jumping a football field to catch back up.
        Your boss walks in, eyes the new widget, and on their way out says: "Needs to be smoother."

        The frontend guys couldn't possibly muddle their pristine codebase with backend concerns, and volun-tell
        you to help out with making the slider better to use. They also inform you that figuring out when the
        sensor came online or went offline was too much to fit into this week's sprint, and that the function
        you write must be able to handle timestamps outside of the range of the sensor.

        Part A: 
        This method uses linear interpolation to estimate a sensor reading at the requested timestamp.
        If either sample used in the calculation is invalid, returns None.
    
        Part B: 
        If the requested timestamp is before the sensor came online, or after it went offline, this method 
        will assume that the sensor has been moving at a constant velocity based on the instantaneous
        velocity of the most recent two samples, and return an estimate for the position based on that velocity.

        Hints:
            - Both position and velocity are separable in latitude, longitude, and altitude.
            - It is easiest to work in units of degrees and degrees per second.
            - Assume that the lattitude and longitude exist on a perfect plane. Do not bother correcting for 
              warping of the globe, simply treat them as x and y coordinates in a linear coordinate space. 
            - For part B you can assume that the first and last 2 samples are always valid.
        
        Reference Implementation: 72 lines

        :param timestamp: The timestamp of the requested estimate in seconds since the linux epoch.
        :type timestamp: float
        :return: A new LocationSample containing the estimated position at the requested timestamp.
        :rtype: LocationSample | None
        """
        time_distances = np.subtract(self.__timestamp_buffer, timestamp)
        index = np.argmin(np.abs(time_distances))
        closest_sample: LocationSample = self.__sample_buffer[index]

        # Determine if the timestamp is to the left or right of the closest index.
        extrapolate = False
        left_sample: LocationSample = None
        right_sample: LocationSample = None

        if timestamp < closest_sample.time_utc_seconds:
            if index - 1 < 0:
                # We are extrapolating before poweron.
                extrapolate = True
                left_sample = self.__sample_buffer[0]
                right_sample = self.__sample_buffer[1]

            else:
                if self.__sample_buffer[index-1] is None:
                    return None
                left_sample = self.__sample_buffer[index-1]
                right_sample = self.__sample_buffer[index]
        else:
            if index + 1 >= self.__max_samples:
                extrapolate = True
                left_sample = self.__sample_buffer[-2]
                right_sample = self.__sample_buffer[-1]

            else:
                if self.__sample_buffer[index+1] is None:
                    return None
                left_sample = self.__sample_buffer[index]
                right_sample = self.__sample_buffer[index+1]
        
        if extrapolate:
            delta_time = right_sample.time_utc_seconds - left_sample.time_utc_seconds
            vel_lat = (right_sample.lat_degrees - left_sample.lat_degrees) / delta_time
            vel_lon = (right_sample.lon_degrees - left_sample.lon_degrees) / delta_time
            vel_alt = (right_sample.alt_meters - left_sample.alt_meters) / delta_time

            if index == 0:
                extrap_time = timestamp - left_sample.time_utc_seconds
                
                delta_lat = vel_lat * extrap_time
                delta_lon = vel_lon * extrap_time
                delta_alt = vel_alt * extrap_time

                new_lat = left_sample.lat_degrees + delta_lat
                new_lon = left_sample.lon_degrees + delta_lon
                new_alt = left_sample.alt_meters + delta_alt
            else:
                extrap_time = timestamp - right_sample.time_utc_seconds
                
                delta_lat = vel_lat * extrap_time
                delta_lon = vel_lon * extrap_time
                delta_alt = vel_alt * extrap_time

                new_lat = right_sample.lat_degrees + delta_lat
                new_lon = right_sample.lon_degrees + delta_lon
                new_alt = right_sample.alt_meters + delta_alt

            interp_sample = LocationSample(new_lat, new_lon, new_alt, timestamp)
            return interp_sample

        baseline = right_sample.time_utc_seconds - left_sample.time_utc_seconds
        normalized_timestamp = timestamp - left_sample.time_utc_seconds
        percent = normalized_timestamp / baseline

        interp_lat = ((1 - percent) * left_sample.lat_degrees) + (percent * right_sample.lat_degrees)
        interp_lon = ((1 - percent) * left_sample.lon_degrees) + (percent * right_sample.lon_degrees)
        interp_alt = ((1 - percent) * left_sample.alt_meters) + (percent * right_sample.alt_meters)

        interp_sample = LocationSample(interp_lat, interp_lon, interp_alt, timestamp)
        return interp_sample

    def get_true_course_degrees(self, timestamp: float) -> float | None:
        """
        Motivation:
        The frontend team now realizes that they want the position sprite to rotate so that it
        aligns with the direction the sensor is moving. Of course, this should just be a library
        call or something...

        This method returns the course of the position sensor at the requested timestamp. 
        If either sample used in the calculation is invalid, returns None.
        If the requested timestamp is before the sensor came online, or after the camera went
        offline, this method will assume that the sensor has been moving at a constant velocity based
        on the instantaneous velocity of the most recent two samples, and return an estimate for the track
        based on that velocity.

        Hints:
            - Course is defined as the direction of movement with respect to North.
              In other words, this is the direction of movement where 0 degrees is moving perfectly north,
              90 perfectly east, -90 is perfectly west, and 180 or -180 is perfectly south. 
            - True course means that North is defined geometricly - with respect to the North pole instead
              of with respect to the magnetic pole which is moving over russia. This means that you shouldn't
              have to deal with any weird magnetic corrections, just utilize simple trig functions.
            - The tests assume that values from -180 to 180 are valid. It would be equally valid in an engineering sense
              to utilize 0-360 instead, but for now utilize the range above.

        :param timestamp: The timestamp of the requested estimate in seconds since the linux epoch.
        :type timestamp: float
        :return: The track of the sensor in true degrees.
        :rtype: float | None
        """
        time_distances = np.subtract(self.__timestamp_buffer, timestamp)
        index = np.argmin(np.abs(time_distances))
        closest_sample: LocationSample = self.__sample_buffer[index]

        # Determine if the timestamp is to the left or right of the closest index.
        extrapolate = False
        left_sample: LocationSample = None
        right_sample: LocationSample = None

        if timestamp < closest_sample.time_utc_seconds:
            if index - 1 < 0:
                # We are extrapolating before poweron.
                left_sample = self.__sample_buffer[0]
                right_sample = self.__sample_buffer[1]

            else:
                if self.__sample_buffer[index-1] is None:
                    return None
                left_sample = self.__sample_buffer[index-1]
                right_sample = self.__sample_buffer[index]
        else:
            if index + 1 >= self.__max_samples:
                left_sample = self.__sample_buffer[-2]
                right_sample = self.__sample_buffer[-1]

            else:
                if self.__sample_buffer[index+1] is None:
                    return None
                left_sample = self.__sample_buffer[index]
                right_sample = self.__sample_buffer[index+1]
        
        delta_lat = right_sample.lat_degrees - left_sample.lat_degrees
        delta_lon = right_sample.lon_degrees - left_sample.lon_degrees

        course_true_deg = math.degrees(math.atan2(delta_lat, delta_lon))

        return course_true_deg
