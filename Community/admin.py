from django.contrib import admin
from .models import Game, CommunityGames, CommunityGameRatings, CommunityInst, CommunityPacingRatings, CommunityExtraRatings

@admin.register(CommunityInst)
class CommunityInstAdmin(admin.ModelAdmin):
	model = CommunityInst

@admin.register(CommunityGameRatings)
class CommunityGameRatingsAdmin(admin.ModelAdmin):
	model = CommunityGameRatings

@admin.register(CommunityGames)
class CommunityGames(admin.ModelAdmin):
	model = CommunityGames

@admin.register(Game)
class GamesAdmin(admin.ModelAdmin):
	model = Game

@admin.register(CommunityPacingRatings)
class CommunityPacingRatingAdmin(admin.ModelAdmin):
	model = CommunityPacingRatings

@admin.register(CommunityExtraRatings)
class CommunityExtraRatings(admin.ModelAdmin):
	model = CommunityExtraRatings
