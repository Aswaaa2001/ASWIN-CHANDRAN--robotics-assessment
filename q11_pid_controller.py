import time


class PIDVelocityController:

    def __init__(
        self,
        kp=2.0,
        ki=0.5,
        kd=0.1,
        max_integral=5
    ):

        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.integral = 0
        self.prev_error = 0

        self.max_integral = max_integral

    def update(
        self,
        desired_velocity,
        measured_velocity,
        dt
    ):

        # Error
        error = (
            desired_velocity
            -
            measured_velocity
        )

        # Integral
        self.integral += (
            error * dt
        )

        # Anti-windup
        # Keep Ki × max_integral
        # inside motor limits
        self.integral = max(
            -self.max_integral,
            min(
                self.integral,
                self.max_integral
            )
        )

        # Derivative
        derivative = (
            error
            -
            self.prev_error
        ) / dt

        # PID output
        output = (
            self.kp * error
            +
            self.ki * self.integral
            +
            self.kd * derivative
        )

        self.prev_error = error

        return output


controller = PIDVelocityController()

desired_velocity = 1.0

while True:

    measured_velocity = 0.7

    motor_cmd = controller.update(
        desired_velocity,
        measured_velocity,
        0.05
    )

    print(
        motor_cmd
    )

    time.sleep(0.05)