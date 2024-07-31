import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import TennisPlayer, Tournament, Match, SurfaceChoices
from django.db.models import Count

def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""

    elif search_name is not None and search_country is not None:
        players = TennisPlayer.objects.filter(
            full_name__icontains=search_name,
            country__icontains=search_country
        ).order_by('ranking')

    elif search_name is not None:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name).order_by('ranking')

    else:
        players = TennisPlayer.objects.filter(country__icontains=search_country).order_by('ranking')

    result = []
    for player in players:
        result.append(f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}")

    return '\n'.join(result) if result else ''


def get_top_tennis_player():
    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if not top_player:
        return ""

    return f"Top Tennis Player: {top_player.full_name} with {top_player.count_wins} wins."

def get_tennis_player_by_matches_count():
    player = TennisPlayer.objects.annotate(
        matches_count=Count('players')
    ).order_by('-matches_count', 'ranking').first()

    if not player or player.matches_count == 0:
        return ""

    return f"Tennis Player: {player.full_name} with {player.matches_count} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ""

    surface_type = Tournament.objects.filter(surface_type__icontains=surface).order_by('-start_date')

    result = []
    for match in surface_type:
        num_matches = match.all_matches.all().count() if match.all_matches else 0
        result.append(f"Tournament: {match.name}, start date: {match.start_date}, matches: {num_matches}")

    return '\n'.join(result) if result else ''


def get_latest_match_info():
    match = Match.objects.all().order_by('date_played', 'id').last()

    if not match:
        return ""

    all_players = ' vs '.join([x.full_name for x in match.players.all().order_by('full_name')])
    winner = match.winner.full_name if match.winner else "TBA"

    return f"Latest match played on: {match.date_played}, tournament: {match.tournament.name}, score: {match.score}, players: {all_players}, winner: {winner}, summary: {match.summary}"


def get_matches_by_tournament(tournament_name=None):
    matches = Match.objects.filter(tournament__name__exact=tournament_name).order_by('-date_played')

    if not matches or tournament_name is None:
        return "No matches found."

    result = []
    for match in matches:
        winner = match.winner.full_name if match.winner else 'TBA'
        result.append(f"Match played on: {match.date_played}, score: {match.score}, winner: {winner}")

    return '\n'.join(result) if result else ''
