TRAVIS_REPO_SLUG ?= fernandoe/fe-instagram-api
TAG ?= local

build:
	docker build -t '${TRAVIS_REPO_SLUG}:${TAG}' .

ci.test:
	true
#	docker run --rm -it '${TRAVIS_REPO_SLUG}:${TAG}' pytest -s

compose-up:
	docker-compose up api-instagram

compose-migrate:
	docker-compose run --rm api-instagram python manage.py migrate

compose-createsuperuser:
	docker-compose run --rm api-instagram python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@example.com', 'password')"

compose-extract_tags:
	docker-compose run --rm api-instagram python manage.py extract_tags
