import math


class DayCycle:

    def __init__(self, system):

        self.system = system

        self.day_length = 50000
        self.night_length = 50000

        self.start_phase = 0
        self.start_time = 95000
        self.current_time = self.start_time

        self.last_update_time = (
            system.time.get_current_time()
        )

        self.brightness = 0

        self.day = 0
        self.year = 0


    def update(self):

        current_time = (
            self.system.time.get_current_time()
        )

        delta_time = (
            current_time
            -
            self.last_update_time
        )

        self.last_update_time = current_time

        self.current_time += delta_time


        cycle_length = (
            self.day_length
            +
            self.night_length
        )


        if self.current_time >= cycle_length:

            self.current_time -= cycle_length
            self.day += 1
            if self.day >= 100:
                self.day = 0
                self.year += 1



    def get_time_progress(self):

        cycle_length = (
            self.day_length
            +
            self.night_length
        )

        return (
            self.current_time
            /
            cycle_length
        )



    def get_day_night_color(self):

        night = (
            20,
            30,
            80
        )

        day = (
            135,
            206,
            235
        )

        if self.current_time <= self.day_length:

            day_progress = (
                self.current_time
                /
                self.day_length
            )
            self.brightness = (
                math.sin(
                    day_progress
                    *
                    math.pi
                )
            )


            r = int(
                night[0]
                +
                (day[0] - night[0])
                *
                self.brightness
            )

            g = int(
                night[1]
                +
                (day[1] - night[1])
                *
                self.brightness
            )

            b = int(
                night[2]
                +
                (day[2] - night[2])
                *
                self.brightness
            )


        # night phase
        else:

            self.brightness = 0

            r, g, b = night



        self.system.window.fill(
            (
                r,
                g,
                b
            )
        )



    def draw(self):

        self.get_day_night_color()



    def get_brightness(self):

        return int(
            self.brightness * 100
        )



    def get_daytime(self):

        return int(
            self.current_time / 1000
        )



    def is_day(self):

        return (
            self.current_time
            <=
            self.day_length
        )



    def reset(self):

        self.current_time = self.start_time

        self.last_update_time = (
            self.system.time.get_current_time()
        )

        self.brightness = 0

    def get_sun_progress(self):

        if self.current_time > self.day_length:
            return None

        return (
            self.current_time
            /
            self.day_length
        )