# Blue Minds — EV3 Robot | TBR 2026

🇧🇷 [Português](#português) | 🇺🇸 [English](#english)

---

## Português

### Sobre o projeto

Este repositório contém o programa em Python do robô LEGO MINDSTORMS EV3 da equipe **Blue Minds**, desenvolvido para o **Torneio Brasileiro de Robótica (TBR) 2026**.

O programa usa **EV3 MicroPython com Pybricks** para controlar o deslocamento do robô, corrigir sua trajetória com um giroscópio e movimentar a garra.

### Recursos

- Deslocamento para frente e para trás por uma distância em centímetros.
- Curvas controladas pelo giroscópio.
- Correção da direção durante o deslocamento.
- Abertura e fechamento da garra por rotações do motor.

### Hardware e portas

| Componente | Porta |
| --- | --- |
| Motor esquerdo de tração | B |
| Motor direito de tração | C |
| Motor da garra | A |
| Giroscópio | S2 |

O código também configura o diâmetro das rodas e a distância entre elas no objeto `DriveBase`. Confira esses valores e as portas antes de executar o programa.

### Funções principais

- `andar_frente_centimetros(centimetros)` — desloca o robô para frente pela distância indicada.
- `andar_tras_centimetros(centimetros)` — desloca o robô para trás pela distância indicada.
- `curva_esquerda(graus)` — realiza uma curva para a esquerda usando o giroscópio.
- `curva_direita(graus)` — realiza uma curva para a direita usando o giroscópio.
- `abrir_garra(rotacoes=2.5)` — abre a garra pelo número de rotações informado.
- `fechar_garra(rotacoes=2.5)` — fecha a garra pelo número de rotações informado.

### Exemplo de sequência

Adicione os comandos que deseja executar ao final do arquivo Python. Por exemplo:

```python
andar_tras_centimetros(100)
curva_direita(90)
abrir_garra()
```

Esse exemplo faz o robô andar para trás 100 cm, virar à direita 90° e abrir a garra. Altere a sequência conforme a estratégia da equipe.

### Requisitos

- Robô LEGO MINDSTORMS EV3.
- Cartão microSD preparado com EV3 MicroPython v2.0.
- Visual Studio Code com a extensão EV3 MicroPython.
- Motores e giroscópio conectados às portas configuradas no código.

### Observações

- Distâncias e ângulos dependem da montagem e da calibração do robô.
- Teste os movimentos em uma área livre antes de usar o robô na arena.
- Confira o sentido dos motores da garra. Se necessário, inverta o sinal da rotação.
- Ajuste os parâmetros de controle e as dimensões do `DriveBase` para o seu robô.

---

## English

### About the project

This repository contains the Python program for the **Blue Minds** LEGO MINDSTORMS EV3 robot, developed for the **2026 Brazilian Robotics Tournament (TBR 2026)**.

The program uses **EV3 MicroPython with Pybricks** to control the robot's movement, correct its heading with a gyroscope, and operate its gripper.

### Features

- Forward and backward movement over a distance measured in centimeters.
- Gyroscope-controlled turns.
- Heading correction while driving.
- Gripper opening and closing by motor rotations.

### Hardware and ports

| Component | Port |
| --- | --- |
| Left drive motor | B |
| Right drive motor | C |
| Gripper motor | A |
| Gyroscope | S2 |

The code also configures the wheel diameter and the distance between the wheels in the `DriveBase` object. Check these values and the port connections before running the program.

### Main functions

- `andar_frente_centimetros(centimetros)` — drives the robot forward by the specified distance.
- `andar_tras_centimetros(centimetros)` — drives the robot backward by the specified distance.
- `curva_esquerda(graus)` — turns the robot left using the gyroscope.
- `curva_direita(graus)` — turns the robot right using the gyroscope.
- `abrir_garra(rotacoes=2.5)` — opens the gripper by the specified number of rotations.
- `fechar_garra(rotacoes=2.5)` — closes the gripper by the specified number of rotations.

### Example sequence

Add the commands you want to run at the end of the Python file. For example:

```python
andar_tras_centimetros(100)
curva_direita(90)
abrir_garra()
```

This example drives backward 100 cm, turns right 90°, and opens the gripper. Change the sequence to match the team's strategy.

### Requirements

- LEGO MINDSTORMS EV3 robot.
- microSD card prepared with EV3 MicroPython v2.0.
- Visual Studio Code with the EV3 MicroPython extension.
- Motors and gyroscope connected to the ports configured in the code.

### Notes

- Distances and angles depend on the robot's construction and calibration.
- Test movements in a clear area before running the robot in the competition arena.
- Check the gripper motor direction. Reverse the rotation sign if needed.
- Adjust the control parameters and `DriveBase` dimensions for your robot.

---

## Créditos / Credits

**Equipe / Team:** Blue Minds  
**Competição / Competition:** TBR 2026 — Torneio Brasileiro de Robótica / Brazilian Robotics Tournament
