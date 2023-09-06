

import click

from db import session
from models import Game, Customer, Order

@click.group()
def cli():
    pass

# @cli.command()
# def home():
#     click.echo(f' \n ======= (; Welcome Back :) ======= \n \n')
#     click.echo("""
#                1 > View a list of customers, available games and orders. \n
#                2 > Add new customers, new games or make an order. \n
#                3 > Update games. \n
#                4 > Delete games. \n
#                5 > Quit :( \n
#                """)
    
@cli.command() 
@click.option('--lists', prompt="view a list of customers:", help="--list view cust list")  
@click.argument('lists', type=int)     
def view_customer_list(lists):
    # lists = int(lists)
    click.echo('\n 1.  View a list of customers, available games and orders. \n')
    click.echo("Customer List. \n")
    get_customer_list()  
    click.echo('\n Available Games \n')
    get_games_list()
    click.echo('\n Orders Lists \n')  
    get_orders_list()   
    
@cli.command()
@click.option('-c', '--customer', prompt="Enter name, email", help="Enter your 'name, email'")
def add_customer(customer):
    name, email = customer.split(',')
    existing_customer = session.query(Customer).filter_by(email= email).first()
    
    if existing_customer:
        click.echo(f'This email address already exists.')
    new_customer = Customer(name, email)
    session.add(new_customer)
    session.commit()  
    click.echo(f'Added new customer: {name} ({email}) successfully')   
    
    # update_game(customer_id)    
        
@cli.command()
@click.option('-g', '--game', nargs=4, type=click.Tuple([str, str, str, int]), prompt="Enter title, genre, platform, price", help="Enter title, genre, platform, price")                      
def add_game(game):
    title, genre, platform, price = game
    new_game = Game(title, genre, platform, price)
    session.add(new_game)
    session.commit()
    click.echo(f'Game Title: {title} Genre: {genre} Platform: {platform} Price: {price} has been added successfully')

@cli.command()
# @click.option('-u', '--updates',prompt="Update game", help="Update Game")
def update_game():
    click.echo(f'\n Fetching Games list \n')
    get_games_list()
    
    id = input("\n Enter game id to update: \n")
    game_update(id)
    
    
@cli.command()
@click.option('-o', '--order', prompt="Add new Order", help="Order Transaction: quantity, customer_id, game_id")
def new_order(order):
    quantity, customer_id, game_id = order.split(',')
    new_order = Order(quantity, customer_id)
    
 
def get_customer_list():
    customer_list = session.query(Customer).all()
    result = []
    for customer in customer_list:
        result.append(f'{customer.id} {customer.name} {customer.email}')
    click.echo('\n'.join(result))    
    
    
def get_games_list():
    games_list = session.query(Game).all()
    results = []
    for game in games_list:
        results.append(f'{game.id} Title: {game.title}  Genre: {game.genre}  PLatform: {game.platform}  Price: {game.price}')
    click.echo(f'\n'.join(results))  
    
def get_orders_list():
    orders_list = session.query(Order).all()
    results = []
    for order in orders_list:
        results.append(f'{order.id}  Quantity: {order.quantity}  Game-id: {order.game_id}  Customer-id: {order.customer_id}  Total_price: {order.total_price}') 
    click.echo(f'\n'.join(results))          
           
def game_update(id):
    updates = session.query(Game).filter_by(id=id).first()
    print(f' \n id: {updates.id} Title: {updates.title}  Genre: {updates.genre}  PLatform: {updates.platform}  Price: {updates.price} \n')
    # return update
    
    changes = input("\n Enter the updates you'd like to make: (title, genre, platform, price)\n")
    title, genre, platform, price = changes.split(",")
   
    session.query(Game).filter_by(id=id).update({"title":title, "genre":genre, "platform":platform, "price":price})
    session.commit()
    get_games_list()
    
    
    


if __name__ == '__main__':
    cli()
