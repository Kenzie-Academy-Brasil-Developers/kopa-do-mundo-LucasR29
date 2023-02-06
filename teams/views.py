from rest_framework.response import Response
from rest_framework.views import APIView, Response, Request, status
from django.forms.models import model_to_dict
from django.db import IntegrityError
from .models import Team


class TeamView(APIView):
    def post(self, request: Request) -> Response:
        try:
            team = Team.objects.create(**request.data)

            team_dict = model_to_dict(team)

            return Response(team_dict, status.HTTP_201_CREATED)

        except IntegrityError as err:
            return Response({"error:": err.args[0]}, status.HTTP_400_BAD_REQUEST)

        except TypeError as err:
            return Response({"error:": err.args[0]}, status.HTTP_400_BAD_REQUEST)

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
            return Response({"error": "team not found"}, status.HTTP_404_NOT_FOUND)

        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"error": "team not found"}, status.HTTP_404_NOT_FOUND)

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"error": "team not found"}, status.HTTP_404_NOT_FOUND)

        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
