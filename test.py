from interfaces.TestInterface import TestInterface
from HodgePodge import HodgePodge
from modules.Game import Game

boy = HodgePodge()
boy.attachModule(Game())

interface = TestInterface(boy)
interface.run()
