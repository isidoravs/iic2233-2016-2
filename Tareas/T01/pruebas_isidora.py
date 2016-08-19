moves = ["a", "b", "c"]
base_moves = [{"name": "c", "hola": 3}, {"name": "j", "hola": 3}, {"name": "a", "hola": 3}, {"name": "b", "hola": 3}]
new_moves = []

for movimiento in moves:
    for dicc in base_moves:
        if movimiento == dicc["name"]:
            new_moves.append(dicc)
            

print(new_moves)