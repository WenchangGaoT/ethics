# This file contains to top level code for the whole task
# It generate a shopping list and call functions for any specific
# shopping task

# please change "path" to absolute path if the yaml file fail to load

from navigation_operator import *
import argparse
import random

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--player_num", type=int, default=0)
    parser.add_argument("--player_id", type=int, default=0)
    args = parser.parse_args()

    player_num = args.player_num    
    player_id = args.player_id

    HOST = '127.0.0.1'
    PORT = 9000
    sock_game = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_game.connect((HOST, PORT))
    target_object = "milk"
    # path = "/home/frank/ethics/propershopper/config.yaml"
    path = "config.yaml"
    sock_game.send(str.encode(f"{player_id} NOP"))
    state = recv_socket_data(sock_game)
    state = json.loads(state)

    raw_shopping_list = state['observation']['players'][0]['shopping_list']
    list_quant = state['observation']['players'][0]['list_quant']
    # merge the shopping list and list_quant into one, each item on the new list means shopping the object ONCE
    shopping_list = []
    for i in range(len(raw_shopping_list)):
        for j in range(list_quant[i]):
            shopping_list.append(raw_shopping_list[i])
            
    shopping_list = ["cucumber","milk","garlic","cheese wheel","prepared foods"]

    random.shuffle(shopping_list)
    print("today's shopping task: {}".format(shopping_list))

    # determine shopping with carts or baskets
    if len(shopping_list)<=6:
        cart_or_basket = "baskets"
    else:
        cart_or_basket = "carts"

    # pickup cart or basket
    pick_operate = start_shopping_operator(sock_game, cart_or_basket, path, 
                                            player_num, player_id)
    pick_operate.get_cart_or_basket()
    
    # do the shopping of the list of items
    genral_buy = general_shopping(sock_game, shopping_list, cart_or_basket, path, 
                                  player_num, player_id)
    genral_buy.run_general_shopping()

    # go to the register
    nav_register = navigation_operator(sock_game,"registers", path, 
                                       player_num, player_id)
    nav_register.do_navigation()

    # checkout
    checkout_purchase = purchase_operator(sock_game, "registers", cart_or_basket, path, 
                                           player_num, player_id)
    checkout_purchase.checkout_good()  

    # return cart/basket
    # pick_operate.return_cart_or_basket()

    # leave
    exit_operate = leave_operator(sock_game, path, player_num, player_id)
    exit_operate.leave()
