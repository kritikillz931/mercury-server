"""View module for handling requests about games"""

from mercuryapi.models.monthlyfinance import MonthlyFinance
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers 
from rest_framework import status


class MonthlyFinanceView(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized monthlyfinance instance
        """

        # Uses the token passed in the `Authorization` header
        monthlyfinance = MonthlyFinance.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        monthlyfinance = MonthlyFinance()
        monthlyfinance.month = request.data["month"]
        monthlyfinance.year = request.data["year"]
        monthlyfinance.cost = request.data["cost"]
        monthlyfinance.revenue = request.data["revenue"]
        monthlyfinance.profit = request.data["profit"]

        # Try to save the new monthlyfinance to the database, then
        # serialize the monthlyfinance instance as JSON, and send the
        # JSON as a response to the client request
        try:
            monthlyfinance.save()
            serializer = MonthlyFinanceSerializer(monthlyfinance, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single monthlyfinance
        Returns:
            Response -- JSON serialized monthlyfinance instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            monthlyfinance = MonthlyFinance.objects.get(pk=pk)
            serializer = MonthlyFinanceSerializer(monthlyfinance, context={'request': request})
            return Response(serializer.data)
        except MonthlyFinance.DoesNotExist as ex:
            return Response(ex.args[0], status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single monthlyfinance
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            monthlyfinance = MonthlyFinance.objects.get(pk=pk)
            monthlyfinance.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except MonthlyFinance.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource
        Returns:
            Response -- JSON serialized list of games
        """
        # Get all monthlyfinance records from the database
        monthlyfinances = MonthlyFinance.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        monthlyfinance = self.request.query_params.get('finance', None)
        if monthlyfinance is not None:
            monthlyfinances = monthlyfinances.filter(monthlyfinances__id=monthlyfinances)

        serializer = MonthlyFinanceSerializer(
            monthlyfinances, many=True, context={'request': request})
        return Response(serializer.data)

class MonthlyFinanceSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    Arguments:
        serializer typeINSERT INTO levelupapi_game (
            id,
            name,
            description,
            number_of_players,
            maker,
            game_type_id,
            gamer_id
          )
        VALUES (
            id:integer,
            'name:varchar(100)',
            'description:varchar(150)',
            number_of_players:integer,
            'maker:varchar(50)',
            'game_type_id:bigint',
            'gamer_id:bigint'
          );
    """
    class Meta:
        model = MonthlyFinance
        fields = ('id', 'month', 'year', 'cost', 'revenue', 'profit')
        depth = 1