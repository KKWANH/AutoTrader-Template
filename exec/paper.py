import time

class PaperBroker:
    def __init__(self): self.fills=[]

    def submit(self, symbol, side, qty, price):
        # Simulate slippage
        slip = 0.0005

        # Calculate fill price with slippage
        fill_price = price*(1+slip if side=="buy" else 1-slip)

        # Record the fill
        o = {"symbol":symbol,"side":side,"qty":qty,"price":fill_price,"ts":time.time()}

        # Append to fills
        self.fills.append(o)
        
        return o
