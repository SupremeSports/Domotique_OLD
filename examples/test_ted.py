from TED5000 import TED5000

ted = TED5000()

power = ted.get("Power","Total","PowerNow")

print(dir(ted))

print(power)
