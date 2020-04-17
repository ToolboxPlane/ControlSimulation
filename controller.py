import planestate
import input


class Controller:
    def get(self, x: planestate.PlaneState, t: float) -> input.Input:
        output = input.Input()

        if t < 10:
            output.power = 1
        else:
            output.power = 0

        return output
