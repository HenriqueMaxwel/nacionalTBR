#!/usr/bin/env pybricks-micropython
# Informa ao sistema EV3 que este programa deve ser executado com Pybricks MicroPython.
# Tells the EV3 system to run this program with Pybricks MicroPython.

# Importa as classes e funções Pybricks usadas neste programa.
# Imports the Pybricks classes and functions used in this program.
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase

# Cria um cronômetro; o tempo é exibido em milissegundos.
# Creates a stopwatch; elapsed time is displayed in milliseconds.
cronometro = StopWatch()

# Cria o objeto que representa o bloco EV3.
# Creates the object that represents the EV3 Brick.
ev3 = EV3Brick()

# Configura os motores de tração e o giroscópio nas portas utilizadas.
# Configures the drive motors and gyroscope on the ports used.
motor_esquerdo = Motor(Port.B)
motor_direito = Motor(Port.C)
giroscopio = GyroSensor(Port.S2)

# Os motores da garra são opcionais. Começam como None e só são criados
# se o EV3 detectar um motor conectado à porta correspondente.
# The gripper motors are optional. They start as None and are created
# only if the EV3 detects a motor connected to the corresponding port.
motor_garra_abre_fecha = None
motor_garra_desce_sobe = None

try:
    motor_garra_abre_fecha = Motor(Port.A)
    print("Motor A conectado")
except OSError:
    # O programa pode continuar sem o motor A; as funções da garra verificarão isso.
    # The program can continue without motor A; the gripper functions check for this.
    print("Motor A não conectado")

try:
    motor_garra_desce_sobe = Motor(Port.D)
    print("Motor D conectado")
except OSError:
    # O programa pode continuar sem o motor D.
    # The program can continue without motor D.
    print("Motor D não conectado")

# Define a geometria do robô em milímetros: diâmetro da roda e distância entre rodas.
# Define the robot geometry in millimeters: wheel diameter and axle track.
# Este objeto está configurado, mas as funções de movimento abaixo controlam
# os motores diretamente e não usam os métodos do DriveBase.
# This object is configured, but the movement functions below control
# the motors directly and do not use DriveBase methods.
robo = DriveBase(
    motor_esquerdo,
    motor_direito,
    wheel_diameter=88,
    axle_track=314,
)

# Ganhos do controlador PID usado para corrigir a direção durante o deslocamento.
# PID controller gains used to correct the heading while driving.
# KP aplica correção proporcional ao erro atual do giroscópio.
# KP applies a correction proportional to the current gyroscope error.
# KI e KD estão em zero; portanto, os termos integral e derivativo não alteram a correção.
# KI and KD are zero, so the integral and derivative terms do not affect the correction.
KP = 8
KI = 0
KD = 0


def limitar(valor, minimo, maximo):
    """
    Limita um valor ao intervalo informado.
    Clamp a value to the specified range.

    Observação: esta função está definida, mas não é chamada no código atual.
    Note: this function is defined but is not called in the current code.
    """
    return max(minimo, min(maximo, valor))


def curva_esquerda(graus):
    """
    Gira o robô para a esquerda até atingir o ângulo solicitado.
    Turn the robot left until it reaches the requested angle.

    O giroscópio é zerado no início, e os motores giram em sentidos opostos.
    The gyroscope is reset at the start, and the motors run in opposite directions.
    """
    giroscopio.reset_angle(0)

    # Continua enquanto o ângulo medido ainda estiver abaixo do alvo.
    # Continue while the measured angle is still below the target.
    while abs(giroscopio.angle()) < abs(graus):
        angulo = giroscopio.angle()

        # Aplica uma velocidade inicial quando o robô ainda está perto do começo da curva.
        # Applies an initial speed while the robot is still near the start of the turn.
        if abs(angulo) < 10:
            motor_esquerdo.run(-300)
            motor_direito.run(300)

        # Calcula a velocidade a partir da diferença entre o ângulo-alvo e o ângulo atual.
        # Calculates speed from the difference between the target and current angles.
        # O divisor 2.5 determina o quanto a velocidade diminui conforme se aproxima do alvo.
        # The divisor 2.5 controls how quickly speed decreases near the target.
        velocidade = (graus - angulo) / 2.5

        motor_esquerdo.run(-velocidade)
        motor_direito.run(velocidade)
        wait(10)

    # Freia os motores quando a curva termina.
    # Brakes the motors when the turn is complete.
    motor_esquerdo.stop(Stop.BRAKE)
    motor_direito.stop(Stop.BRAKE)


def curva_direita(graus):
    """
    Gira o robô para a direita até atingir o ângulo solicitado.
    Turn the robot right until it reaches the requested angle.

    O giroscópio é zerado no início, e os motores giram em sentidos opostos.
    The gyroscope is reset at the start, and the motors run in opposite directions.
    """
    giroscopio.reset_angle(0)

    # Continua enquanto o ângulo medido ainda estiver abaixo do alvo.
    # Continue while the measured angle is still below the target.
    while abs(giroscopio.angle()) < abs(graus):
        angulo = giroscopio.angle()

        # Aplica uma velocidade inicial quando o robô ainda está perto do começo da curva.
        # Applies an initial speed while the robot is still near the start of the turn.
        if abs(angulo) < 10:
            motor_esquerdo.run(300)
            motor_direito.run(-300)

        # Calcula a velocidade a partir da diferença entre o ângulo-alvo e o ângulo atual.
        # Calculates speed from the difference between the target and current angles.
        velocidade = (graus - angulo) / 2.5

        motor_esquerdo.run(velocidade)
        motor_direito.run(-velocidade)
        wait(10)

    # Freia os motores quando a curva termina.
    # Brakes the motors when the turn is complete.
    motor_esquerdo.stop(Stop.BRAKE)
    motor_direito.stop(Stop.BRAKE)


def andar_frente_centimetros(centimetros):
    """
    Move o robô para frente pela distância informada em centímetros.
    Drive the robot forward by the specified distance in centimeters.
    """
    # Zera os encoders dos motores e o ângulo do giroscópio antes do movimento.
    # Resets the motor encoders and gyroscope angle before moving.
    motor_esquerdo.reset_angle(0)
    motor_direito.reset_angle(0)
    giroscopio.reset_angle(0)

    # Converte a distância em centímetros para graus de rotação do motor.
    # Converts the distance in centimeters to motor rotation degrees.
    # A fórmula usa o diâmetro de roda de 8,8 cm e pi aproximado como 3.14.
    # The formula uses an 8.8 cm wheel diameter and an approximate value of pi (3.14).
    alvo = centimetros * 360 / 8.8 / 3.14

    # Inicializa os valores acumulado e anterior usados pelo cálculo PID.
    # Initializes the accumulated and previous values used by the PID calculation.
    integral = 0
    last_error = 0

    # Usa o encoder do motor esquerdo para decidir quando a distância foi percorrida.
    # Uses the left motor encoder to determine when the target distance has been reached.
    while abs(motor_esquerdo.angle()) < abs(alvo):
        # Mede o desvio do robô em relação ao ângulo zero.
        # Measures the robot's heading deviation from zero degrees.
        erro = giroscopio.angle() - 0

        # Atualiza os termos integral e derivativo.
        # Updates the integral and derivative terms.
        integral += erro
        derivativo = erro - last_error

        # Combina os termos PID; com KI e KD iguais a zero, só KP contribui atualmente.
        # Combines the PID terms; with KI and KD set to zero, only KP currently contributes.
        correcao = erro * KP + integral * KI + derivativo * KD

        # Ajusta a velocidade de cada motor para corrigir o rumo.
        # Adjusts each motor speed to correct the heading.
        # 700 é a velocidade-base em graus por segundo; a correção é somada a um lado
        # e subtraída do outro.
        # 700 is the base speed in degrees per second; the correction is added to one
        # side and subtracted from the other.
        motor_esquerdo.run(700 + correcao)
        motor_direito.run(700 - correcao)

        # Guarda o erro atual para o próximo cálculo derivativo.
        # Saves the current error for the next derivative calculation.
        last_error = erro
        wait(10)

    # Freia os motores ao atingir a distância.
    # Brakes the motors when the distance is reached.
    motor_esquerdo.stop(Stop.BRAKE)
    motor_direito.stop(Stop.BRAKE)


def andar_tras_centimetros(centimetros):
    """
    Move o robô para trás pela distância informada em centímetros.
    Drive the robot backward by the specified distance in centimeters.
    """
    # Zera os encoders dos motores e o ângulo do giroscópio antes do movimento.
    # Resets the motor encoders and gyroscope angle before moving.
    motor_esquerdo.reset_angle(0)
    motor_direito.reset_angle(0)
    giroscopio.reset_angle(0)

    # Converte a distância em centímetros para graus de rotação do motor.
    # Converts the distance in centimeters to motor rotation degrees.
    alvo = centimetros * 360 / 8.8 / 3.14

    # Inicializa os valores acumulado e anterior usados pelo cálculo PID.
    # Initializes the accumulated and previous values used by the PID calculation.
    integral = 0
    last_error = 0

    # Usa o encoder do motor esquerdo para decidir quando a distância foi percorrida.
    # Uses the left motor encoder to determine when the target distance has been reached.
    while abs(motor_esquerdo.angle()) < abs(alvo):
        # Mede o desvio do robô em relação ao ângulo zero.
        # Measures the robot's heading deviation from zero degrees.
        erro = giroscopio.angle() - 0

        # Atualiza os termos integral e derivativo.
        # Updates the integral and derivative terms.
        integral += erro
        derivativo = erro - last_error

        # Calcula a correção PID; atualmente apenas o termo proporcional está ativo.
        # Calculates the PID correction; only the proportional term is active right now.
        correcao = erro * KP + integral * KI + derivativo * KD

        # Aplica velocidades negativas para mover o robô para trás e corrigir o rumo.
        # Applies negative speeds to drive backward while correcting the heading.
        motor_esquerdo.run(-700 - correcao)
        motor_direito.run(-700 + correcao)

        # Guarda o erro atual para o próximo cálculo derivativo.
        # Saves the current error for the next derivative calculation.
        last_error = erro
        wait(10)

    # Freia os motores ao atingir a distância.
    # Brakes the motors when the distance is reached.
    motor_esquerdo.stop(Stop.BRAKE)
    motor_direito.stop(Stop.BRAKE)


def abrir_garra(rotacao=2.5):
    """
    Abre a garra girando o motor A pelo número de rotações informado.
    Opens the gripper by rotating motor A for the specified number of rotations.
    """
    # Evita chamar métodos de motor se o motor A não foi detectado.
    # Avoids calling motor methods if motor A was not detected.
    if motor_garra_abre_fecha is None:
        print("Motor da garra abrir/fechar não está conectado. Não é possível abrir a garra.")
        return

    # Converte rotações completas para graus, pois run_angle usa graus.
    # Converts full rotations to degrees because run_angle uses degrees.
    angulo = rotacao * 360

    # Usa 30% do limite máximo de velocidade do motor, em graus por segundo.
    # Uses 30% of the motor's maximum speed limit, in degrees per second.
    velocidade = motor_garra_abre_fecha.control.limits()[0] * 0.30

    motor_garra_abre_fecha.run_angle(velocidade, angulo)
    motor_garra_abre_fecha.stop(Stop.BRAKE)


def fechar_garra(rotacao=2.5):
    """
    Fecha a garra girando o motor A no sentido oposto.
    Closes the gripper by rotating motor A in the opposite direction.
    """
    if motor_garra_abre_fecha is None:
        print("Motor da garra abrir/fechar não está conectado. Não é possível fechar a garra.")
        return

    # O sinal negativo inverte o sentido do motor.
    # The negative sign reverses the motor direction.
    angulo = -rotacao * 360
    velocidade = motor_garra_abre_fecha.control.limits()[0] * 0.30

    motor_garra_abre_fecha.run_angle(velocidade, angulo)
    motor_garra_abre_fecha.stop(Stop.BRAKE)


def subir_garra(rotacao=2.5):
    """
    Sobe a garra usando o motor D.
    Raises the gripper using motor D.
    """
    if motor_garra_desce_sobe is None:
        print("Motor da garra subir/descer não está conectado. Não é possível subir a garra.")
        return

    angulo = rotacao * 360
    velocidade = motor_garra_desce_sobe.control.limits()[0] * 0.30

    motor_garra_desce_sobe.run_angle(velocidade, angulo)
    motor_garra_desce_sobe.stop(Stop.BRAKE)


def descer_garra(rotacao=2.5):
    """
    Desce a garra usando o motor D.
    Lowers the gripper using motor D.
    """
    if motor_garra_desce_sobe is None:
        print("Motor da garra subir/descer não está conectado. Não é possível descer a garra.")
        return

    # O sinal negativo inverte o sentido do motor.
    # The negative sign reverses the motor direction.
    angulo = -rotacao * 360
    velocidade = motor_garra_desce_sobe.control.limits()[0] * 0.30

    motor_garra_desce_sobe.run_angle(velocidade, angulo)
    motor_garra_desce_sobe.stop(Stop.BRAKE)


# Exibe o tempo desde a criação do cronômetro, em milissegundos.
# Displays the time elapsed since the stopwatch was created, in milliseconds.
print("Inicialização concluída:", cronometro.time(), "ms")

# Sequência principal executada quando o arquivo é iniciado.
# Main sequence executed when this file starts.
andar_frente_centimetros(150)
andar_tras_centimetros(50)
