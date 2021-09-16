"""View module for handling requests about games"""
from mercuryapi.models.department import Department
from mercuryapi.models.employee import Employee
from mercuryapi.models.product import Product
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers 
from rest_framework import status


class ProductView(ViewSet):


    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Schedule instance
        """
        # Uses the token passed in the `Authorization` header
        employee = Employee.objects.get(user=request.auth.user) 


        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        product = Product()
        product.image = request.data["image"]
        product.name = request.data["name"]
        product.cost = request.data["cost"]
        product.priceSold = request.data["priceSold"]
        product.stock = request.data["cost"]
        department = Department.objects.get(pk=request.data["departmentId"])
        product.department = department
        product.employee = employee

        # Try to save the new Schedule to the database, then
        # serialize the Schedule instance as JSON, and send the
        # JSON as a response to the client request
        try:
            product.save()
            serializer = ProductSerializer(product, context={'request': request})
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
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Product.DoesNotExist as ex:
            return Response(ex.args[0], status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Schedule
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource
        Returns:
            Response -- JSON serialized list of games
        """
        # Get all Schedule records from the database
        products = Product.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        product = self.request.query_params.get('product', None)
        if product is not None:
            products = products.filter(products__id=products)

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

class ProductSerializer(serializers.ModelSerializer):
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
        model = Product
        fields = ('id', 'department', 'image', 'name', 'cost', 'priceSold', 'stock')
        depth = 1