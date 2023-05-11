import sys
sys.path.append('..')

import unittest
from LocationSensor import LocationSample, LocationSensor

class TestSensor(unittest.TestCase):

    def test_single_read(self):
        ls = LocationSensor()
        sample = ls.read_location()

        self.assertAlmostEqual(sample.alt_meters, 4200.0)
        self.assertAlmostEqual(sample.lat_degrees, 41.188007)
        self.assertAlmostEqual(sample.lon_degrees, -112.020859)
        self.assertAlmostEqual(sample.time_utc_seconds, 10.5)
    
    def test_multiple_reads(self):
        ls = LocationSensor()
        sample_1 = ls.read_location()
        sample_2 = ls.read_location()

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

    def test_invalid_read(self):
        ls = LocationSensor()

        for i in range(9):
            _ = ls.read_location()
        
        sample = ls.read_location()
        self.assertIsNone(sample)
