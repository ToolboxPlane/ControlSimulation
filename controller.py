import planestate
import input


class Controller:
    def get(self, x: planestate.PlaneState, t: float) -> input.Input:
        output = input.Input()
        output.power = 1
        if t < 10:
            output.elevon_l = output.elevon_r = 0
        else:
            output.elevon_l = 1
            output.elevon_r = -1

        return output
