from rest_framework import routers

from movie.views import MovieViewset

router = routers.SimpleRouter()
router.register(r'movies', MovieViewset)

urlpatterns = router.urls