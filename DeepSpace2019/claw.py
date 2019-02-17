
import wpilib

from wpilib import Solenoid

from ctre import TalonSRX
from ctre import FeedbackDevice
from ctre._impl import StatusFrame
from ctre import ControlMode

class DeepSpaceClaw():

  def __init__(self, logger):
    self.logger = logger

  def init(self):
    self.logger.info("DeepSpaceClaw::init()")
    self.timer = wpilib.Timer()
    self.timer.start()

    self.drive_front_extend = Solenoid(9, 3)
    self.drive_front_retract = Solenoid(9, 2)
    self.drive_back_extend = Solenoid(9, 4)
    self.drive_back_retract = Solenoid(9, 5)

    self.claw_open = Solenoid(10, 2)
    self.claw_close = Solenoid(10, 3)

    self.left_grab = TalonSRX(5)
    self.right_grab = TalonSRX(6)
    self.wrist_talon = TalonSRX(8)

    self.claw_close.set(True)
    self.claw_open.set(False)

    self.drive_front_extend.set(False)
    self.drive_front_retract.set(True)
    self.drive_back_extend.set(False)
    self.drive_back_retract.set(True)

  def config(self):
    self.logger.info("DeepSpaceClaw::config()")
    self.wrist_talon.configSelectedFeedbackSensor(FeedbackDevice.Analog, 0, 10)
    self.wrist_talon.configSelectedFeedbackCoefficient(1.0, 0, 10)
    self.wrist_talon.setSensorPhase(False)
    self.wrist_talon.setStatusFramePeriod(StatusFrame.Status_2_Feedback0, 10, 10)
    self.wrist_talon.configNominalOutputForward(0.0, 10)
    self.wrist_talon.configNominalOutputReverse(0.0, 10)
    self.wrist_talon.configPeakOutputForward(1.0, 10)
    self.wrist_talon.configPeakOutputReverse(-1.0, 10)
    self.wrist_talon.enableVoltageCompensation(True)
    self.wrist_talon.configVoltageCompSaturation(11.5, 10)
    self.wrist_talon.configOpenLoopRamp(0.125, 10)

    self.left_grab.configNominalOutputForward(0.0, 10)
    self.left_grab.configNominalOutputReverse(0.0, 10)
    self.left_grab.configPeakOutputForward(1.0, 10)
    self.left_grab.configPeakOutputReverse(-1.0, 10)
    self.left_grab.enableVoltageCompensation(True)
    self.left_grab.configVoltageCompSaturation(11.5, 10)
    self.left_grab.configOpenLoopRamp(0.125, 10)

    self.right_grab.configNominalOutputForward(0.0, 10)
    self.right_grab.configNominalOutputReverse(0.0, 10)
    self.right_grab.configPeakOutputForward(1.0, 10)
    self.right_grab.configPeakOutputReverse(-1.0, 10)
    self.right_grab.enableVoltageCompensation(True)
    self.right_grab.configVoltageCompSaturation(11.5, 10)
    self.right_grab.configOpenLoopRamp(0.125, 10)

  def iterate(self, pilot_stick, copilot_stick):
    if self.timer.hasPeriodPassed(0.5):
      self.logger.info("DeepSpaceClaw::iterate()")
      self.logger.info("Claw current: " + str(self.wrist_talon.getOutputCurrent()))
      self.logger.info("Claw position: " + str(self.wrist_talon.getSelectedSensorPosition(0)))
      self.logger.info("Claw analog in: " + str(self.wrist_talon.getAnalogInRaw()))
    self.wrist_talon.set(ControlMode.PercentOutput, pilot_stick.getRawAxis(1))

    if pilot_stick.getRawButton(1):
      self.left_grab.set(ControlMode.PercentOutput, 0.5)
      self.right_grab.set(ControlMode.PercentOutput, -0.5)
    elif pilot_stick.getRawButton(2):
      self.left_grab.set(ControlMode.PercentOutput, -0.5)
      self.right_grab.set(ControlMode.PercentOutput, 0.5)
    else:
      self.left_grab.set(ControlMode.PercentOutput, 0.0)
      self.right_grab.set(ControlMode.PercentOutput, 0.0)

    if pilot_stick.getRawButton(3):  #X
      self.claw_close.set(True)
      self.claw_open.set(False)
    elif pilot_stick.getRawButton(4): #Y
      self.claw_close.set(False)
      self.claw_open.set(True)




  def disable(self):
    self.logger.info("DeepSpaceClaw::disable()")
