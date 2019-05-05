from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Hero, Power, User


engine = create_engine('sqlite:///superhero.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(id=1, name="Varun", email="vchadha99@gmail.com")
session.add(User1)
session.commit()


hero1 = Hero(user_id=1,id= 0, name="IronMan")
session.add(hero1)
session.commit()

hero2 = Hero(user_id=1,id= 1, name="Thor")
session.add(hero2)
session.commit()

hero3 = Hero(user_id=1,id= 2, name="Captain America")
session.add(hero3)
session.commit()

hero4 = Hero(user_id=1,id= 3, name="SpiderMan")
session.add(hero4)
session.commit()

hero5 = Hero(user_id=1,id= 4, name="Hulk")
session.add(hero5)
session.commit()

hero6 = Hero(user_id=1,id= 5, name="Batman")
session.add(hero6)
session.commit()

hero7 = Hero(user_id=1,id= 6, name="Aquaman")
session.add(hero7)
session.commit()

power = Power(user_id=1,powers="Mechanical and Robotic Suit controlled\
                                by Tony Stark.",hero_id= 0)
session.add(power)
session.commit()

power = Power(user_id=1,powers="He can fly and fire",hero_id= 0)
session.add(power)
session.commit()

power = Power(user_id=1,powers="The god of lighting from Asgard\
                                with a mighty hammer.",hero_id= 1)
session.add(power)
session.commit()

power = Power(user_id=1,powers="He can give you high voltage shocks",hero_id= 1)
session.add(power)
session.commit()

power = Power(user_id=1,powers="The America's oldest but smartest\
                                and powerful hero of war",hero_id= 2)
session.add(power)
session.commit()

power = Power(user_id=1,powers="His mind game is very stong ",hero_id= 2)
session.add(power)
session.commit()
                                
power = Power(user_id=1,powers="Peter Parker a college student got bitten\
                                by spider and turns into saviour.",hero_id = 3)
session.add(power)
session.commit()

power = Power(user_id=1,powers="He is fast and flexible",hero_id= 3)
session.add(power)
session.commit()

power = Power(user_id=1,powers="The docter experiment with gama\
                                gone wrong and now he is a gaint",hero_id= 4)
session.add(power)
session.commit()

power = Power(user_id=1,powers="He can crush a plane into small balls",hero_id= 4)
session.add(power)
session.commit()

power = Power(user_id=1,powers="The billionare of gotham got science\
                                and made himself a suit and locomotive to save world.",hero_id= 5)
session.add(power)
session.commit()

power = Power(user_id=1,powers="He is superhero of night",hero_id= 5)
session.add(power)
session.commit()

power = Power(user_id=1,powers="The king of atlants and its rise ",hero_id= 6)
session.add(power)
session.commit()

power = Power(user_id=1,powers="He has the stongest triend",hero_id= 2)
session.add(power)
session.commit()

print("Heros added")