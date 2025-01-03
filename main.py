import time
from sdk.red_alert_sdk import RedAlert

def main():

    # initalize the red alert object
    alert = RedAlert()
    # check for alerts all the time and do stuff, never stop.
    while True:
        # set empty alert data dict
        alert_data = {}
        city_data = []
        migun_time = 0
        # sleep 1 second before checking alerts over again to not put pressure on the server.
        time.sleep(1)
        # get alerts from pikud ha-oref website
        red_alerts = alert.get_red_alerts()
        # if there is red alerts right now, get into action, quickly!
        if(red_alerts != None):
            # loop through each city there is red alert currently
            for alert_city in red_alerts["data"]:
                # get unique alert id for the current looping alerts
                alert_id = red_alerts["id"]
                # get the data of the current alert code
                for i in alert.locations:
                    if(alert.locations[i]["label"] == alert_city):
                        migun_time = alert.locations[i]["migun_time"]
                        # set the timestamp of the current alert
                        city_data.append(alert.locations[i])
                        # get the coordinates of the city where the rocket is flying to
                        '''
                        # Google Maps requires API key #
                        '''
                        #alert_data["coordinates"] = alert.get_coordinates(location_name=alert_city)
                        # random coordinates where the rocket should fly to in the visualization map
                        #alert_data["random_coordinates"] = alert.random_coordinates(latitude=alert_data["coordinates"]["lat"],longitude=alert_data["coordinates"]["lng"])
                red_alerts["cities_labels"] = city_data
                red_alerts["time_to_run"] = migun_time
                '''
                In this block you do what you have to do with your code,
                now when you have all what you could possibly have including:
                alert id, alert city, time to run away, coordinates of city,
                random coordinates where the missle may land and timestamp when the missle started fireup.
                '''
        else:
            print("[-] No alerts for now, keep checking ...")

if __name__ == "__main__":
    # main()
    alert = RedAlert()
    alert.get_red_alerts_history()

