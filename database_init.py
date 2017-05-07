from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///catalog.db')

# Clear database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

users = [{'email': 'worldmaps@gmail.com', 'username': 'worldmaps'}]

for user in users:
    user_obj = User(email=user['email'], name=user['username'])
    session.add(user_obj)
    session.commit()
user_id_1 = user_obj.id

category1 = Category(
    name='Europe',
    user_id=user_id_1)
session.add(category1)
session.commit()

item1 = Item(
    name='United Kingdom',
    user_id=user_id_1,
    category=category1,
    description="""The United Kingdom of Great Britain and Northern Ireland,
    commonly known as the United Kingdom (UK) or Britain, is a sovereign
    country in western Europe.""")
session.add(item1)
session.commit()

item2 = Item(
    name='Iceland',
    user_id=user_id_1,
    category=category1,
    description="""Iceland is a Nordic island country in the North Atlantic
    Ocean. It has a population of 332,529 and an area of 103,000 square
    kilometres, making it the most sparsely populated country in Europe. The
    capital and largest city is Reykjavik.""")
session.add(item2)
session.commit()

item3 = Item(
    name='Russia',
    user_id=user_id_1,
    category=category1,
    description="""Russia is a country in Eurasia.[14] At 17,075,200 square
    kilometres, Russia is the largest country in the world by surface area,
    covering more than one-eighth of the Earth's inhabited land area""")
session.add(item3)
session.commit()

item4 = Item(
    name='Greece',
    user_id=user_id_1,
    category=category1,
    description="""Greece, historically also known as Hellas, is a country in
    southeastern Europe, with a population of approximately 11 million as of
    2015. Athens is the nation's capital and largest city, followed by
    Thessaloniki.""")
session.add(item4)
session.commit()


category2 = Category(
    name='North America',
    user_id=user_id_1)
session.add(category2)
session.commit()

item1 = Item(
    name='Canada',
    user_id=user_id_1,
    category=category2,
    description="""Canada is a country in the northern part of North America.
    Its ten provinces and three territories extend from the Atlantic to the
    Pacific and northward into the Arctic Ocean, covering 9.98 million square
    kilometres, making it the world's second-largest country by total area and
    the fourth-largest country by land area.""")
session.add(item1)
session.commit()

item2 = Item(
    name='USA',
    user_id=user_id_1,
    category=category2,
    description="""The United States of America (USA), commonly known as the
    United States or America, is a constitutional federal republic composed of
    50 states, a federal district, five major self-governing territories, and
    various possessions. Forty-eight of the fifty states and the federal
    district are contiguous and located in North America between Canada and
    Mexico.""")
session.add(item2)
session.commit()


item3 = Item(
    name='Mexico',
    user_id=user_id_1,
    category=category2,
    description="""Mexico, officially the United Mexican States, is a federal
    republic in the southern half of North America. It is bordered to the north
    by the United States; to the south and west by the Pacific Ocean; to the
    southeast by Guatemala, Belize, and the Caribbean Sea; and to the east by
    the Gulf of Mexico.""")
session.add(item3)
session.commit()

category3 = Category(
    name='South America',
    user_id=user_id_1)
session.add(category3)
session.commit()

item1 = Item(
    name='Argentina',
    user_id=user_id_1,
    category=category3,
    description="""Argentina is a federal republic in the southern half of
    South America. Sharing the bulk of the Southern Cone with its neighbor
    Chile to the west, the country is also bordered by Bolivia and Paraguay to
    the north, Brazil to the northeast, Uruguay and the South Atlantic Ocean to
    the east, and the Drake Passage to the south.""")
session.add(item1)
session.commit()

item2 = Item(
    name='Brazil',
    user_id=user_id_1,
    category=category3,
    description="""Brazil is the largest country in both South America and
    Latin America. As the world's fifth-largest country by both area and
    population, it is the largest country to have Portuguese as an official
    language and the only one in the Americas.""")
session.add(item2)
session.commit()

item3 = Item(
    name='Chile',
    user_id=user_id_1,
    category=category3,
    description="""Chile is a South American country occupying a long, narrow
    strip of land between the Andes to the east and the Pacific Ocean to the
    west. It borders Peru to the north, Bolivia to the northeast, Argentina to
    the east, and the Drake Passage in the far south.""")
session.add(item3)
session.commit()

category4 = Category(
    name='Asia',
    user_id=user_id_1)
session.add(category4)
session.commit()

item1 = Item(
    name='Israel',
    user_id=user_id_1,
    category=category4,
    description="""Israel is a country in the Middle East, on the southeastern
    shore of the Mediterranean Sea and the northern shore of the Red Sea. It
    has land borders with Lebanon to the north, Syria to the northeast, Jordan
    on the east.""")
session.add(item1)
session.commit()

item2 = Item(
    name='India',
    user_id=user_id_1,
    category=category4,
    description="""India is a country in South Asia. It is the seventh-largest
    country by area, the second-most populous country (with over 1.2 billion
    people), and the most populous democracy in the world. It is bounded by the
    Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of
    Bengal on the southeast.""")
session.add(item2)
session.commit()

item3 = Item(
    name='Japan',
    user_id=user_id_1,
    category=category4,
    description="""Japan is a sovereign island nation in East Asia. Located in
    the Pacific Ocean, it lies off the eastern coast of the Asian mainland, and
    stretches from the Sea of Okhotsk in the north to the East China Sea and
    Taiwan in the southwest.""")
session.add(item3)
session.commit()

category5 = Category(
    name='Oceania',
    user_id=user_id_1)
session.add(category5)
session.commit()

item1 = Item(
    name='Australia',
    user_id=user_id_1,
    category=category5,
    description="""Australia is a country comprising the mainland of the
    Australian continent, the island of Tasmania and numerous smaller islands.
    It is the world's sixth-largest country by total area. The neighbouring
    countries are Papua New Guinea, Indonesia and East Timor to the north; the
    Solomon Islands and Vanuatu to the north-east; and New Zealand to the
    south-east. Australia's capital is Canberra, and its largest urban area is
    Sydney.""")
session.add(item1)
session.commit()

item2 = Item(
    name='New Zealand',
    user_id=user_id_1,
    category=category5,
    description="""New Zealand is an island nation in the southwestern Pacific
    Ocean. The country geographically comprises two main landmasses and around
    600 smaller islands.""")
session.add(item2)
session.commit()

item3 = Item(
    name='Fiji',
    user_id=user_id_1,
    category=category5,
    description="""Fiji is an island country in Melanesia in the South Pacific
    Ocean about 1,100 nautical miles (2,000 km; 1,300 mi) northeast of New
    Zealand's North Island. Its closest neighbours are Vanuatu to the west, New
    Caledonia to the southwest, New Zealand's Kermadec Islands to the
    southeast, Tonga to the east, the Samoas and France's Wallis and Futuna to
    the northeast, and Tuvalu to the north.""")
session.add(item3)
session.commit()

category6 = Category(
    name='Africa',
    user_id=user_id_1)
session.add(category5)
session.commit()

item1 = Item(
    name='Egypt',
    user_id=user_id_1,
    category=category6,
    description="""Egypt is a transcontinental country spanning the northeast
    corner of Africa and southwest corner of Asia by a land bridge formed by
    the Sinai Peninsula. Egypt is a Mediterranean country bordered by the Gaza
    Strip and Israel to the northeast, the Gulf of Aqaba to the east, the Red
    Sea to the east and south, Sudan to the south, and Libya to the west.""")
session.add(item1)
session.commit()

item2 = Item(
    name='Ethiopia',
    user_id=user_id_1,
    category=category6,
    description="""Ethiopia is a country located in the Horn of Africa. It
    shares borders with Eritrea to the north and northeast, Djibouti and
    Somalia to the east, Sudan and South Sudan to the west, and Kenya to the
    south. With over 100 million inhabitants,[3] Ethiopia is the most populous
    landlocked country in the world, as well as the second-most populous nation
    on the African continent after Nigeria.""")
session.add(item2)
session.commit()

item3 = Item(
    name='South Africa',
    user_id=user_id_1,
    category=category6,
    description="""South Africa is the southernmost country in Africa. It is
    bounded on the south by 2,798 kilometres of coastline of Southern Africa
    stretching along the South Atlantic and Indian Oceans, on the north by the
    neighbouring countries of Namibia, Botswana and Zimbabwe, and on the east
    and northeast by Mozambique and Swaziland, and surrounding the kingdom of
    Lesotho.""")
session.add(item3)
session.commit()

for i in session.query(Item).all():
    session.add(i)
    session.commit()
