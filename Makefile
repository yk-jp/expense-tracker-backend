build:
	docker-coompose build -f docker-compose.yml .

run:
	docker-compose -f docker-compose.yml up

stop:
	docker-compose -f docker-compose.yml down

# clean container 
clean-c:
	docker rm expense-tracker-backend

# clean image
clean-i:
	docker rmi expense-tracker-backend

# clean image forcefully
clean-if:
	docker rmi -f expense-tracker-backend

# clean all
clean-all:
	$(MAKE) clean-c ; $(MAKE) clean-i
