## See "FilipMinor.txt" for details about new rate calculation

## Returns cost of electricity as a function of watthours used
def electricityCost(watthrs: float) -> float:
    RatePerKwattHr = 0.135 
    return (watthrs/1000) * RatePerKwattHr # Cost of electrity for passed in number of Watt Hours

## Returns the cost of water as a function of gallons used
def waterCost(gallons: float) -> float:
    HCF = gallons/748
    if HCF < 4:
        Cost = HCF*2.59
    elif HCF <= 15:
        excess = HCF - 4
        Cost = 4*(2.59) + excess*(3.42)
    elif HCF > 15:
        excess = HCF - 15
        Cost = 4*(2.59) + 12*(3.42) + excess*(5.99)
    return Cost

## Returns watt/second power usage 
def power_per_second(watts: float) -> float:
    return watts / 3600 