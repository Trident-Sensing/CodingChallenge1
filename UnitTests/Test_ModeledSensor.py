import sys
sys.path.append('..')

import unittest
from LocationSensor import LocationSample, LocationSensor
from ModeledLocationSensor import ModeledLocationSensor

class Part1_TestGetNearest(unittest.TestCase):
    def test_first_sample(self):
        ms = ModeledLocationSensor()
        sample = ms.get_nearest_sample(10.5)

        self.assertAlmostEqual(sample.alt_meters, 4200.0)
        self.assertAlmostEqual(sample.lat_degrees, 41.188007)
        self.assertAlmostEqual(sample.lon_degrees, -112.020859)
        self.assertAlmostEqual(sample.time_utc_seconds, 10.5)

    def test_before_online(self):
        ms = ModeledLocationSensor()
        sample = ms.get_nearest_sample(1.0)

        self.assertAlmostEqual(sample.alt_meters, 4200.0)
        self.assertAlmostEqual(sample.lat_degrees, 41.188007)
        self.assertAlmostEqual(sample.lon_degrees, -112.020859)
        self.assertAlmostEqual(sample.time_utc_seconds, 10.5)
    
    def test_after_online(self):
        ms = ModeledLocationSensor()
        sample = ms.get_nearest_sample(100.0)

        self.assertAlmostEqual(sample.alt_meters, 4200.0)
        self.assertAlmostEqual(sample.lat_degrees, 41.203751)
        self.assertAlmostEqual(sample.lon_degrees, -112.000096)
        self.assertAlmostEqual(sample.time_utc_seconds, 24.50)
    
    def test_middle_sample(self):
        ms = ModeledLocationSensor()
        sample = ms.get_nearest_sample(23.0)

        self.assertAlmostEqual(sample.alt_meters, 4200.0)
        self.assertAlmostEqual(sample.lat_degrees, 41.202207)
        self.assertAlmostEqual(sample.lon_degrees, -112.002098)
        self.assertAlmostEqual(sample.time_utc_seconds, 23.48)

    def test_invalid_sample(self):
        ms = ModeledLocationSensor(sensor_read_path='Data/empty.csv')
        sample = ms.get_nearest_sample(10.0)
        self.assertIsNone(sample)
    
    def test_multiple_reads(self):
        ms = ModeledLocationSensor()
        sample_1 = ms.get_nearest_sample(10.0)
        sample_2 = ms.get_nearest_sample(11.1)

        self.assertAlmostEqual(sample_1.alt_meters, 4200.0)
        self.assertAlmostEqual(sample_1.lat_degrees, 41.188007)
        self.assertAlmostEqual(sample_1.lon_degrees, -112.020859)
        self.assertAlmostEqual(sample_1.time_utc_seconds, 10.5)
        
        # Ensure we are not returning the same thing each time.
        self.assertNotAlmostEqual(sample_1.lat_degrees, sample_2.lat_degrees)
        self.assertNotAlmostEqual(sample_1.lon_degrees, sample_2.lon_degrees)
        self.assertNotAlmostEqual(sample_1.time_utc_seconds, sample_2.time_utc_seconds)

        self.assertAlmostEqual(sample_2.alt_meters, 4200.0)
        self.assertAlmostEqual(sample_2.lat_degrees, 41.188935)
        self.assertAlmostEqual(sample_2.lon_degrees, -112.019638)
        self.assertAlmostEqual(sample_2.time_utc_seconds, 11.51)


class Part2A_TestGetEstimated(unittest.TestCase):
    def test_middle_sample_close_to_first_point(self):
        ms = ModeledLocationSensor()
        sample = ms.get_estimated_sample(10.5)

        self.assertAlmostEqual(sample.alt_meters, 4200.0)
        self.assertAlmostEqual(sample.lat_degrees, 41.188007)
        self.assertAlmostEqual(sample.lon_degrees, -112.020859)
        self.assertAlmostEqual(sample.time_utc_seconds, 10.5)

    def test_middle_sample_close_to_second_point(self):
        ms = ModeledLocationSensor()
        sample = ms.get_estimated_sample(11.51)

        self.assertAlmostEqual(sample.alt_meters, 4200.0)
        self.assertAlmostEqual(sample.lat_degrees, 41.188935)
        self.assertAlmostEqual(sample.lon_degrees, -112.019638)
        self.assertAlmostEqual(sample.time_utc_seconds, 11.51)

    def test_middle_sample_inbetween_points(self):
        ms = ModeledLocationSensor()
        sample = ms.get_estimated_sample(10.75)
        self.assertAlmostEqual(sample.alt_meters, 4200.0)
        self.assertAlmostEqual(sample.lat_degrees, 41.188236, delta=1e-6)
        self.assertAlmostEqual(sample.lon_degrees, -112.020556, delta=1e-6)
        self.assertAlmostEqual(sample.time_utc_seconds, 10.75)

    def test_invalid_sample(self):
        ms = ModeledLocationSensor()
        sample = ms.get_estimated_sample(18.0)
        self.assertIsNotNone(sample)

        sample = ms.get_estimated_sample(19.0)
        self.assertIsNone(sample)

        sample = ms.get_estimated_sample(20.0)
        self.assertIsNone(sample)

        sample = ms.get_estimated_sample(21.0)
        self.assertIsNotNone(sample)

class Part2B_TestGetEstimatedExtrapolation(unittest.TestCase):
    delta=2e-5
    def test_close_to_start(self):
        ms = ModeledLocationSensor()
        sample = ms.get_estimated_sample(10.499)

        self.assertAlmostEqual(sample.alt_meters, 4200.0, delta=self.delta)
        self.assertAlmostEqual(sample.lat_degrees, 41.188007, delta=self.delta)
        self.assertAlmostEqual(sample.lon_degrees, -112.020859, delta=self.delta)
        self.assertAlmostEqual(sample.time_utc_seconds, 10.499, delta=self.delta)

    def test_close_to_end(self):
        ms = ModeledLocationSensor()
        sample = ms.get_estimated_sample(24.501)

        self.assertAlmostEqual(sample.alt_meters, 4200.0, delta=self.delta)
        self.assertAlmostEqual(sample.lat_degrees, 41.203751, delta=self.delta)
        self.assertAlmostEqual(sample.lon_degrees, -112.000096, delta=self.delta)
        self.assertAlmostEqual(sample.time_utc_seconds, 24.501, delta=self.delta)
    
    def test_10_seconds_before_poweron(self):
        ms = ModeledLocationSensor()
        sample = ms.get_estimated_sample(1.50)
        self.assertAlmostEqual(sample.alt_meters, 4200.0, delta=self.delta)
        self.assertAlmostEqual(sample.lat_degrees, 41.17974688118812, delta=self.delta)
        self.assertAlmostEqual(sample.lon_degrees, -112.0317271089109, delta=self.delta)
        self.assertAlmostEqual(sample.time_utc_seconds, 1.50, delta=self.delta)
    
    def test_10_seconds_after_poweroff(self):
        ms = ModeledLocationSensor()
        sample = ms.get_estimated_sample(34.5)
        self.assertAlmostEqual(sample.alt_meters, 4200.0, delta=self.delta)
        self.assertAlmostEqual(sample.lat_degrees, 41.21888825490196, delta=self.delta)
        self.assertAlmostEqual(sample.lon_degrees, -111.9804685490196, delta=self.delta)
        self.assertAlmostEqual(sample.time_utc_seconds, 34.5, delta=self.delta)


class Part3_TestGetEstimatedCourse(unittest.TestCase):
    delta=1e-5
    def test_middle_course(self):
        ms = ModeledLocationSensor()
        sample = ms.get_true_course_degrees(14.0)
        self.assertAlmostEqual(sample, -81.30873495286335, delta=self.delta)

    def test_before_poweron_course(self):
        ms = ModeledLocationSensor()
        sample = ms.get_true_course_degrees(0.0)
        self.assertAlmostEqual(sample, 37.236023752106576, delta=self.delta)

    def test_after_poweroff_course(self):
        ms = ModeledLocationSensor()
        sample = ms.get_true_course_degrees(100)
        self.assertAlmostEqual(sample, 37.640443159078316, delta=self.delta)

    def test_invalid_sample(self):
        ms = ModeledLocationSensor()
        sample = ms.get_true_course_degrees(18.0)
        self.assertIsNotNone(sample)

        sample = ms.get_true_course_degrees(19.0)
        self.assertIsNone(sample)

        sample = ms.get_true_course_degrees(20.0)
        self.assertIsNone(sample)

        sample = ms.get_true_course_degrees(21.0)
        self.assertIsNotNone(sample)
