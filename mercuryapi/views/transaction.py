"""View module for handling requests about games"""
from mercuryapi.models import transaction
from mercuryapi.models.transaction import Transaction
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers 
from rest_framework import status
from datetime import date


class TransactionView(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Schedule instance
        """

        # Uses the token passed in the `Authorization` header
        transaction = Transaction.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        transaction = Transaction()
        transaction.date.time() 
        transaction.priceSold = request.data["priceSold"]
        transaction.quantity = request.data["quantity"]
        # Try to save the new Schedule to the database, then
        # serialize the Schedule instance as JSON, and send the
        # JSON as a response to the client request
        try:
            transaction.save()
            serializer = TransactionSerializer(product, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single Schedule
        Returns:
            Response -- JSON serialized Schedule instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            transaction = Transaction.objects.get(pk=pk)
            serializer = TransactionSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Transaction.DoesNotExist as ex:
            return Response(ex.args[0], status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Schedule
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            transaction = Transaction.objects.get(pk=pk)
            transaction.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Transaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource
        Returns:
            Response -- JSON serialized list of games
        """
        # Get all Schedule records from the database
        transactions = Transaction.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        transaction = self.request.query_params.get('transaction', None)
        if transaction is not None:
            transactions = transactions.filter(transactions__id=transactions)

        serializer = TransactionSerializer(
            transactions, many=True, context={'request': request})
        return Response(serializer.data)

class TransactionSerializer(serializers.ModelSerializer):
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
        model = Transaction
        fields = ('id', 'employee', 'product', 'date', 'priceSold', 'quantity')
        depth = 1