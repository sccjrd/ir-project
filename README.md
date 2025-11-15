# IR_Project
Information Retrieval - IKEA hacks 

Theodor Vavassori, Francesc Jordi Sacco

1. HOW TO RUN SPIDERS

# Test IKEA Hackers 
scrapy crawl ikea -o data/ikea_hacks.json -s CLOSESPIDER_ITEMCOUNT=10

# Test Tosize 
scrapy crawl tosize -o data/tosize_hacks.json -s CLOSESPIDER_ITEMCOUNT=10

# Test Love Property
scrapy crawl loveproperty -o data/loveproperty_hacks.json -s CLOSESPIDER_ITEMCOUNT=10

# IKEA Hackers - get 100 items
scrapy crawl ikea -o data/ikea_hacks.json -s CLOSESPIDER_ITEMCOUNT=100

# Tosize - get 100 items
scrapy crawl tosize -o data/tosize_hacks.json -s CLOSESPIDER_ITEMCOUNT=100

# Love Property - get 100 items
scrapy crawl loveproperty -o data/loveproperty_hacks.json -s CLOSESPIDER_ITEMCOUNT=100

Total items in data repo:
ikea_hacks.json = 203 items
tosize_hacks.json = 20 items
loveproperty_hacks.json = 100 items
