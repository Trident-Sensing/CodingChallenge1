# Author: Colin Pollard
# Date Created: 4/29/2023
# Copyright: Trident Sensing LLC. (colin.pollard@tridentsensing.com)

from LocationSensor import LocationSensor, LocationSample
import numpy as np
import math

''' 
Welcome to the first attempt at a technical interview question for prospective TS engineers!

- This interview asks you to implement the class below. Don't modify any files other than this one.
- There are unit tests which will evaluate your implementation. Test_Sensor should pass immediately, you will need to get Test_ModeledSensor to pass.
- Feel free to use any tools you normally would while coding.
- Using libraries is encouraged. We utilized numpy and math in our implementation.
- Don't stare at the solutions directory, I'm far too lazy to keep them elsewhere.
- The first "question" is implementing get_nearest_sample, try to read the motivation in the constrtuctor and then implement this function in tandem with constructor logic.

Side note:
- The None handling in this project doesn't really make sense from a motivation perspective, but is added for complexity and additional logic requirements.

Pissing Contest:
Colin Pollard: 16:57, 12:19, ~13:01, ~5:02 | ~47:00
Luke Majors: 16:54, 33:18, 

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
        pass


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
        pass
        

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
        pass


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
        

        pass
