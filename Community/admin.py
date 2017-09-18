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


















# @admin.register(CommunityInstance)
# class CommunityInstanceAdmin(admin.ModelAdmin):
#     field_sets = (
#         ('Games', {
#          'fields': ('games', 'number_of_games')
#             }),
#         ('Awards', {
#             'fields': ('awards', 'number_of_awards')
#             }),
#         ('Talent', {
#             'fields' : ('type_of_talent', 'number_of_talent')
#             }),
#         )

# @admin.register(Game)
# class GameAdmin(admin.ModelAdmin):
#     list_view = ('name, description, number_of_participants, estimated_length')

# @admin.register(Talent)
# class TalentAdmin(admin.ModelAdmin):
#     list_view = ('name, description, author')
