#!/usr/bin/env python3
# Python 3.6

import hlt
from hlt import constants
from hlt.positionals import Direction
from hlt.positionals import Position
from hlt.game_map import MapCell
from astar import Astar

import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

def find_best_local_halite_spot(ship, game_map, reserved_targets = set(), radius = 4, min_halite = 0):
    best_pos = None
    best_halite = min_halite
    ship_pos = ship.position
    width, height = game_map.width, game_map.height
    
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx == 0 and dy == 0: 
                continue
            
            x = (ship_pos.x + dx) % width
            y = (ship_pos.y + dy) % height
            pos = Position(x, y)
            
            if pos in reserved_targets or game_map[pos].is_occupied: 
                continue
            
            halite = game_map[pos].halite_amount
            if halite > best_halite:
                best_halite = halite
                best_pos = pos
    
    return best_pos

def get_safe_move(ship, game_map, target, reserved_moves=set(), is_return=False):
    if ship.position == target:
        reserved_moves.add(ship.position)
        return ship.stay_still()
    
    direction = game_map.naive_navigate(ship, target)
    next_pos = ship.position.directional_offset(direction)
    
    if (next_pos not in reserved_moves and
        (not game_map[next_pos].is_occupied or game_map[next_pos].ship.owner == ship.owner)):
        reserved_moves.add(next_pos)
        return ship.move(direction)
    
    if is_return:
        circle_dirs = [Direction.North, Direction.South, Direction.East, Direction.West]
        random.shuffle(circle_dirs)
        for dir_alt in circle_dirs + [Direction.Still]:
            alt_pos = ship.position.directional_offset(dir_alt)
            if (alt_pos not in reserved_moves and
                (not game_map[alt_pos].is_occupied or game_map[alt_pos].ship.owner == ship.owner)):
                reserved_moves.add(alt_pos)
                return ship.move(dir_alt)
    else:
        alternatives = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]
        random.shuffle(alternatives)
        for dir_alt in alternatives:
            alt_pos = ship.position.directional_offset(dir_alt)
            if (alt_pos not in reserved_moves and
                (not game_map[alt_pos].is_occupied or game_map[alt_pos].ship.owner == ship.owner)):
                reserved_moves.add(alt_pos)
                return ship.move(dir_alt)
    
    reserved_moves.add(ship.position)
    return ship.stay_still()

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
game.ready("livlivbot03")
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))


'''
Gocollect = "go to collect halite"
Collecting = "Just collect halite"
Gobackhome = "go to shipyard"
Blockade = "block enemy shipyard"
'''

states = {}
targets = {}
blocker_ships = set() 
enemy_yard = None
count = 0
#astar = Astar(game.game_map)

while True:
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []

    ships = list(me.get_ships())
    random.shuffle(ships)

    reserved_targets = set()
    reserved_moves = set()

    shipyard = me.shipyard.position

    if enemy_yard is None:
        for pid, player in game.players.items():
            if pid != me.id and player.shipyard:
                enemy_yard = player.shipyard.position
                logging.info(f"Enemy yard: {enemy_yard}")
                break

    if len(blocker_ships) < 3:
        new_ships = sorted([s for s in ships if s.id not in blocker_ships], key=lambda s: s.id)
        for s in new_ships[:3 - len(blocker_ships)]:
            blocker_ships.add(s.id)
            states[s.id] = "Blockade"
        logging.info(f"Blockers: {blocker_ships}")

    returning_ships = [s for s in ships if s.halite_amount >= 600 + game_map.calculate_distance(s.position, shipyard) * 4]
    returning_ships.sort(key=lambda s: game_map.calculate_distance(s.position, shipyard))  
    
    for ship in returning_ships:
        logging.info(f"Ship {ship.id} RETURNING (priority)")
        cmd = get_safe_move(ship, game_map, shipyard, reserved_moves, is_return=True)
        command_queue.append(cmd)
   
    mining_ships = [s for s in ships if s not in returning_ships]
    random.shuffle(mining_ships)
    
    for ship in mining_ships:
        current_halite = game_map[ship.position].halite_amount
        dist_to_yard = game_map.calculate_distance(ship.position, shipyard)
        return_thresh = 600 + dist_to_yard * 4

        logging.info(f"Ship {ship.id} h={ship.halite_amount}/{return_thresh} cell={current_halite}")

        if ship.halite_amount >= return_thresh:
            logging.info(f"Ship {ship.id} RETURNING")
            cmd = get_safe_move(ship, game_map, shipyard, reserved_moves)
            command_queue.append(cmd)
            states[ship.id] = "Gobackhome"
            continue

        if ship.id not in states:
            states[ship.id] = "Gocollect"

        if states[ship.id] == "Blockade":
            # Circle enemy yard
            adj_cells = []
            for d in [Direction.North, Direction.South, Direction.East, Direction.West]:
                adj = enemy_yard.directional_offset(d)
                if not game_map[adj].is_occupied:
                    adj_cells.append(adj)
            circle_target = random.choice(adj_cells) if adj_cells else ship.position
            cmd = get_safe_move(ship, game_map, circle_target, reserved_moves)
            command_queue.append(cmd)

        if states[ship.id] == "Gocollect":
            logging.info("Gocollect")
            need_new_target = (
                ship.id not in targets or
                targets[ship.id] is None or
                game_map[targets[ship.id]].halite_amount < constants.MAX_HALITE * 0.05  
            )
            
            if need_new_target or current_halite < constants.MAX_HALITE * 0.1:  
                logging.info(f"Ship {ship.id} NEW TARGET (depleted/current low)")
                new_target = find_best_local_halite_spot(ship, game_map, reserved_targets)
                targets[ship.id] = new_target or ship.position
                if targets[ship.id] != ship.position:
                    reserved_targets.add(targets[ship.id])
            
            target = targets[ship.id]
            cmd = get_safe_move(ship, game_map, target, reserved_moves)
            command_queue.append(cmd)

            if (ship.position == target or current_halite > constants.MAX_HALITE * 0.12):
                states[ship.id] = "Collecting"

        elif states[ship.id] == "Collecting":
            logging.info("Collecting")
            cmd = ship.stay_still()
            command_queue.append(cmd)
            if ship.halite_amount >= return_thresh:
                states[ship.id] = "Gobackhome"
            if game_map[ship.position].halite_amount < constants.MAX_HALITE*0.12:
                states[ship.id] = "Gocollect"

        elif states[ship.id] == "Gobackhome":
            logging.info("Gobackhome")
            cmd = get_safe_move(ship, game_map, shipyard, reserved_moves)
            command_queue.append(cmd)

            if ship.position == shipyard:
                states[ship.id] = "Gocollect"


        
    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if (game.turn_number % 6 == 1 and
        me.halite_amount >= constants.SHIP_COST + 200 and
        not game_map[shipyard].is_occupied and
        count < 12):
        command_queue.append(me.shipyard.spawn())
        count += 1

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

