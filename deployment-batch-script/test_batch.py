from score import test_ride_duration_prediction

if __name__ == "__main__":
    test_ride_duration_prediction.serve(
        name = "ride_duration_scheduled",
        cron = "0/10 * * * *")

