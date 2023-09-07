
import random 
from faker import Faker

from model.models import Game, Customer, Order
from database.db import session

def populate_db():
    
    session.query(Game).delete()
    session.query(Customer).delete()
    session.query(Order).delete()
    
    fake = Faker()
    
    genres = ['action', 'adventure', 'strategy',
        'puzzle', 'first-person shooter', 'racing']
    
    platforms = ['switch', 'playstation 4', 'playstation 5', 'xbox one', 'xbox series s', 'pc']
    
    games = []
    
    for i in range(13):
        game = Game(
            title = fake.unique.name(),
            genre = random.choice(genres),
            platform = random.choice(platforms),
            price = random.randint(50, 100),
            available = True,
        )
        
        session.add(game)
        session.commit()
        games.append(game)
        
    customers = []
    for i in range(6):
        name = fake.name()
        email = name.replace(' ', '')+'@gmail.com'
        customer = Customer(
            name = name,
            email = email, 
        )    
        
        session.add(customer)
        session.commit()
        customers.append(customer)
        
    orders = []   
    for game in games:
        for i in range(random.randint(1,3)):
            customer = random.choice(customers)
            if game not in customer.games:
                customer.games.append(game)
                session.add(customer)
                session.commit()
              
            quantity = random.randint(1,5)   
            total = int(quantity) * int(game.price) 
            order = Order(
                quantity=quantity,
                customer_id=customer.id,  
                game_id=game.id,          
            )    
            order.total_price = total
            
            orders.append(order)
            
    session.bulk_save_objects(orders)
    session.commit()
    session.close()       
    
if __name__ == '__main__':
    print("database seeded")
    populate_db()        