from django.contrib import admin
from .models import Gamedata, Ladder


class GamedataAdmin(admin.ModelAdmin):
    fields = ('game_name', 'api_key', 'admin_name', 'image')


class LadderAdmin(admin.ModelAdmin):
    fields = ('game_index', 'score')


admin.site.register(Gamedata, GamedataAdmin)
admin.site.register(Ladder, LadderAdmin)
