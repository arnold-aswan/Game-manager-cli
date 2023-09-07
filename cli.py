
import click

from main.database.db import session
from main.model.models import Game, Customer, Order

@click.group()
def cli():
    pass

@cli.command()     
def view_lists():
    click.echo("""\n View a list of 
               1 > customers \n 
               2 > available games \n 
               3 > orders. \n
               """)
    choice =click.prompt("view a list of 1. customers | 2. games | 3. orders:", type=int)

    if choice == 1:
        click.echo("Customer List. \n")
        get_customer_list()  
    elif choice == 2:    
        click.echo('\n Available Games \n')
        get_games_list()
    elif choice == 3:    
        click.echo('\n Orders Lists \n')  
        get_orders_list()   
    
@cli.command()
@click.option('--name', prompt="Enter your name:", help="Your name")
@click.option('--email', prompt="Enter email address", help="email address")
def add_customer(name, email):
    name = name
    email = email.replace(" ", "")
    existing_customer = session.query(Customer).filter_by(email=email).first()
    
    if existing_customer:
        click.echo(f'This email address already exists.')
        click.echo(f'Try a different email address')
    else:    
        new_customer = Customer(name, email)
        session.add(new_customer)
        session.commit()  
        click.echo(f'Added new customer: name:{name} email:{email} successfully') 
       
@cli.command()
@click.option('--title', prompt="Enter game title", help="The name of the game")          
@click.option('--genre', prompt="Enter game genre", help="The genre of te game")   
@click.option('--platform', prompt="The platform game is available to", help="PS4, ps5, xbox, pc, nintendo")   
@click.option('--price', type=int, prompt="Enter price of the game", help="i.e 60$")            
def add_game(title,genre,platform,price):
    new_game = Game(title, genre, platform, price)
    session.add(new_game)
    session.commit()
    click.echo(f' \n Game Title: {title} | Genre: {genre} | Platform: {platform} | Price: {price} | has been added successfully \n')

@cli.command()
def update_game():
    click.echo(f'\n Fetching Games list \n')
    get_games_list()
    
    id = input("\n Enter game id to update: \n")
    game_update(id)
    
    
@cli.command()
@click.option('--quantity', type=int, prompt="Quantity of games", help="No of games ordered")
@click.option('--customer_id', type=int, prompt="Enter customer id", help="input customer_id")
@click.option('--game_id', type=int, prompt="Enter game id", help="input game_id")
def new_order(quantity,customer_id,game_id ):
    new_order = Order(quantity, customer_id, game_id)
    session.add(new_order)
    session.commit()
    click.echo(f' +++ New order +++ \n Quantity: {quantity}, Cust.id: {customer_id}, Game.id: {game_id}')
    
@cli.command()
def delete_game():
    click.echo(f'\n Current list of games \n')
    get_games_list()
    id = input("\n Enter game id to delete: \n")
    game_deletion(id)
    
     
def get_customer_list():
    customer_list = session.query(Customer).all()
    result = []
    for customer in customer_list:
        result.append(f'id: {customer.id} | Name: {customer.name} | email: {customer.email}')
    click.echo('\n'.join(result))     
       
def get_games_list():
    games_list = session.query(Game).all()
    results = []
    for game in games_list:
        results.append(f'id: {game.id} | Title: {game.title} | Genre: {game.genre} | PLatform: {game.platform} | Price: {game.price}')
    click.echo(f'\n +++++ Games List +++++ \n')    
    click.echo(f'\n'.join(results))   
    
def get_orders_list():
    orders_list = session.query(Order).all()
    results = []
    for order in orders_list:
        results.append(f'id: {order.id} | Quantity: {order.quantity} | Game-id: {order.game_id} | Customer-id: {order.customer_id} | Total_price: {order.total_price}')
    click.echo(f'\n +++++ Orders List +++++ \n') 
    click.echo(f'\n'.join(results))          
           
def game_update(id):
    updates = session.query(Game).filter_by(id=id).first()
    print(f' \n id: {updates.id} Title: {updates.title}  Genre: {updates.genre}  PLatform: {updates.platform}  Price: {updates.price} \n')
    
    changes = input("\n Enter the updates you'd like to make: (title, genre, platform, price)\n")
    title, genre, platform, price = changes.split(",")
   
    session.query(Game).filter_by(id=id).update({"title":title, "genre":genre, "platform":platform, "price":price})
    session.commit()
    get_games_list()
    
def game_deletion(id):
    session.query(Game).filter_by(id=id).delete()
    session.commit()
    
    print(f' ----------------- Game deleted from database succesfully -----------------')
    print(f'\n +++++++++++++ Updated Games list +++++++++++++ \n')
    get_games_list()
        
    
if __name__ == '__main__':
    cli()
