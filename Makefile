build:
	docker-coompose build -f docker-compose.yml .

run:
	docker-compose -f docker-compose.yml up

stop:
	docker-compose -f docker-compose.yml down

# create db table 
create-table:
	docker exec expense-tracker-backend python manage.py makemigrations && docker exec expense-tracker-backend python manage.py migrate

# clean container 
clean-c-django:
	docker rm expense-tracker-backend

clean-c-mongodb:
	docker rm mongodb

clean-c-redis:
	docker rm redis

clean-c-all:
	$(MAKE) clean-c-django ; $(MAKE) clean-c-mongodb ; $(MAKE) clean-c-redis

# clean image 
clean-i-django:
	docker rmi expense-tracker-backend

clean-i-redis:
	docker rmi redis:7.0

clean-i-mongo:
	docker rmi mongo:5.0

clean-i-all:
	$(MAKE) clean-i-django ; $(MAKE) clean-i-mongodb ; $(MAKE) clean-i-redis

# clean image forcefully
clean-if-django:
	docker rmi -f expense-tracker-backend

clean-if-redis:
	docker rmi -f redis:7.0

clean-if-mongo:
	docker rmi -f mongo:5.0

clean-if-all:
	$(MAKE) clean-if-django ; $(MAKE) clean-if-mongodb ; $(MAKE) clean-if-redis

# clean all
clean-all:
	$(MAKE) clean-c-all; $(MAKE) clean-i-all

#clean volume
clean-v-mongo:
	docker volume rm expense-tracker-backend_mongo-data

clean-v-redis:
	docker volume rm expense-tracker-backend_redis-data

clean-v-all:
	$(MAKE) clean-v-mongo ; $(MAKE) clean-v-redis

