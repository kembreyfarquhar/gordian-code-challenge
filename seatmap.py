import xml.etree.ElementTree as ET
import json
tree = ET.parse('OTA_AirSeatMapRS.xml')
root = tree.getroot()
body = root.find('{http://schemas.xmlsoap.org/soap/envelope/}Body')
ota_air_seat_map = body.find(
    '{http://www.opentravel.org/OTA/2003/05/common/}OTA_AirSeatMapRS')
seat_map_responses = ota_air_seat_map.find(
    '{http://www.opentravel.org/OTA/2003/05/common/}SeatMapResponses')
seat_map_response = seat_map_responses.find(
    '{http://www.opentravel.org/OTA/2003/05/common/}SeatMapResponse')
seat_map_details = seat_map_response.find(
    '{http://www.opentravel.org/OTA/2003/05/common/}SeatMapDetails')


seats = []

for item in seat_map_details:
    for row in item.findall('{http://www.opentravel.org/OTA/2003/05/common/}RowInfo'):
        cabin_class = row.attrib['CabinType']
        seat_type = None
        seat_id = None
        price = None
        availability = None
        for seat_info in row.findall('{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo'):
            for seat in seat_info:
                if seat.tag == '{http://www.opentravel.org/OTA/2003/05/common/}Summary':
                    availability = seat.attrib['AvailableInd']
                    seat_id = seat.attrib['SeatNumber']
                if seat.tag == '{http://www.opentravel.org/OTA/2003/05/common/}Features':
                    if 'Lavatory' in seat.attrib.values():
                        seat_type = 'Bathroom'
                    else:
                        if not bool(seat.attrib):
                            seat_type = seat.text
                if seat.tag == '{http://www.opentravel.org/OTA/2003/05/common/}Service':
                    for item in seat:
                        price = float(item.attrib['Amount'])
                seats.append({"seat_type": seat_type, "seat_id": seat_id, "price": price,
                              "cabin_class": cabin_class, "availability": availability})


json_seat_info = json.dumps(seats)

print(json_seat_info)
