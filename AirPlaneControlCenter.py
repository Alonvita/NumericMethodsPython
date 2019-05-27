import datetime
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


class TimeIndicationEventArguments:
    _timestamp = None

    def __init__(self, timestamp):
        self._timestamp = timestamp

    def get_timestamp(self):
        return self._timestamp


class TimeIndicatingObject(ABC):
    def __update_time_changed(self):
        raise NotImplementedError


class AirPlaneControlCenter(TimeIndicatingObject):
    _air_planes = None
    _line_space = None

    def __init__(self, line_space_dimensions):
        if len(line_space_dimensions) != 3:
            raise ValueError("line space dimensions must be of the following format: (start, stop, num)")

        # initialize an empty air planes list
        self._air_planes = list()
        try:
            self._line_space = np.linspace(line_space_dimensions[0],
                                           line_space_dimensions[1],
                                           line_space_dimensions[3])
        except ValueError:
            raise ValueError("error in given line space dimensions. Airplane NOT added")

    def __update_time_changed(self):
        """
        __update_time_changed(self).

        update all airplanes with a new TimeIndicationEventArguments, with the event time (now)
        """
        for airplane in self._air_planes:
            # update airplane
            airplane.time_changed_event(TimeIndicationEventArguments(datetime.datetime.now()))

    def add_airplane(self, desired_departure_time, route_equation):
        """
        add_airplane(self)

        adds a new airplane to the system, considering existing airplanes.
        The function will call [NAME] to calculate departure time for the newly added airplane.

        :param desired_departure_time: the desired departure time may vary, as the systems will
                calculate the ideal time for the airplane to depart so there are no collisions
                with the other airplanes in the system.
        :param route_equation: the equation of the route

        :return: returns the h0 set to the airplane - that is the set departure time.
        """

        for air_plane in self._air_planes:
            simulate_plane = AirPlane(len(self._air_planes),
                                      desired_departure_time,
                                      route_equation)

            if self.__collision_detected_recursive(air_plane, simulate_plane):
                desired_departure_time += 1

        # adds a new airplane with the time calculated
        self._air_planes.append(AirPlane(len(self._air_planes),
                                         desired_departure_time,
                                         route_equation))

        return desired_departure_time

    def __animate_airplanes(self):
        pass

    def __collision_detected_recursive(self, airplane1, airplane2):
        pass


class LineEquation:
    """
    Line equation is: y = ax + b.
    """
    _a = 0
    _b = 0

    def __init__(self, x_coefficient, free_variable):
        self._a = x_coefficient
        self._b = free_variable

    def get_a(self):
        return self._a

    def get_b(self):
        return self._b


class TimeDependantObject(ABC):
    """
    Time dependant listener object.
    """
    def time_changed_event(self, event_args):
        raise NotImplementedError


class AirPlane(TimeDependantObject):
    _id = None
    _location = None
    _position = None
    _departure_time = None
    _route_equation = None

    def __init__(self, plane_id, starting_location, departure_time, route_equation):
        self._id = plane_id
        self._location = starting_location
        self._departure_time = departure_time
        self._route_equation = route_equation

    def time_changed_event(self, event_args):
        # get the time stamp
        time_stamp = event_args.get_timestamp()

        # get time difference from the initial take off
        delta = time_stamp - self._departure_time

        # calculate the new location for the airplane
        self._location = self._route_equation.get_a() * delta.miliseconds + self._route_equation.get_b()

    def get_id(self):
        return self._id

    def get_h0(self):
        return self._departure_time

    def get_route_equation(self):
        return self._route_equation


def main():
    pass


if __name__ == '__main__':
    main()

