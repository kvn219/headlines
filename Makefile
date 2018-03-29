up:
	docker build --force-rm=true -t kvn219/headlines .
	docker run --name headlines --rm -it  \
	--env-file	.env \
	-p 5000:5000 \
	-d \
	kvn219/headlines

reset:
	docker stop headlines
	docker build --force-rm=true -t kvn219/headlines .
	docker run --name headlines --rm -it  \
	--env-file	.env \
	-p 5000:5000 \
	-d \
	kvn219/headlines
