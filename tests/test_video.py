import xml.etree.ElementTree as ET

import httpretty

from tests import FulcrumTestCase


class VideoTest(FulcrumTestCase):
    @httpretty.activate
    def test_search(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/videos',
            body='{"videos": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        videos = self.fulcrum_api.videos.search()
        self.assertIsInstance(videos, dict)
        self.assertEqual(len(videos['videos']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/videos/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        video = self.fulcrum_api.videos.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertIsInstance(video, dict)
        self.assertEqual(video['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_track_json(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/videos/5b656cd8-f3ef-43e9-8d22-84d015052778/track.json',
            body='{"tracks":[{"track":[[1403210979925,27.93367156854065,-82.7239782096335,2.311797142028809,1414,10,-1,-1,251.4257049560547,null],[1403210982639,27.93367156854065,-82.7239782096335,2.311797142028809,1414,10,-1,-1,212.7987899780273,null]]}]}',
            status=200)
        resp = self.fulcrum_api.videos.track('5b656cd8-f3ef-43e9-8d22-84d015052778', 'json')
        self.assertIsInstance(resp, dict)
        self.assertEqual(resp['tracks'][0]['track'][0][0], 1403210979925)

    @httpretty.activate
    def test_track_gpx(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/videos/5b656cd8-f3ef-43e9-8d22-84d015052778/track.gpx',
            body='<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" creator="Fulcrum" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd">\n  <metadata>\n    <link href="http://fulcrumapp.com">\n      <text>Fulcrum</text>\n    </link>\n  </metadata>\n\n  <trk>\n    <name>2BD6595F-169B-4B85-A798-77E3777D7B18</name>\n\n    <trkseg>\n\n<trkpt lat="27.93367156854065" lon="-82.7239782096335">\n  <ele>2.311797142028809</ele>\n  <time>2014-06-19T20:49:39Z</time>\n</trkpt>\n\n<trkpt lat="27.93367156854065" lon="-82.7239782096335">\n  <ele>2.311797142028809</ele>\n  <time>2014-06-19T20:49:42Z</time>\n</trkpt>\n\n    </trkseg>\n\n  </trk>\n\n</gpx>\n',
            status=200)
        resp = self.fulcrum_api.videos.track('5b656cd8-f3ef-43e9-8d22-84d015052778', 'gpx')
        xml = ET.fromstring(resp.decode('UTF-8'))
        self.assertIsInstance(xml, ET.Element)
        self.assertEqual(xml.attrib['creator'], 'Fulcrum')
