from rest_framework.response import Response
from rest_framework.views import APIView, Response, Request, status
from .error import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError
from django.forms.models import model_to_dict
from django.db import IntegrityError
from datetime import datetime, timedelta
from .models import Team


class TeamView(APIView):
    def post(self, request: Request) -> Response:
        try:
            team = Team(**request.data)

            team_dict = model_to_dict(team)

            if team_dict.get("titles") < 0:
                raise NegativeTitlesError("titles cannot be negative")

            first_cup = datetime.strptime(team_dict.get("first_cup"), "%Y-%m-%d")
            first_cup_year = first_cup.year
            first_cup_year_to_iterate = first_cup.year

            now = datetime.now()
            now_year = now.year

            count = -2

            if first_cup_year > 1938 and first_cup_year < 1950 or first_cup_year < 1930:
                raise InvalidYearCupError("there was no world cup this year")

            while first_cup_year < now_year:
                first_cup_year += 4
                count += 1

            while first_cup_year_to_iterate > 1930:
                first_cup_year_to_iterate -= 4

            if first_cup_year_to_iterate < 1930:
                raise InvalidYearCupError("there was no world cup this year")

            if team_dict.get("titles") > count:
                raise ImpossibleTitlesError(
                    "impossible to have more titles than disputed cups"
                )

            team = Team.objects.create(**request.data)
            team_dict = model_to_dict(team)

            return Response(team_dict, status.HTTP_201_CREATED)

        except IntegrityError as err:
            return Response({"error:": err.args[0]}, status.HTTP_400_BAD_REQUEST)

        except TypeError as err:
            return Response({"error:": err.args[0]}, status.HTTP_400_BAD_REQUEST)

        except NegativeTitlesError as err:
            return Response(
                {"error": err.message},
                status.HTTP_400_BAD_REQUEST,
            )
        except InvalidYearCupError as err:
            return Response(
                {"error": err.message},
                status.HTTP_400_BAD_REQUEST,
            )
        except ImpossibleTitlesError as err:
            return Response(
                {"error": err.message},
                status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request: Request) -> Response:
        teams = Team.objects.all()

        teams_list = []

        for team in teams:
            team_dict = model_to_dict(team)
            teams_list.append(team_dict)

        return Response(teams_list, status.HTTP_200_OK)


class TeamViewDetail(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)

        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
