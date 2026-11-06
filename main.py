#!/usr/bin/env pybricks-micropython

# Import the Pybricks modules used to control the EV3, motors, sensors, and robot.
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase

# Create the EV3 brick object for sound and other hub features.
ev3 = EV3Brick()

# Configure the drive motors, gripper motors, and gyroscope.
motor_esquerdo = Motor(Port.B)
motor_direito = Motor(Port.C)
motor_garra_abre_fecha = Motor(Port.A)
motor_garra_desce_sobe = Motor(Port.D)
giroscopio = GyroSensor(Port.S2)


# Configure the robot dimensions.
# Pybricks expects millimeters: 88 mm wheel diameter and 314 mm axle track.
robo = DriveBase(
    motor_esquerdo,
    motor_direito,
    wheel_diameter=88,
    axle_track=314,
)

# PID controller gains used to correct the robot's heading.
# With KI and KD set to zero, only proportional correction is active.
KP = 1
KI = 0
KD = 0


def limitar(valor, minimo, maximo):
    """Keep a value within the specified minimum and maximum limits."""
    return max(minimo, min(maximo, valor))


def curva_esquerda(graus):
    """Turn the robot left by the requested number of degrees."""
    # Reset the gyroscope so the turn is measured from the current position.
    giroscopio.reset_angle(0)

    # Continue turning until the target angle is reached.
    while abs(giroscopio.angle()) < abs(graus):
        angulo = giroscopio.angle()

        # Apply an initial turning speed while the robot is near the start.
        if abs(angulo) < 10:
            motor_esquerdo.run(300)
            motor_direito.run(-300)

        # Reduce the motor speed as the robot approaches the target angle.
        velocidade = (graus - angulo) / 2.5
        motor_esquerdo.run(velocidade)
        motor_direito.run(-velocidade)
        wait(10)

    # Stop both drive motors when the turn is complete.
    motor_esquerdo.stop(Stop.BRAKE)
    motor_direito.stop(Stop.BRAKE)


def curva_direita(graus):
    """Turn the robot right by the requested number of degrees."""
    # Reset the gyroscope so the turn is measured from the current position.
    giroscopio.reset_angle(0)

    # Continue turning until the target angle is reached.
    while abs(giroscopio.angle()) < abs(graus):
        angulo = giroscopio.angle()

        # Apply an initial turning speed while the robot is near the start.
        if abs(angulo) < 10:
            motor_esquerdo.run(300)
            motor_direito.run(-300)

        # Reduce the motor speed as the robot approaches the target angle.
        velocidade = (graus - angulo) / 2.5
        motor_esquerdo.run(velocidade)
        motor_direito.run(-velocidade)
        wait(10)

    # Stop both drive motors when the turn is complete.
    motor_esquerdo.stop(Stop.BRAKE)
    motor_direito.stop(Stop.BRAKE)


def andar_frente_centimetros(centimetros):
    """Drive forward for the requested distance in centimeters."""
    # Reset motor encoders and the gyroscope before starting the movement.
    motor_esquerdo.reset_angle(0)
    motor_direito.reset_angle(0)
    giroscopio.reset_angle(0)

    # Convert the requested distance from centimeters to motor rotation degrees.
    alvo = centimetros * 360 / 8.8 / 3.14

    # Initialize the values used by the PID correction.
    integral = 0
    last_error = 0

    # Keep moving until the left motor reaches the target rotation.
    while abs(motor_esquerdo.angle()) < abs(alvo):
        # Measure the robot's heading error relative to zero degrees.
        erro = giroscopio.angle() - 0

        # Update the integral and derivative terms.
        integral += erro
        derivativo = erro - last_error

        # Calculate the steering correction from the PID terms.
        correcao = erro * KP + integral * KI + derivativo * KD

        # Adjust the two motor speeds to keep the robot moving straight.
        motor_esquerdo.run(35 + correcao)
        motor_direito.run(35 - correcao)

        # Save the current error for the next derivative calculation.
        last_error = erro
        wait(10)

    # Stop both drive motors when the target distance is reached.
    motor_esquerdo.stop(Stop.BRAKE)
    motor_direito.stop(Stop.BRAKE)


def andar_tras_centimetros(centimetros):
    """Drive backward for the requested distance in centimeters."""
    # Reset motor encoders and the gyroscope before starting the movement.
    motor_esquerdo.reset_angle(0)
    motor_direito.reset_angle(0)
    giroscopio.reset_angle(0)

    # Convert the requested distance from centimeters to motor rotation degrees.
    alvo = centimetros * 360 / 8.8 / 3.14

    # Initialize the values used by the PID correction.
    integral = 0
    last_error = 0

    # Keep moving until the left motor reaches the target rotation.
    while abs(motor_esquerdo.angle()) < abs(alvo):
        # Measure the robot's heading error relative to zero degrees.
        erro = giroscopio.angle() - 0

        # Update the integral and derivative terms.
        integral += erro
        derivativo = erro - last_error

        # Calculate the steering correction from the PID terms.
        correcao = erro * KP + integral * KI + derivativo * KD

        # Adjust the motor speeds in reverse while correcting the heading.
        motor_esquerdo.run(-35 - correcao)
        motor_direito.run(-35 + correcao)

        # Save the current error for the next derivative calculation.
        last_error = erro
        wait(10)

    # Stop both drive motors when the target distance is reached.
    motor_esquerdo.stop(Stop.BRAKE)
    motor_direito.stop(Stop.BRAKE)


def abrir_garra(rotacao = 2.5):
    angulo = rotacao * 360  # Convert rotations to degrees
    velocidade = motor_garra_abre_fecha.control.limits()[0] * 0.30 
    """Open the gripper by running the opening motor."""
    motor_garra_abre_fecha.run_angle(velocidade, angulo)  # Adjust speed and angle as needed
    motor_garra_abre_fecha.stop(Stop.BRAKE)

def fechar_garra(rotacao = 2.5):
    angulo = -rotacao * 360  # Convert rotations to degrees (negative for closing)
    velocidade = motor_garra_abre_fecha.control.limits()[0] * 0.30 
    """Close the gripper by running the closing motor."""
    motor_garra_abre_fecha.run_angle(velocidade, angulo)  # Adjust speed and angle as needed
    motor_garra_abre_fecha.stop(Stop.BRAKE)

def subir_garra(rotacao = 2.5):
    angulo = rotacao * 360  # Convert rotations to degrees
    velocidade = motor_garra_desce_sobe.control.limits()[0] * 0.30 
    """Raise the gripper by running the raising motor."""
    motor_garra_desce_sobe.run_angle(velocidade, angulo)  # Adjust speed and angle as needed
    motor_garra_desce_sobe.stop(Stop.BRAKE)

def descer_garra(rotacao = 2.5):
    angulo = -rotacao * 360  # Convert rotations to degrees (negative for lowering)
    velocidade = motor_garra_desce_sobe.control.limits()[0] * 0.30 
    """Lower the gripper by running the lowering motor."""
    motor_garra_desce_sobe.run_angle(velocidade, angulo)  # Adjust speed and angle as needed
    motor_garra_desce_sobe.stop(Stop.BRAKE)
