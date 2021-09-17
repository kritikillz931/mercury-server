"""View module for handling requests about games"""

from django.contrib.auth.models import User
from mercuryapi.models.department import Department
from mercuryapi.models.employee import Employee
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers 
from rest_framework import status


class EmployeeView(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized employee instance
        """

        # Uses the token passed in the `Authorization` header
        employee = Employee.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        employee = Employee()
        employee.first_name = request.data["first_name"]
        employee.last_name = request.data["last_name"]
        employee.position = request.data["position"]
        employee.dateHired = request.data["dateHired"]
        employee.image = request.data["image"]
        department = Department.objects.get(pk=request.data["departmentId"])
        employee.department = department
        employee.employee = employee




        # Try to save the new employee to the database, then
        # serialize the employee instance as JSON, and send the
        # JSON as a response to the client request
        try:
            employee.save()
            serializer = EmployeeSerializer(employee, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single employee
        Returns:
            Response -- JSON serialized employee instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee, context={'request': request})
            return Response(serializer.data)
        except Employee.DoesNotExist as ex:
            return Response(ex.args[0], status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def update(self, request, pk=None):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        employee = Employee.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        employee = Employee.objects.get(pk=pk)
        employee.first_name = request.data["first_name"]
        employee.last_name = request.data["last_name"]
        employee.position = request.data["position"]
        employee.dateHired = request.data["dateHired"]
        employee.image = request.data["image"]
        employee.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)    


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single employee
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Employee.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource
        Returns:
            Response -- JSON serialized list of games
        """
        # Get all employee records from the database
        employees = Employee.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        employee = self.request.query_params.get('employee', None)
        if employee is not None:
            employees = employees.filter(employees__id=employees)

        serializer = EmployeeSerializer(
            employees, many=True, context={'request': request})
        return Response(serializer.data)

class EmployeeSerializer(serializers.ModelSerializer):
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
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'position', 'dateHired', 'image', 'department')
        depth = 1