from rest_framework.routers import DefaultRouter
from .views import TreinadorViewSet, PokemonViewSet

router = DefaultRouter()
router.register("treinadores", TreinadorViewSet)
router.register("pokemons", PokemonViewSet)
urlpatterns = router.urls