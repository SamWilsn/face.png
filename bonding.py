#!/usr/bin/env python3

SUPPLY = 147
INITIAL = 130000000000000
MULTIPLIER = 1082
DIVISOR = 1000
GIFTS = 1

last_price = INITIAL
total = 0

print("tokenId,price,cumulative")

for tokenId in range(GIFTS, SUPPLY):
    total += last_price
    print(tokenId, last_price, total, sep=",")
    last_price = (last_price * MULTIPLIER) // DIVISOR
